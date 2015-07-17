import ROOT
import math
from DataFormats.FWLite import Events, Handle
from Utils import *
from HOMuon import *

MAX_NUMBER = 24000

numberOfGoodNonBadByDeltaRPileUp = ROOT.TH1D ("numberOfGoodNonBadByDeltaRPileUp", "numberOfGoodNonBadByDeltaRPileUp", 100, -.005, .995)
numberOfNonGoodBadByDeltaRPileUp = ROOT.TH1D ("numberOfNonGoodBadByDeltaRPileUp", "numberOfNonGoodBadByDeltaRPileUp", 100, -.005, .995)
numberOfNonGoodNonBadByDeltaRPileUp = ROOT.TH1D ("numberOfNonGoodNonBadByDeltaRPileUp", "numberOfNonGoodNonBadByDeltaRPileUp", 100, -.005, .995)
numberOfGoodBadByDeltaRPileUp = ROOT.TH1D ("numberOfGoodBadByDeltaRPileUp", "numberOfGoodBadByDeltaRPileUp", 100, -.005, .995)

numberOfGoodNonBadByDeltaRPileUpGen = ROOT.TH1D ("numberOfGoodNonBadByDeltaRPileUpGen", "numberOfGoodNonBadByDeltaRPileUpGen", 100, -.005, .995)
numberOfNonGoodBadByDeltaRPileUpGen = ROOT.TH1D ("numberOfNonGoodBadByDeltaRPileUpGen", "numberOfNonGoodBadByDeltaRPileUpGen", 100, -.005, .995)
numberOfNonGoodNonBadByDeltaRPileUpGen = ROOT.TH1D ("numberOfNonGoodNonBadByDeltaRPileUpGen", "numberOfNonGoodNonBadByDeltaRPileUpGen", 100, -.005, .995)
numberOfGoodBadByDeltaRPileUpGen = ROOT.TH1D ("numberOfGoodBadByDeltaRPileUpGen", "numberOfGoodBadByDeltaRPileUpGen", 100, -.005, .995)

deltaZ = ROOT.TH1D("Delta z position", "Delta z position", 100, -1, 1)
eventsBad = Events ('FEVT_NonWorkingDetector.root') #sample with dead MB1
eventsGood = Events ('FEVT_WorkingDetector.root')

# create handle outside of loop
genParticlesHandle  = Handle ('std::vector<reco::GenParticle>')
goodMuonsHandle  = Handle ('std::vector<reco::Muon>')
badMuonsHandle = Handle('std::vector<reco::Muon>')
badL1MuonsHandle = Handle('std::vector<l1extra::L1MuonParticle>')
goodL1MuonsHandle = Handle('std::vector<l1extra::L1MuonParticle>')
hoEntriesHandle = Handle('edm::SortedCollection<HORecHit,edm::StrictWeakOrdering<HORecHit>>')
phiContainerHandle = Handle('L1MuDTChambPhContainer')
thContainerHandle = Handle('L1MuDTChambThContainer')
#phiContainerHandle = Handle('L1MuDTChambPhContainer')
# a label is just a tuple of strings that is initialized justvector<reco::GenParticle>
# like and edm::InputTag
label = ("muons")
labelL1 = ("l1extraParticles")
labelHoEntries = ("horeco")
labelPhiContainer = ("dttfDigis")
labelThContainer = ("dttfDigis")
labelGenParticles = ("genParticles")

#print Utils.getEta(4.02, 6.61) #Straight line from center to end of station 1 in wheel 2
#print Utils.getEta(7.38, 6.61) #Straight line from center to end of station 4 in wheel 2
#print Utils.getEta(4.02, 3.954) #Straight line from center to end of station 1 wheel 1
#print Utils.getEta(4.02, 1.268) #Straight line from center to end of station 1 in wheel 0
print Utils.getEta(4.645, 1.28)
#print 2**.5*math.pi/36

def save(name, *plot):
    file = ROOT.TFile(name, 'RECREATE')
    for x in plot:
        x.Write()
    file.Close()

