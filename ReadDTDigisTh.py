import ROOT
import math
from DataFormats.FWLite import Events, Handle
from Utils import *

MAX_NUMBER = 600000

eventsFile = Events ('SingleMuonGunPlusMinus.root')

# create handle outside of loop
genParticlesHandle  = Handle ('std::vector<reco::GenParticle>')
goodMuonsHandle  = Handle ('std::vector<reco::Muon>')
badMuonsHandle = Handle('std::vector<reco::Muon>')
badL1MuonsHandle = Handle('std::vector<l1extra::L1MuonParticle>')
goodL1MuonsHandle = Handle('std::vector<l1extra::L1MuonParticle>')
hoEntriesHandle = Handle('edm::SortedCollection<HORecHit,edm::StrictWeakOrdering<HORecHit>>')
phiContainerHandle = Handle('L1MuDTChambThContainer')
#phiContainerHandle = Handle('L1MuDTChambPhContainer')
# a label is just a tuple of strings that is initialized justvector<reco::GenParticle>
# like and edm::InputTag
label = ("muons")
labelL1 = ("l1extraParticles")
labelHoEntries = ("horeco")
labelPhiContainer = ("dttfDigis")
labelGenParticles = ("genParticles")

#print Utils.getEta(4.02, 6.61) #Straight line from center to end of station 1 in wheel 2
#print Utils.getEta(7.38, 6.61) #Straight line from center to end of station 4 in wheel 2
#print Utils.getEta(4.02, 3.954) #Straight line from center to end of station 1 wheel 1
#print Utils.getEta(4.02, 1.268) #Straight line from center to end of station 1 in wheel 0
#print 2**.5*math.pi/36

angleSubtractedVsPT1 = ROOT.TH2D("PhiB - Phi vs pt at station 1", "PhiB - Phi vs pt at station 1", 1000, -1, 1, 95, 5, 100)
angleSubtractedVsPT2 = ROOT.TH2D("PhiB - Phi vs pt at station 2", "PhiB - Phi vs pt at station 2", 1000, -1, 1, 95, 5, 100)
angleSubtractedVsPT3 = ROOT.TH2D("PhiB - Phi vs pt at station 3", "PhiB - Phi vs pt at station 3", 1000, -1, 1, 95, 5, 100)
angleSubtractedVsPT4 = ROOT.TH2D("PhiB - Phi vs pt at station 4", "PhiB - Phi vs pt at station 4", 1000, -1, 1, 95, 5, 100)

bendingAngleVsAngle90GeV1 = ROOT.TH2D("Bending angle vs. entrance angle for muon pT > 90 GeV Station 1", "Bending angle vs. entrance angle for muon pT > 90 GeV Station 1", 2048, -600, 1447, 512, -255, 256)
bendingAngleVsAngle90GeV2 = ROOT.TH2D("Bending angle vs. entrance angle for muon pT > 90 GeV Station 2", "Bending angle vs. entrance angle for muon pT > 90 GeV Station 2", 2048, -600, 1447, 512, -255, 256)
bendingAngleVsAngle90GeV3 = ROOT.TH2D("Bending angle vs. entrance angle for muon pT > 90 GeV Station 3", "Bending angle vs. entrance angle for muon pT > 90 GeV Station 3", 2048, -600, 1447, 512, -255, 256)
bendingAngleVsAngle90GeV4 = ROOT.TH2D("Bending angle vs. entrance angle for muon pT > 90 GeV Station 4", "Bending angle vs. entrance angle for muon pT > 90 GeV Station 4", 2048, -600, 1447, 512, -255, 256)

ietaVsAngle1HLT = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 1 HLT", "Direction angle vs. iphi of highest HO entry 1 HLT", 19, -4, 14, 17, -8.5, 8.5)

ietaVsAngle1 = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 1", "Direction angle vs. iphi of highest HO entry 1", 19, -4, 14, 17, -8.5, 8.5)
iphiVsAngle2 = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 2", "Direction angle vs. iphi of highest HO entry 2", 400, -20, 80, 72, .5, 72.5)
iphiVsAngle3 = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 3", "Direction angle vs. iphi of highest HO entry 3", 400, -20, 80, 72, .5, 72.5)
iphiVsAngle4 = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 4", "Direction angle vs. iphi of highest HO entry 4", 400, -20, 80, 72, .5, 72.5)

iphiVsAngle1Threshold = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 1 > 0.2 GeV", "Direction angle vs. iphi of highest HO entry 1 > 0.2 GeV", 400, -20, 80, 72, .5, 72.5)
iphiVsAngle2Threshold = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 2 > 0.2 GeV", "Direction angle vs. iphi of highest HO entry 2 > 0.2 GeV", 400, -20, 80, 72, .5, 72.5)
iphiVsAngle3Threshold = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 3 > 0.2 GeV", "Direction angle vs. iphi of highest HO entry 3 > 0.2 GeV", 400, -20, 80, 72, .5, 72.5)
iphiVsAngle4Threshold = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 4 > 0.2 GeV", "Direction angle vs. iphi of highest HO entry 4 > 0.2 GeV", 400, -20, 80, 72, .5, 72.5)

