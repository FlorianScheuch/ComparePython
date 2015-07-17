class HOMuon:
    def __init__(self, eta, phi, pt, quality):
        self.eta = eta
        self.phi = phi
        self.pt = pt 
        self.quality = quality
    
    def printInfo(self):
        print 'Quality: ' + str(self.quality) + ' Eta: ' + str(self.eta) + ' Phi: ' + str(self.phi) + ' pT: ' + str(self.pt)