def printDigis(phDigi, thDigi):
    for d in phDigi:
        if d.stNum() == 2 and d.scNum() == 1 and d.whNum() == 0:
            print 'Station: ', d.stNum(), ' Sector: ', d.scNum(), ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
    for d in thDigi:
        if d.stNum() == 2 and d.scNum() == 1 and d.whNum() == 0:
            for pos in xrange(8):
                if d.position(pos) > 0:
                    print 'Station: ', d.stNum(), ' Sector: ', d.scNum(), ' Wheel: ', d.whNum(), ' pos: ', pos

def matchesHO(phDigi, thDigi, hoEntries, qualityCodes2d): #DONE
    # Do correction if possible here
    iphi = 5
    phi = Utils.getTrigPos(phDigi)
    print 'Trigger position: ', str(phi)
    if phi > -10 and phi <= -5:
        iphi = 71
    if phi > -5 and phi <= 0:
        iphi = 72
    if phi > 0 and phi <= 5:
        iphi = 1
    if phi > 5 and phi <= 10:
        iphi = 2
    if phi > 10 and phi <= 15:
        iphi = 3
    if phi > 15 and phi <= 20:
        iphi = 4
        
    ieta = -20 #array machen
    if thDigi is not None:
        ieta = -19
        for pos in xrange(8):
            if thDigi.code(pos) > 0:
                if thDigi.whNum() == 0 and thDigi.scNum() == 1 and thDigi.stNum() == 2:
                    ieta = pos - 3
                    ieta = -1*ieta

    print 'Muon expected at phi: ', str(iphi), ' eta: ', str(ieta) 
    for i in range(hoEntries.size()):
        bg = hoEntries.__getitem__(i)
        if bg.energy() > .2:
            detId = bg.id()
            if detId.iphi() == iphi:
                testEta = detId.ieta()
                if testEta > 0:
                    testEta = testEta-1
                if testEta == ieta:
                    qualityCodes2d.Fill(0,0)
                    return 40
                if testEta == ieta - 1:
                    qualityCodes2d.Fill(-1,0)
                    return 30
                if testEta == ieta + 1:
                    qualityCodes2d.Fill(1,0)
                    return 30
                for j in range(-4,4):
                    if testEta == j:
                        qualityCodes2d.Fill(testEta-ieta, 0)
                        return 20
                if ieta == -20: #Falls keine info fuer eta da ist
                    qualityCodes2d.Fill(-10, 0)
                    return 10
            for xphi in xrange(3):
                nphi = (((detId.iphi()-1) + 72 - 1 + xphi)%72) + 1
                if nphi == iphi:
                    testEta = detId.ieta()
                    if testEta > 0:
                        testEta = testEta-1
                    if testEta == ieta:
                        qualityCodes2d.Fill(0 , xphi-1)
                        return 3
                    if testEta == ieta - 1:
                        qualityCodes2d.Fill(-1, xphi-1)
                        return 2
                    if testEta == ieta + 1:
                        qualityCodes2d.Fill(1, xphi-1)
                        return 2
                    for j in range(-4,4):
                        if testEta == j:
                            qualityCodes2d.Fill(testEta-ieta, xphi-1)
                            return 1
                    if ieta == -20: #Falls keine info fuer eta da ist
                        qualityCodes2d.Fill(-10, xphi-1)
                        return 0
                
    return -1

    # Falls ieta == -20, dann gibt es keinen eta eintrag
    # Falls vorhanden gucke in iphi und ieta im intervall 3 nach einem eintrag ueber threshold
    # Falls nicht, gucke in iphi und komplett eta
    # Checks if phDigi matches to an ok HO entry
    
def getPtFromDigi(phDigi, stNum): #DONE
    # Return pT from digi
    # Use fit parameters from Dropbox/Promotion/CMS/Analyse/DTAngle/Script.c
    if stNum==2 :
        p0 = 8.00605e-1
        p1 = 1.84458
        p2 = 1.71943e-2
        n0 = -7.91097e-1
        n1 = 1.89551
        n2 = -1.75413e-2
    else:
        return 0
    phiB = phDigi.phiB()/512.
    if phiB < 0:
        return abs(n0/(phiB-n2)+n1)
    else:
        return abs(p0/(phiB-p2)+p1)
    
    
