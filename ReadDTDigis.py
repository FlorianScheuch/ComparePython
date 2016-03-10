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
phiContainerHandle = Handle('L1MuDTChambPhContainer')
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

angleGenVsEntranceAngle1 = ROOT.TH2D("GenAngle vs entrance angle station 1", "GenAngle vs entrance angle station 1", 629, -3.14, 3.14, 629, -3.14, 3.14)
angleGenVsEntranceAngle2 = ROOT.TH2D("GenAngle vs entrance angle station 2", "GenAngle vs entrance angle station 2", 629, -3.14, 3.14, 629, -3.14, 3.14)
angleGenVsEntranceAngle3 = ROOT.TH2D("GenAngle vs entrance angle station 3", "GenAngle vs entrance angle station 3", 629, -3.14, 3.14, 629, -3.14, 3.14)
angleGenVsEntranceAngle4 = ROOT.TH2D("GenAngle vs entrance angle station 4", "GenAngle vs entrance angle station 4", 629, -3.14, 3.14, 629, -3.14, 3.14)

angleGenVsEntranceAnglePlusBendingAngle1 = ROOT.TH2D("GenAngle vs entrance angle PlusBendingAnglestation 1", "GenAngle vs entrance angle PlusBendingAnglestation 1", 629, -3.14, 3.14, 629, -3.14, 3.14)
angleGenVsEntranceAnglePlusBendingAngle2 = ROOT.TH2D("GenAngle vs entrance angle PlusBendingAnglestation 2", "GenAngle vs entrance angle PlusBendingAnglestation 2", 629, -3.14, 3.14, 629, -3.14, 3.14)
angleGenVsEntranceAnglePlusBendingAngle3 = ROOT.TH2D("GenAngle vs entrance angle PlusBendingAnglestation 3", "GenAngle vs entrance angle PlusBendingAnglestation 3", 629, -3.14, 3.14, 629, -3.14, 3.14)
angleGenVsEntranceAnglePlusBendingAngle4 = ROOT.TH2D("GenAngle vs entrance angle PlusBendingAnglestation 4", "GenAngle vs entrance angle PlusBendingAnglestation 4", 629, -3.14, 3.14, 629, -3.14, 3.14)

bendingAngleVsAngle90GeV1 = ROOT.TH2D("Bending angle vs. entrance angle for muon pT > 90 GeV Station 1", "Bending angle vs. entrance angle for muon pT > 90 GeV Station 1", 2048, -600, 1447, 512, -255, 256)
bendingAngleVsAngle90GeV2 = ROOT.TH2D("Bending angle vs. entrance angle for muon pT > 90 GeV Station 2", "Bending angle vs. entrance angle for muon pT > 90 GeV Station 2", 2048, -600, 1447, 512, -255, 256)
bendingAngleVsAngle90GeV3 = ROOT.TH2D("Bending angle vs. entrance angle for muon pT > 90 GeV Station 3", "Bending angle vs. entrance angle for muon pT > 90 GeV Station 3", 2048, -600, 1447, 512, -255, 256)
bendingAngleVsAngle90GeV4 = ROOT.TH2D("Bending angle vs. entrance angle for muon pT > 90 GeV Station 4", "Bending angle vs. entrance angle for muon pT > 90 GeV Station 4", 2048, -600, 1447, 512, -255, 256)

