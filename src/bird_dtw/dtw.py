# core DTW file. 
import math
class DTW: 
    def __init__(self, A: list[tuple[float, float]], B: list[tuple[float, float]], W: int): 
        """
        Initialize latitude-longitude system to compare each animal's migratory path
        against its template path, i.e: [(lat1, lon1), (lat2, lon2), (lat3, lon3)]
        haversine = distance between 2 (lat, lon) points on a sphere. 
        DTW = overall alignment function we are using. 
        Window = the sakoe-chiba band size. 
        Latitude analogy -> horizontal stripes (e.x. rings of saturn)
        Longitude analogy -> vertical wedges (e.x. terry's chocolate orange)
        """
        self.individual_path: list[tuple[float, float]] = A #goes on the rows  
        self.template_path: list[tuple[float, float]] = B #goes on the columns
        self.ROWS, self.COLS = len(self.individual_path), len(self.template_path)
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
        #use lazy loading for instance variable creation. 
        self.dp = [[float('inf')] * self.COLS for _ in range(self.ROWS)]
        self.dp[0][0] = self._get_haversine_km(self.individual_path[0], self.template_path[0])
        #fill first row 
        first_individual_path_point = self.individual_path[0]
        for c in range(1, self.COLS): 
            if not self._in_band(0, c): 
                continue #allow for re-entry into the valid band 
            self.dp[0][c] = self._get_haversine_km(
                first_individual_path_point, self.template_path[c] 
            ) + self.dp[0][c-1]
        #fill first col 
        first_template_path_point = self.template_path[0]
        for r in range(1, self.ROWS): 
            if not self._in_band(r, 0):  
                continue #allow for re-entry into band 
            self.dp[r][0] = self._get_haversine_km(
                self.individual_path[r], first_template_path_point
            ) + self.dp[r-1][0]
        #fill in the rest: 
        for r in range(1, self.ROWS): 
            for c in range(1, self.COLS): 
                if not self._in_band(r, c): 
                    continue # Band is diagonal; we can re-enter after leaving
                self.dp[r][c] = self._get_haversine_km(
                    self.individual_path[r],
                    self.template_path[c]
                ) + self._get_cost(r, c)
        return (self.dp[self.ROWS-1][self.COLS-1], self.dp) #also return the matrix for futher use

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
        self.path: list[tuple[int, int]] = [] #use lazy loading for instance variable creation. 
        r, c = self.ROWS-1, self.COLS-1 #start at bottom right hand corner 
        while r > 0 or c > 0: 
            self.path.append((r, c))
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
        self.path.append((0, 0))
        self.path.reverse()
        return self.path

    def convert_path_indices_to_original_coordinates(self):
        """
        Converts grid indices to actual lat/lon coordinates. 
        """
        res: list[tuple[float, float]] = []
        for r, c in self.path: 
            res.append((self.individual_path[r], self.template_path[c]))
        return res

    def _in_band(self, r: int, c: int) -> bool: 
        """
        private helper function to determine whether or not a given (r, c) cell falls 
        within the allowable band size. 
        """
        expected_c = r * (self.COLS / self.ROWS)
        return abs(c - expected_c) <= self.window

    def _get_haversine_km(self, p1: tuple[float, float], p2: tuple[float, float]) -> float:
        lat1, lon1 = math.radians(p1[0]), math.radians(p1[1])
        lat2, lon2 = math.radians(p2[0]), math.radians(p2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        R = 6371
        return R * c
        
