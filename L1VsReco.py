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
L1PtVsGenPt = ROOT.TH2D("L1 Pt vs GEN Pt", "L1 Pt vs GEN Pt", 1000, 0, 1000, 1000, 0, 1000)


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
    
        for i in xrange(badL1Muons.size()):
            L1PtVsGenPt.Fill(badL1Muons.at(i).pt(),genParticles.at(0).pt())
        



#for i in xrange(100):
analyze(.2, .5)


#save('Data.root', deltaZ)
save('L1PtVsGenPt.root', L1PtVsGenPt)