iphiVsAngle1 = ROOT.TH2D("Direction angle vs. iphi of highest HO entry 1", "Direction angle vs. iphi of highest HO entry 1", 400, -20, 80, 72, .5, 72.5)
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
        phiContainer = phiContainerHandle.product()
        #----- END GET THE HANDLES -----
        
        digis = phiContainer.getContainer()
        
        #if genParticles.at(0).pt() > 10:
        #    continue
    
        if badHoEntries.size() > 0:
            highestHoEntry = badHoEntries.__getitem__(0)
            for i in xrange (0, badHoEntries.size()):
                if badHoEntries.__getitem__(i).energy() > highestHoEntry.energy():
                    highestHoEntry = badHoEntries.__getitem__(i)
                    
        id = highestHoEntry.id()
        
        for d in digis:
            if d.stNum() == 1:
                if genParticles.at(0).pt() > 90:
                    bendingAngleVsAngle90GeV1.Fill(d.phi(), d.phiB())
                #Utils.getNewAngle(d)
                angleGenVsEntranceAngle1.Fill(genParticles.at(0).phi(), d.phi()/2048.)
                angleGenVsEntranceAnglePlusBendingAngle1.Fill(genParticles.at(0).phi(), d.phi()/2048.+d.phiB()/512.)
                angleSubtractedVsPT1.Fill(d.phiB()/512., genParticles.at(0).pt())
                angleSubtractedVsPT1Graph.SetPoint(i,d.phiB()/512., genParticles.at(0).pt())
                iphiVsAngle1.Fill(Utils.getTrigDir(d), id.iphi())
                iphiVsPos1.Fill(Utils.getTrigPos(d), id.iphi())
                if highestHoEntry.energy() > .2:
                    iphiVsAngle1Threshold.Fill(Utils.getTrigDir(d), id.iphi())
                    iphiVsPos1Threshold.Fill(Utils.getTrigPos(d), id.iphi())
            if d.stNum() == 2:
                if genParticles.at(0).pt() > 90:
                    bendingAngleVsAngle90GeV2.Fill(d.phi(), d.phiB())
                angleSubtractedVsPT2.Fill(d.phiB()/512., genParticles.at(0).pt())
                angleGenVsEntranceAnglePlusBendingAngle2.Fill(genParticles.at(0).phi(), d.phi()/2048.+d.phiB()/512.)
                angleGenVsEntranceAngle2.Fill(genParticles.at(0).phi(), d.phi()/2048.)
                iphiVsAngle2.Fill(Utils.getTrigDir(d), id.iphi())
                iphiVsPos2.Fill(Utils.getTrigPos(d), id.iphi())
                if highestHoEntry.energy() > .2:
                    iphiVsAngle2Threshold.Fill(Utils.getTrigDir(d), id.iphi())
                    iphiVsPos2Threshold.Fill(Utils.getTrigPos(d), id.iphi())
            if d.stNum() == 3:
                if genParticles.at(0).pt() > 90:
                    bendingAngleVsAngle90GeV3.Fill(d.phi(), d.phiB())
                angleSubtractedVsPT3.Fill(d.phiB()/512., genParticles.at(0).pt())
                angleGenVsEntranceAnglePlusBendingAngle3.Fill(genParticles.at(0).phi(), d.phi()/2048.+d.phiB()/512.)
                angleGenVsEntranceAngle3.Fill(genParticles.at(0).phi(), d.phi()/2048.)
                iphiVsAngle3.Fill(Utils.getTrigDir(d), id.iphi())
                iphiVsPos3.Fill(Utils.getTrigPos(d), id.iphi())
                if highestHoEntry.energy() > .2:
                    iphiVsAngle3Threshold.Fill(Utils.getTrigDir(d), id.iphi())
                    iphiVsPos3Threshold.Fill(Utils.getTrigPos(d), id.iphi())
            if d.stNum() == 4:
                if genParticles.at(0).pt() > 90:
                    bendingAngleVsAngle90GeV4.Fill(d.phi(), d.phiB())
                angleSubtractedVsPT4.Fill(d.phiB()/512., genParticles.at(0).pt())
                angleGenVsEntranceAnglePlusBendingAngle4.Fill(genParticles.at(0).phi(), d.phi()/2048.+d.phiB()/512.)
                angleGenVsEntranceAngle4.Fill(genParticles.at(0).phi(), d.phi()/2048.)
                iphiVsAngle4.Fill(Utils.getTrigDir(d), id.iphi())
                iphiVsPos4.Fill(Utils.getTrigPos(d), id.iphi())
                if highestHoEntry.energy() > .2:
                    iphiVsAngle4Threshold.Fill(Utils.getTrigDir(d), id.iphi())
                    iphiVsPos4Threshold.Fill(Utils.getTrigPos(d), id.iphi())
        



#for i in xrange(100):
analyze(.2, .5)


#save('Data.root', deltaZ)
save('DTDigiDataAngle.root',angleGenVsEntranceAnglePlusBendingAngle1,angleGenVsEntranceAnglePlusBendingAngle2,angleGenVsEntranceAnglePlusBendingAngle3,angleGenVsEntranceAnglePlusBendingAngle4,angleGenVsEntranceAngle1,angleGenVsEntranceAngle2,angleGenVsEntranceAngle3,angleGenVsEntranceAngle4, bendingAngleVsAngle90GeV1, bendingAngleVsAngle90GeV2, bendingAngleVsAngle90GeV3, bendingAngleVsAngle90GeV4, angleSubtractedVsPT1, angleSubtractedVsPT2, angleSubtractedVsPT3, angleSubtractedVsPT4, angleSubtractedVsPT1Graph, iphiVsAngle1, iphiVsAngle2, iphiVsAngle3, iphiVsAngle4, iphiVsAngle1Threshold, iphiVsAngle2Threshold, iphiVsAngle3Threshold, iphiVsAngle4Threshold, iphiVsPos1Threshold, iphiVsPos2Threshold, iphiVsPos3Threshold, iphiVsPos4Threshold, iphiVsPos1, iphiVsPos2, iphiVsPos3, iphiVsPos4)