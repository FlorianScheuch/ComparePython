import math

class Utils:
    @staticmethod
    def getEta(z, r):
        a = math.atan(z/r)
        b = math.tan(a/2)
        c = -1.*math.log(b)
        return c
    
    @staticmethod
    def getDistance(muon1, muon2):
        return ((muon1.eta()-muon2.eta())**2+(muon1.phi()-muon2.phi())**2)**.5

    @staticmethod
    def getMatch(muon1, muonList, minR, relPt):
        minDist = 10
        if len(muonList) == 0 :
            return
        minMuon = muonList[0]
        for element in muonList:
            if Utils.getDistance(muon1, element) < minDist:
                minDist = Utils.getDistance(muon1, element)
                minMuon = element
        #print 'R: ',minDist, ' pT: ', minMuon.pt(), ' pTL1: ', muon1.pt() 
        if minDist > minR:
        #2**.5*math.pi/36:i
        #print 'NoMatch'
            return 
        if abs((minMuon.pt()-muon1.pt())/(minMuon.pt()+muon1.pt())) > relPt:
            #print 'NoMatch'
            return
        return minMuon
    
    @staticmethod
    def isInRange(l1Muon):
        if(abs(l1Muon.eta()) < Utils.getEta(4.02, 6.61)):
            return True
        return False
    
    @staticmethod
    def isSame(muon1, muon2):
        if muon1 == None:
            return False
        if muon2 == None:
            return False
        if(muon1.pt() == muon2.pt()):
            if(muon1.phi() == muon2.phi()):
                if(muon1.eta() == muon2.eta()):
                    return True
        return False
    
    @staticmethod
    def translateToIEta(eta):
        val = eta/(2*math.pi/72)
        val = int(val)
        if eta < 0:
            val = val - 1
        else:
            val = val + 1
        return val
    
    @staticmethod
    def translateToIPhi(phi):
        if phi < 0:
            val = 2*math.pi + phi
        else:
            val = phi
        val = val/2/math.pi*72
        val = int(val)
        val = val + 1
        return val
    
    @staticmethod
    def getHoEntry(iphi, ieta, hoEntries):
        for i in range(hoEntries.size()):
            bg = hoEntries.__getitem__(i)
            detId = bg.id()
            if detId.iphi() == iphi and detId.ieta() == ieta:
                return bg
        return
    
    @staticmethod
    def getHighestHoEntry3(iphi, ieta, hoEntries):
        high = 0
        for i in range(hoEntries.size()):
            bg = hoEntries.__getitem__(i)
            detId = bg.id()
            for xphi in xrange(3):
                nphi = (((iphi-1) + 72 - 1 + xphi)%72) + 1
                #print 'search: ', nphi, ' xphi: ' , xphi
                if detId.iphi() == nphi and detId.ieta() == ieta:
                    if high < bg.energy():
                        high = bg.energy()
        return high