def getPhiFromDigi(phDigi, stNum):
    return -1.*phDigi.phi()/4096.
    # Return phi from digi
    # Perhaps correct for bending
    
def getEtaFromDigi(thDigi, stNum): # How to calculate?
    for pos in xrange(8):
         if thDigi.code(pos) > 0:
             if stNum == 2:
                 return Utils.getEta(4.645, (.32*pos) - 1.12)
    return 0
             
    # Return eta from digi
    # (give eta at the middle of station if no eta available)
    
def getMuonCandidates(phDigi, thDigi, hoEntries, qualityCodes2d): #DONE
    stNum = 2
    candidates = []
    # look for phi and theta and match to phi eta tile of ho. add to list of candidates if ho gives signal
    for dP in phDigi:
        if not dP.stNum() == 2:
#             print 'Station is ', str(dP.stNum()), ' ... continue'
            continue
        if not dP.scNum() == 1:
#             print 'Sector is ', str(dP.scNum()), ' ... continue'
            continue
        if not dP.whNum() == 0:
#             print 'Wheel is ', str(dP.whNum()), ' ... continue'
            continue
        hasThDigi = False
        for dT in thDigi:
            if dP.stNum() == dT.stNum() and dP.scNum() == dT.scNum() and dP.whNum() == dT.whNum():
                    # Here we have high quality and check for HO in eta and phi
                hasThDigi = True
                quality = matchesHO(dP, dT, hoEntries, qualityCodes2d)
                if quality >= 0:
                        candidates.append(HOMuon(-1.*getEtaFromDigi(dT, stNum), getPhiFromDigi(dP, stNum), getPtFromDigi(dP, stNum), quality))
        if hasThDigi == False:
            quality = matchesHO(dP, None, hoEntries, qualityCodes2d)
            if quality >= 0:
                candidates.append(HOMuon(0, getPhiFromDigi(dP, stNum), -1*getPtFromDigi(dP, stNum), quality))
    return candidates



