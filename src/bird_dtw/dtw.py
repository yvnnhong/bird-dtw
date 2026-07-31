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
        pass #temp
