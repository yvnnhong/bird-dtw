# core DTW file. 
import math
class DTW: 
    def __init__(self, A: list[tuple[float, float]], B: list[tuple[float, float]], W: int): 
        """
        Initialize latitude-longitude system to compare each animal's migratory path
        against its template path, i.e: [(lat1, lon1), (lat2, lon2), (lat3, lon3)]
        Euclidean = local cost function we are using. 
        DTW = overall alignment function we are using. 
        Window = the sakoe-chiba band size. 
        Latitude analogy -> horizontal stripes (e.x. rings of saturn)
        Longitude analogy -> vertical wedges (e.x. terry's chocolate orange)
        """
        self.individual_path: list[tuple[float, float]] = A #goes on the rows  
        self.template_path: list[tuple[float, float]] = B #goes on the columns
        self.ROWS, self.COLS = len(self.individual_rows), len(self.template_path)
        self.window: int = W

    def dynamic_time_warping(self) -> None: 
        """
        Returns the final DTW distance of a specific bird species against the template path.
        We use the standard convention for a 2D Dynamic Time Warping matrix: 
        The input sequence (A; individual bird path) is assigned to the rows. 
        The template sequence (B) is assigned to the columns.
        Visual: 
            B0 B1 B2 
         A0 [[] [] []
         A1  [] [] []
         A2  [] [] []] 
         A note on the sakoe-chiba band: 
         window=30 means that the warping path can deviate at MOST 30 GPS observations 
         from the diagonal, so in practice, that is roughly a few days of timing
         flexibility. 
         For example: 
         If W = 30, then the sakoe-chiba band is saying "this eagle's day 50 can only 
         match template days 20-80. It is a TIME flexibility constraint, not a geographic one.  
        """
        self.dp = [[float('inf')] * self.COLS for _ in range(self.ROWS)]
        self.dp[0][0] = self._get_euclidean_distance(self.individual_path[0], self.template_path[0])
        #fill first row 
        first_individual_path_point = self.individual_path[0]
        for c in range(1, self.COLS): 
            if c > self.window: 
                break #continue is also ok here, but break is an optimization.
            self.dp[0][c] = self._get_euclidean_distance(
                first_individual_path_point, self.template_path[c] 
            ) + self.dp[0][c-1]
        #fill first col 
        first_template_path_point = self.template_path[0]
        for r in range(1, self.ROWS): 
            if r > self.window: 
                break #continue is also ok here, but break is an optimization.
            self.dp[r][0] = self._get_euclidean_distance(
                self.individual_path[r], first_template_path_point
            ) + self.dp[r-1][0]
        #fill in the rest: 
        for r in range(1, self.ROWS): 
            for c in range(1, self.COLS): 
                if abs(r-c) > self.window:
                    continue # Band is diagonal; we can re-enter after leaving
                self.dp[r][c] = self._get_euclidean_distance(
                    self.individual_path[r],
                    self.template_path[c]
                ) + self._get_cost(r, c)
        return (self.dp[self.ROWS-1][self.COLS-1], self.dp) #also return the matrix for futher use

    def _get_euclidean_distance(self, p1: tuple[float, float], p2: tuple[float, float]) -> float: 
        """Our local cost function (Euclidean) to compare 2 points against each other."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def _get_cost(self, r: int, c: int) -> float: 
        return min(
            self.dp[r-1][c], #cell directly above
            self.dp[r][c-1], #cell directly left 
            self.dp[r-1][c-1] #cell directly diagonal up-left 
        )

    def backtrack(self) -> list[tuple[int, int]]: #temp
        """
        This backtracking function returns the indices (zero-indexed) corresponding
        to the optimal path that leads to the best DTW distance.
        Input: the 2D result matrix from the dynamic_time_warping function. 
        """
        path: list[tuple[int, int]] = []
        r, c = self.ROWS-1, self.COLS-1 #start at bottom right hand corner 
        while r > 0 or c > 0: 
            path.append((r, c))
            if r == 0: #can only go left 
                c -= 1 
            elif c == 0: #can only go up 
                r -= 1
            else: 
                best: float = min(
                    self.dp[r-1][c], #up
                    self.dp[r][c-1], #left 
                    self.dp[r-1][c-1] #diagonal up-left 
                )
                #This is written so that if there is a tie between best choices, 
                #it follows the order below. 
                if best == self.dp[r-1][c-1]: #move position accordingly 
                    r, c = r-1, c-1 
                elif best == self.dp[r-1][c]: #go up
                    r -= 1 
                elif best == self.dp[r][c-1]: 
                    c -= 1 #go left 
        path.append((0, 0))
        path.reverse()
        return path
        
