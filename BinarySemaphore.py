class BinarySemaphore:
    count = 0

    def waitForResource(self):
        while (self.count == 0): pass

    def waitForGettingResource(self):
        while (self.count == 1): pass

    def putResource(self):
        self.count = 1

    def getResource(self):
        self.count = 0