iphiVsPos1 = ROOT.TH2D("Direction pos vs. iphi of highest HO entry 1", "Direction pos vs. iphi of highest HO entry 1", 400, -20, 80, 72, .5, 72.5)
iphiVsPos2 = ROOT.TH2D("Direction pos vs. iphi of highest HO entry 2", "Direction pos vs. iphi of highest HO entry 2", 400, -20, 80, 72, .5, 72.5)
iphiVsPos3 = ROOT.TH2D("Direction pos vs. iphi of highest HO entry 3", "Direction pos vs. iphi of highest HO entry 3", 400, -20, 80, 72, .5, 72.5)
iphiVsPos4 = ROOT.TH2D("Direction pos vs. iphi of highest HO entry 4", "Direction pos vs. iphi of highest HO entry 4", 400, -20, 80, 72, .5, 72.5)

iphiVsPos1Threshold = ROOT.TH2D("Direction pos vs. iphi of highest HO entry 1 > 0.2 GeV", "Direction pos vs. iphi of highest HO entry 1 > 0.2 GeV", 400, -20, 80, 72, .5, 72.5)
iphiVsPos2Threshold = ROOT.TH2D("Direction pos vs. iphi of highest HO entry 2 > 0.2 GeV", "Direction pos vs. iphi of highest HO entry 2 > 0.2 GeV", 400, -20, 80, 72, .5, 72.5)
iphiVsPos3Threshold = ROOT.TH2D("Direction pos vs. iphi of highest HO entry 3 > 0.2 GeV", "Direction pos vs. iphi of highest HO entry 3 > 0.2 GeV", 400, -20, 80, 72, .5, 72.5)
iphiVsPos4Threshold = ROOT.TH2D("Direction pos vs. iphi of highest HO entry 4 > 0.2 GeV", "Direction pos vs. iphi of highest HO entry 4 > 0.2 GeV", 400, -20, 80, 72, .5, 72.5)

def save(name, *plot):
    file = ROOT.TFile(name, 'RECREATE')
    for x in plot:
        x.Write()
    file.Close()

x = ROOT.TVectorD()
y = ROOT.TVectorD()
angleSubtractedVsPT1Graph = ROOT.TGraph()

def analyze(deltaR, relPt):
    
    # deltaR: DeltaR of the matching cone
    # relPt: allowed relative pT deviation (1 = no deviation, 0 = infinit deviation)
    eventsFile.toBegin()
    
    events_iter = eventsFile.__iter__()
    
    ROOT.gROOT.SetStyle('Plain') # white background
    
    
    ##    PLOTS   ##
    
    
  
    ### COUNTER ##
    
    for i in xrange(MAX_NUMBER):
        print 'Nr. ', i
        # GET THE EVENTS
        event = events_iter.next()
        
        # GET THE HANDLES
        event.getByLabel(label,badMuonsHandle)
        badRecoMuons = badMuonsHandle.product()
    
        event.getByLabel(labelGenParticles, genParticlesHandle)
        genParticles = genParticlesHandle.product()
        
        event.getByLabel(labelL1, badL1MuonsHandle)
        badL1Muons = badL1MuonsHandle.product()
        
        event.getByLabel(labelHoEntries, hoEntriesHandle)
        badHoEntries = hoEntriesHandle.product()
    
        event.getByLabel(labelPhiContainer, phiContainerHandle)
        thContainer = phiContainerHandle.product()
        #----- END GET THE HANDLES -----
        
        digis = thContainer.getContainer();
        #if genParticles.at(0).pt() > 10:
        #    continue
    
        if badHoEntries.size() > 0:
            highestHoEntry = badHoEntries.__getitem__(0)
            for i in xrange (0, badHoEntries.size()):
                if badHoEntries.__getitem__(i).energy() > highestHoEntry.energy():
                    highestHoEntry = badHoEntries.__getitem__(i)
                    
        id = highestHoEntry.id()
        
        
        
        for d in digis:
            for pos in xrange(8):
                if d.stNum() > 1:
                    continue
                if not d.scNum() == 0:
                    continue
                if d.position(pos) > 0:
                    if d.whNum() == 0:
                        ietaVsAngle1.Fill(pos, id.ieta())
                    if d.whNum() == 1:
                        ietaVsAngle1.Fill(7-pos+8, id.ieta())
                    if d.whNum() == -1:
                        ietaVsAngle1.Fill(pos-8, id.ieta())
                    if d.code(pos) == 2:
                        if d.whNum() == 0:
                            ietaVsAngle1HLT.Fill(pos, id.ieta())
                        if d.whNum() == 1:
                            ietaVsAngle1HLT.Fill(7-pos+8, id.ieta())
                        if d.whNum() == -1:
                            ietaVsAngle1HLT.Fill(pos-8, id.ieta())



#for i in xrange(100):
analyze(.2, .5)


#save('Data.root', deltaZ)
save('DTDigiDataAngleTh.root', bendingAngleVsAngle90GeV1, bendingAngleVsAngle90GeV2, bendingAngleVsAngle90GeV3, bendingAngleVsAngle90GeV4, angleSubtractedVsPT1, angleSubtractedVsPT2, angleSubtractedVsPT3, angleSubtractedVsPT4, angleSubtractedVsPT1Graph, ietaVsAngle1, iphiVsAngle2, iphiVsAngle3, iphiVsAngle4, iphiVsAngle1Threshold, iphiVsAngle2Threshold, iphiVsAngle3Threshold, iphiVsAngle4Threshold, iphiVsPos1Threshold, iphiVsPos2Threshold, iphiVsPos3Threshold, iphiVsPos4Threshold, iphiVsPos1, iphiVsPos2, iphiVsPos3, iphiVsPos4, ietaVsAngle1HLT)