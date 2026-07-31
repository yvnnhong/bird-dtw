# core DTW file. 
class DTW: 
    def __init__(): 
        """
        Initialize latitude-longitude system to compare each animal's migratory path
        against its template path, i.e: [(lat1, lon1), (lat2, lon2), (lat3, lon3)]
        Euclidean = local cost function we are using. 
        DTW = overall alignment function we are using. 
        Window = the sakoe-chiba band size. 
        Latitude analogy -> horizontal stripes (e.x. rings of saturn)
        Longitude analogy -> vertical wedges (e.x. terry's chocolate orange)
        """
        