class HOMuon:
    def __init__(self, eta, phi, pt, quality):
        self._eta = eta
        self._phi = phi
        self._pt = pt 
        self.quality = quality
    
    def printInfo(self):
        print 'Quality: ' + str(self.quality) + ' Eta: ' + str(self._eta) + ' Phi: ' + str(self._phi) + ' pT: ' + str(self._pt)
    
    def eta(self):
        return self._eta
    
    def phi(self):
        return self._phi
    
    def pt(self):
        return self._pt
    
    def equals(self, otherMuon):
        if self.pt() == otherMuon.pt() and self.phi() == otherMuon.phi() and self.eta() == otherMuon.eta():
            return True
        return False