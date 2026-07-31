# core DTW file. 
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
        
        pass #temp
