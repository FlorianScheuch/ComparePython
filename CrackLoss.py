import ROOT
import math
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from PhysicsTools.PythonAnalysis.cmstools import *
from ROOT import *
from Utils import *
from HOMuon import *
import os
import thread
import threading
import subprocess
import sys
from sys import argv

cmstools.ROOT.gSystem.Load("libFWCoreFWLite.so")
cmstools.ROOT.AutoLibraryLoader.enable()
MAX_NUMBER = 1000 #Events per file
stNum=1
isGetHighestCandidate = 0
download = False
stopped = 0
fileList = []
startNumber = 1
currentEndNumber = startNumber-1
endNumber = 100

nothing, startNumber, endNumber = argv
startNumber = int(startNumber)
endNumber = int(endNumber)
currentEndNumber = startNumber-1

for i in range(startNumber, endNumber+1): # 1,51 101
#    fileList.append(['dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/FailureSamples/Working2/FEVT_WorkingDetector'+str(i)+'.root', 'dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/FailureSamples/NonWorking2/FEVT_NonWorkingDetector'+str(i)+'.root'])
    fileList.append('dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/Analysis/Wheel2M/Working/Working'+str(i)+'.root')
    fileList.append('dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/Analysis/Wheel1M/Working/Working'+str(i)+'.root')
    fileList.append('dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/Analysis/Wheel0/Working/Working'+str(i)+'.root')

# create handle outside of loop
genParticlesHandle  = Handle ('std::vector<reco::GenParticle>')
goodMuonsHandle  = Handle ('std::vector<reco::Muon>')
badMuonsHandle = Handle('std::vector<reco::Muon>')
badL1MuonsHandle = Handle('std::vector<l1extra::L1MuonParticle>')
goodL1MuonsHandle = Handle('std::vector<l1extra::L1MuonParticle>')
hoEntriesHandle = Handle('edm::SortedCollection<HORecHit,edm::StrictWeakOrdering<HORecHit>>')
phiContainerHandle = Handle('L1MuDTChambPhContainer')
phiPrimitiveContainerHandle = Handle('L1MuDTChambPhContainer')
thContainerHandle = Handle('L1MuDTChambThContainer')
jetContainerHandle = Handle('std::vector<l1extra::L1JetParticle>')
pfJetContainerHandle = Handle('std::vector<reco::PFJet>')
pfCandidateHandle = Handle('vector<reco::PFCandidate>')
rpcDigiContainerHandle = Handle('vector<L1MuRegionalCand>')
#phiContainerHandle = Handle('L1MuDTChambPhContainer')
# a label is just a tuple of strings that is initialized justvector<reco::GenParticle>
# like and edm::InputTag
label = ("muons")
labelL1 = ("l1extraParticles")
labelHoEntries = ("horeco")
labelPhiContainer = ("dttfDigis")
labelPhiPrimitiveContainer = ("simDtTriggerPrimitiveDigis")
labelThContainer = ("dttfDigis")
labelGenParticles = ("genParticles")
labelJetContainer = ("l1extraParticles", "Central", "HLT") #, "Central", "HLT"
labelPfJetContainer = ('ak5PFJets')
labelPfCandidate = ('particleFlow')
#labelRpcDigiContainer = ("gtDigis", "RPCb", "HLT") #, "Central", "HLT

#print Utils.getEta(4.02, 6.61) #Straight line from center to end of station 1 in wheel 2
#print Utils.getEta(7.38, 6.61) #Straight line from center to end of station 4 in wheel 2
#print Utils.getEta(4.02, 3.954) #Straight line from center to end of station 1 wheel 1
#print Utils.getEta(4.02, 1.268) #Straight line from center to end of station 1 in wheel 0
# print Utils.getEta(4.645, 1.28)
#print 2**.5*math.pi/36

def analyze(deltaR, relPt, stNum, download):
     global currentEndNumber
     ROOT.gROOT.SetStyle('Plain') # white background
     
     
     etaOfAllGenMuons = ROOT.TH1D("Eta of all GEN muons", "Eta of all GEN muons", 1000, -2, 2)
     etaOfAllGenMuonsDtOnly  = ROOT.TH1D("Eta of DT only GEN muons", "Eta of DT only GEN muons", 1000, -2, 2)
     etaOfNotMatchingGenMuons = ROOT.TH1D("Eta of not matching GEN muons", "Eta of not matching GEN muons", 1000, -2, 2)
     
     for f in range(len(fileList)):
        print str(fileList[f])
        
        events = Events(fileList[f])
        events.toBegin()
        events_iter = events.__iter__()
        
        for i in xrange(MAX_NUMBER):
            event = events_iter.next()
            
            # GEN muons
            event.getByLabel(labelGenParticles, genParticlesHandle)
            genParticles = genParticlesHandle.product()
            
            event.getByLabel(labelL1, goodL1MuonsHandle)
            l1Muons = goodL1MuonsHandle.product()
            
            l1MuonTuple = []
            genMuon = 0
            matchingL1Muon = 1
            
            for element in genParticles:
                thisTuple = [element, Utils.getMatch(element, l1Muons, deltaR, relPt)]
                l1MuonTuple.append(thisTuple)
                
            for j in range(len(l1MuonTuple)):
                element = l1MuonTuple[j]
                etaOfAllGenMuons.Fill(element[genMuon].eta())
                if element[matchingL1Muon] == None:
                    if not element[genMuon] == None:
                        # Inefficiency
                        etaOfNotMatchingGenMuons.Fill(element[genMuon].eta())
                else:
                    if not element[matchingL1Muon].isRPC():
                        etaOfAllGenMuonsDtOnly.Fill(element[genMuon].eta())
        currentEndNumber = currentEndNumber + f%3
        
     Utils.save('CrackLoss_' + str(startNumber) + '_' + str(currentEndNumber) + '.root', etaOfAllGenMuons, etaOfAllGenMuonsDtOnly, etaOfNotMatchingGenMuons)
analyze(.3, .6, 1, 0)