def analyze(deltaR, relPt):
    # deltaR: DeltaR of the matching cone
    # relPt: allowed relative pT deviation (1 = no deviation, 0 = infinit deviation)
    eventsBad.toBegin()
    eventsGood.toBegin()
    
    eventsGood_iter = eventsGood.__iter__()
    eventsBad_iter = eventsBad.__iter__()
    
    ROOT.gROOT.SetStyle('Plain') # white background
    
    
    ##    PLOTS   ##
    # Only RECO working / L1 working
    qualityCodes = ROOT.TH1D("QualityCodes", "QualityCodes", 100, -1.5, 98.5)
    qualityCodes2d = ROOT.TH2D("Quality Codes 2D", "Quality Codes 2D", 20, -10.5, 9.5, 10, -5.5, 4.5)
    realPtVsL1Pt = ROOT.TH2D("Real Pt vs L1 HO Pt", "Real Pt vs L1 HO Pt", 100, 0, 500, 100, 0, 500)
    realPhiVsL1Phi = ROOT.TH2D("Real Phi vs L1 HO Pt", "Real Phi vs L1 HO Pt", 100, -.5, .5, 100, -.5, .5)
    realEtaVsL1Eta = ROOT.TH2D("Real Eta vs L1 HO Pt", "Real Eta vs L1 HO Pt", 100, -.5, .5, 100, -.5, .5)
    
    
    
    
    
    
    allRecoMuonsPt = ROOT.TH1D ("Pt of all RECO muons", "Pt of all RECO muons", 1000, 0, 100)
    allRecoMuons = ROOT.TH2D("Eta phi of all RECO muons / good detector", "Eta phi of all RECO muons / good detector", 30, -1.*Utils.getEta(4.02, 6.61), Utils.getEta(4.02, 6.61), 72, -1*math.pi, math.pi)
    
    allWorkingRecoMuonsPt = ROOT.TH1D ("Pt of all working RECO muons with L1 match working", "Pt of all working RECO muons with L1 match working", 1000, 0, 100)
    allWorkingRecoMuons = ROOT.TH2D("Eta phi of all RECO muons with l1 muons match/ good detector", "Eta phi of all RECO muons with l1 muons match / good detector", 30, -1.*Utils.getEta(4.02, 6.61), Utils.getEta(4.02, 6.61), 72, -1*math.pi, math.pi)
    
    allNonWorkingRecoMuonsGoodPt = ROOT.TH1D ("Pt of all non working RECO muons with L1 match good", "Pt of all non working RECO muons with L1 match good", 1000, 0, 100)
    allNonWorkingRecoMuonsGood = ROOT.TH2D("Eta phi of not matching Reco muons to l1 muons / good detector", "Eta phi of not matching Reco muons to l1 muons / good detector", 30, -1.*Utils.getEta(4.02, 6.61), Utils.getEta(4.02, 6.61), 72, -1*math.pi, math.pi)
    # Only RECO non working / L1 non working
    
    
    # Only RECO working / L1 non working
    allNonWorkingRecoMuonsBadPt = ROOT.TH1D ("Pt of all non working RECO muons with L1 match bad", "Pt of all non working RECO muons with L1 match bad", 1000, 0, 100)
    allNonWorkingRecoMuonsBad = ROOT.TH2D("Eta phi of not matching Reco muons to l1 muons / bad detector", "Eta phi of not matching Reco muons to l1 muons / bad detector", 30, -1.*Utils.getEta(4.02, 6.61), Utils.getEta(4.02, 6.61), 72, -1*math.pi, math.pi)
    
    #Mixed
    diffFailsEtaPhi = ROOT.TH2D("Number of additional fails", "Number of additional fails", 30, -1.*Utils.getEta(4.02, 6.61), Utils.getEta(4.02, 6.61), 72, -1*math.pi, math.pi)
    diffGhostsEtaPhi = ROOT.TH2D("Number of additional ghosts", "Number of additional ghosts", 30, -1.*Utils.getEta(4.02, 6.61), Utils.getEta(4.02, 6.61), 72, -1*math.pi, math.pi)
    hoEntryPlot = ROOT.TH1D ("HoEnergyInNonWorking", "HoEnergyInNonWorking", 800, 0, 8)
    hoEntryPlot3Phi = ROOT.TH1D ("HoEnergyInNonWorking3Phi", "HoEnergyInNonWorking3Phi", 800, 0, 8)
    
    #Controll plots
    YGoodYBadPt = ROOT.TH1D ("YGYB Pt", "YGYB Pt", 1000, 0, 100)
    NGoodYBadPt = ROOT.TH1D ("NGYB Pt", "NGYB Pt", 1000, 0, 100)
    YGoodNBadPt = ROOT.TH1D ("YGNB Pt", "YGNB Pt", 1000, 0, 100)
    NGoodNBadPt = ROOT.TH1D ("NGNB Pt", "NGNB Pt", 1000, 0, 100)
    
    YGoodYBadPtGen = ROOT.TH1D ("YGYB Pt Gen", "YGYB Pt Gen", 1000, 0, 100)
    NGoodYBadPtGen = ROOT.TH1D ("NGYB Pt Gen", "NGYB Pt Gen", 1000, 0, 100)
    YGoodNBadPtGen = ROOT.TH1D ("YGNB Pt Gen", "YGNB Pt Gen", 1000, 0, 100)
    NGoodNBadPtGen = ROOT.TH1D ("NGNB Pt Gen", "NGNB Pt Gen", 1000, 0, 100)
    
    ### COUNTER ##
    
    numberOfAdditionals = 0
    numberOfHighHOEntries = 0
    numberOfHighHOEntries3Phi = 0
    
    numberOfNonGoodNonBad = 0
    numberOfNonGoodBad = 0
    numberOfGoodNonBad = 0
    numberOfGoodBad = 0
    numberOfNonGoodNonBadGen = 0
    numberOfNonGoodBadGen = 0
    numberOfGoodNonBadGen = 0
    numberOfGoodBadGen = 0
    
    numberOfFails = 0
    numberOfRecoveries = 0
    
    
    
    for i in xrange(MAX_NUMBER):
        # GET THE EVENTS
        badEvent = eventsBad_iter.next()
        goodEvent = eventsGood_iter.next()
        
        # GET THE HANDLES
        badEvent.getByLabel(label,badMuonsHandle)
        badRecoMuons = badMuonsHandle.product()
    
        goodEvent.getByLabel(labelGenParticles, genParticlesHandle)
        genParticles = genParticlesHandle.product()
        
        badEvent.getByLabel(labelL1, badL1MuonsHandle)
        badL1Muons = badL1MuonsHandle.product()
        
        goodEvent.getByLabel(label,goodMuonsHandle)
        goodRecoMuons = goodMuonsHandle.product()

        goodEvent.getByLabel(labelL1, goodL1MuonsHandle)
        goodL1Muons = goodL1MuonsHandle.product()
        
        badEvent.getByLabel(labelHoEntries, hoEntriesHandle)
        badHoEntries = hoEntriesHandle.product()
    
        badEvent.getByLabel(labelPhiContainer, phiContainerHandle)
        phiContainer = phiContainerHandle.product()
        #----- END GET THE HANDLES -----
        badEvent.getByLabel(labelPhiContainer, phiContainerHandle)
        phiContainer = phiContainerHandle.product()
        #----- END GET THE HANDLES -----
        phiDigis = phiContainer.getContainer()
        
        
        badEvent.getByLabel(labelThContainer, thContainerHandle)
        thContainer = thContainerHandle.product()
        #----- END GET THE HANDLES -----
        thDigis = thContainer.getContainer()
        
        
        
        l1MuonTuple = []
        
        recoMuon = 0
        matchingBadMuon = 1 #L1Muon
        matchingGoodMuon = 2 #L1Muon
        
        matchedToGenRecoMuon = Utils.getMatch(genParticles[0], goodRecoMuons, .1, .7)
        #print matchedToGenRecoMuon, " Matched to"
        
        for element in goodRecoMuons:
            if Utils.isInRange(element):
                thisTuple = [element, Utils.getMatch(element, badL1Muons, deltaR, relPt), Utils.getMatch(element, goodL1Muons, deltaR, relPt)]
                l1MuonTuple.append(thisTuple)
    
        for j in range(len(l1MuonTuple)):
            element = l1MuonTuple[j]
            if not element[matchingGoodMuon] == None:
                if element[matchingBadMuon] == None:
                    if abs(element[recoMuon].eta()) < Utils.getEta(4.645, 1.28):
                        if element[recoMuon].phi() >= -10.*math.pi/180. and element[recoMuon].phi() < 20./180.*math.pi:
                            numberOfFails = numberOfFails + 1
                            print 'Event ' + str(i) + ', RECO (gen), pT: ', str(element[recoMuon].pt()), ' eta: ', str(element[recoMuon].eta()), 'phi ', str(element[recoMuon].phi())
                            printDigis(phiDigis, thDigis)
                            candidates = getMuonCandidates(phiDigis, thDigis, badHoEntries, qualityCodes2d)
                            for c in candidates:
                                c.printInfo()
                                qualityCodes.Fill(c.quality)
                                realPtVsL1Pt.Fill(element[recoMuon].pt(), c.pt)
                                realPhiVsL1Phi.Fill(element[recoMuon].phi(), c.phi)
                                realEtaVsL1Eta.Fill(element[recoMuon].eta(), c.eta)
                                numberOfRecoveries = numberOfRecoveries + 1
                            if not candidates:
                                qualityCodes.Fill(-1)
                            print '--------------------------- '
                    
                    # Here we have the muons that are detected in L1 for the working detector, but are not detected in the non working detector anymore
                    # element[recoMuon] is the corresponding RECO muon (meaning the 'GEN' muon)
    print 'Number of additional fails: ', str(numberOfFails)
    print 'Number of recoveries : ' , str(numberOfRecoveries)
    save('Quality.root', qualityCodes, realPtVsL1Pt, realPhiVsL1Phi, realEtaVsL1Eta, qualityCodes2d)
#for i in xrange(100):
analyze(.2, .5)

#save('Data.root', deltaZ)
