import math
import ROOT
#from colorama import init, Fore, Back, Style

class Utils:
        
        
    @staticmethod
    def toL1Pt(pT):
        if pT <= 8:
            return pT
        if pT <= 10:
            return 10
        if pT <= 12:
            return 12
        if pT <= 14:
            return 14
        if pT <= 16:
            return 16
        if pT <= 18:
            return 18
        if pT <= 20:
            return 20
        if pT <= 25:
            return 25
        if pT <= 30:
            return 30
        if pT <= 35:
            return 35
        if pT <= 40:
            return 40
        if pT <= 45:
            return 45
        if pT <= 50:
            return 50
        if pT <= 60:
            return 60
        if pT <= 70:
            return 70
        if pT <= 80:
            return 80
        if pT <= 90:
            return 90
        if pT <= 100:
            return 100
        if pT <= 120:
            return 120
        return 140
        
    
    @staticmethod
    def getEta(z, r):
#         print 'z: ', str(z), ' r: ', str(r)
        a = math.atan(z/r)
#         print 'a: ', str(a)
        b = math.tan(a/2)
#         print 'b: ', str(b)
        c = -1.*math.copysign(1, b)*math.log(abs(b))
#         print 'Eta (c): ' + str(c)
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
        minDist = Utils.getDistance(muon1, minMuon)
        
        
        for element in muonList:
            if Utils.getDistance(muon1, element) < minDist:
                minDist = Utils.getDistance(muon1, element)
                minMuon = element
        #print 'R: ',minDist, ' pT: ', minMuon.pt(), ' pTL1: ', muon1.pt() 
        if minDist > minR:
        #2**.5*math.pi/36:i
        #print 'NoMatch'
            return 
        if (minMuon.pt()-muon1.pt())/(minMuon.pt()+muon1.pt()) > relPt:
            #print 'NoMatch'
            return
        return minMuon
    
    @staticmethod
    def matchJet(muon, jetList, minR):
        minRNow = 1000
        particle = None
        for element in jetList:
            if Utils.getDistance(muon, element) < minR and Utils.getDistance(muon, element) < minRNow and element.pt() > 4:
                minRNow = Utils.getDistance(muon, element)
                particle = element
        if minRNow < 1000:
            return particle
        return
    
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
    def findNearestRecoMuon(c, l1MuonTuple):
        deltaR = 10
        el = None
        for element in l1MuonTuple:
            if Utils.getDistance(c, element[0]) < deltaR:
                deltaR = Utils.getDistance(c, element[0])
                el = element
        return el
    
                    
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
    
    @staticmethod
    def getTrigPos(trig):
        wh = trig.whNum()
        sec = trig.scNum()+1
        phi = trig.phi()
        phi = Utils.getNewAngle(trig) ###Change
        phiB = trig.phiB()

        
        #dir = (phi/4096.)
        
        dir = phi/4096.*180./math.pi
        
        if sec < 6:
            dir = dir + (sec-1)*28
        else:
            dir = dir + (sec-13)*28
        #print 'pos, dir: ', dir, ' wh: ', wh, 'sec: ', sec, ' phi: ', phi
        return dir
    
    @staticmethod
    def getNewAngle(trig):
        """ This method calculates the entrance position of a muon in HO
            Therefore, the position at a certain muon station is used and a linear or a circular extrapolation is done
            l is the distance from the beam axis to the certain muon station
            a is the distance between muon station and HO"""
#        return trig.phi()
        phi = trig.phi()/4096.
        phiB = trig.phiB()/512.
        a = .2
        if trig.stNum() == 1:
            l = 3.85 #station 1
        if trig.stNum() == 2:
            l = 4.645 #station 2
        b = l-a
        return math.atan((l*math.tan(phi) - a*math.tan(phi+phiB))/b)*4096.
        
        r = Utils.getBendingRadius(trig)# getRadius
        #val = (r*math.cos(math.asin(-1.*a/r-math.sin(phi+phiB)))+l*math.tan(phi)-r*math.cos(phi+phiB))/b
        try:
            radPhi = math.atan((r*math.cos(math.asin(-1.*a/r-math.sin(phi+phiB)))+l*math.tan(phi)-r*math.cos(phi+phiB))/b)
            
            #print phi, ' ', radPhi
        

            return radPhi*4096.
        except:
            newPhi = math.atan((l*math.tan(phi) - a*math.tan(phi+phiB))/b)
            return newPhi*4096.
    
    @staticmethod
    def getPtFromDigi(phDigi): #DONE
        stNum = phDigi.stNum()
    # Return pT from digi
    # Use fit parameters from Dropbox/Promotion/CMS/Analyse/DTAngle/Script.c
        if stNum==2:
            p0 = 8.00605e-1
            p1 = 1.84458
            p2 = 1.71943e-2
            n0 = -7.91097e-1
            n1 = 1.89551
            n2 = -1.75413e-2
        elif stNum==1:
            p0 = 1.10456
            p1 = 2.27101
            p2 = 1.57637e-2
            n0 = -1.07813
            n1 = 2.34187
            n2 = -2.00791e-2
        else:
            return 0
        phiB = phDigi.phiB()/512.
        if phiB < 0:
            return abs(n0/(phiB-n2)+n1)
        else:
            return abs(p0/(phiB-p2)+p1)
    
    @staticmethod
    def getBendingRadius(trig):
        pT = Utils.getPtFromDigi(trig)
        return 3.33*pT/1
    
    @staticmethod
    def hasPositiveRF(trig):
        if trig.whNum() > 0 or trig.scNum()%4>1:
            return True
        return False
    
    @staticmethod
    def save(name, *plot):
        file = ROOT.TFile(name, 'RECREATE')
        for x in plot:
            x.Write()
        file.Close()
    
    @staticmethod
    def getTrigDir(trig):
        wh = trig.whNum()
        sec = trig.scNum()+1
        phi = trig.phi()
        phiB = trig.phiB()
        
        phi = Utils.getNewAngle(trig)
        
        #dir = (phi/4096.)*180./math.pi
        dir = (phiB/512.+phi/4096.)*180./math.pi
        

        if sec < 6:
            dir = dir + (sec-1)*28
        else:
            dir = dir + (sec-1)*28
            
        #if wh>0 or (wh == 0 and sec%4>1):
        #    dir = -dir
        return dir