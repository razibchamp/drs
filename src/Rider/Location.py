class Location:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def getLocation(self):
        return "lat :" + str(self.latitude) + "    Lng: " + str(self.longitude)
    
    def getLat(self):
        return self.latitude
        
    def getLng(self):
        return self.longitude

    