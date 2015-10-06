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
#from colorama import init, Fore, Back, Style

# voms-proxy-init --voms cms --valid 300:00

cmstools.ROOT.gSystem.Load("libFWCoreFWLite.so")
cmstools.ROOT.AutoLibraryLoader.enable()
MAX_NUMBER = 1000 #Events per file
stNum=1
isGetHighestCandidate = 1
download = False
fileList = []
for i in range(1,151): # 1,51 101
    fileList.append(['FEVT_WorkingDetector'+str(i)+'.root', 'FEVT_NonWorkingDetector'+str(i)+'.root'])
eventList = []



#/pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/FailureSamples/Working2
# uberftp grid-srm "cd /pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/FailureSamples/Working2/; get FEVT_NonWorkingDetector1.root"

# create handle outside of loop
genParticlesHandle  = Handle ('std::vector<reco::GenParticle>')
goodMuonsHandle  = Handle ('std::vector<reco::Muon>')
badMuonsHandle = Handle('std::vector<reco::Muon>')
badL1MuonsHandle = Handle('std::vector<l1extra::L1MuonParticle>')
goodL1MuonsHandle = Handle('std::vector<l1extra::L1MuonParticle>')
hoEntriesHandle = Handle('edm::SortedCollection<HORecHit,edm::StrictWeakOrdering<HORecHit>>')
phiContainerHandle = Handle('L1MuDTChambPhContainer')
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
labelThContainer = ("dttfDigis")
labelGenParticles = ("genParticles")
labelJetContainer = ("l1extraParticles", "Central", "HLT") #, "Central", "HLT"
labelPfJetContainer = ('ak5PFJets')
labelPfCandidate = ('particleFlow')
labelRpcDigiContainer = ("gtDigis", "RPCb", "HLT") #, "Central", "HLT

#print Utils.getEta(4.02, 6.61) #Straight line from center to end of station 1 in wheel 2
#print Utils.getEta(7.38, 6.61) #Straight line from center to end of station 4 in wheel 2
#print Utils.getEta(4.02, 3.954) #Straight line from center to end of station 1 wheel 1
#print Utils.getEta(4.02, 1.268) #Straight line from center to end of station 1 in wheel 0
# print Utils.getEta(4.645, 1.28)
#print 2**.5*math.pi/36


def download(filename, event):
    pr = subprocess.Popen(filename)
    pr.communicate() 
    if pr.returncode == 0:
        event.set()
        print 'Done downloading: ' , filename, ' with exit code ', pr.returncode
    else:
        print 'Error downloading: ' , filename, ' with exit code ', pr.returncode
        
def downloadAll():
    for f in range(len(fileList)):
        print 'Downloading: ' , fileList[f][0]
        download(['uberftp', 'grid-ftp.physik.rwth-aachen.de',r'cd /pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/FailureSamples/Working2/; get '+ fileList[f][0]], eventList[f][0])
        print 'Downloading: ' , fileList[f][1]
        download(['uberftp', 'grid-ftp.physik.rwth-aachen.de',r'cd /pnfs/physik.rwth-aachen.de/cms/store/user/fscheuch/FailureSamples/NonWorking2/; get '+ fileList[f][1]], eventList[f][1])
        # downloaden
        # warten
        # event auf set setzen

def save(name, *plot):
    file = ROOT.TFile(name, 'RECREATE')
    for x in plot:
        x.Write()
    file.Close()

def printDigis(phDigi, thDigi):
    printed = False
    for d in phDigi:
        sc = d.scNum()+1
        #print str(d.stNum()), ' ', str(d.scNum()), ' ', str(d.whNum())
        if d.stNum() == 1 and sc == 1 and d.whNum() == 0:
#             print 'Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
        if d.stNum() == 1 and sc == 12 and d.whNum() == 0:
#             print '####!!!!#### Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
        if d.stNum() == 1 and sc == 2 and d.whNum() == 0:
#             print '####!!!!#### Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
        if d.stNum() == 1 and sc == 1 and d.whNum() == -1:
#             print '####!!!!#### Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
        if d.stNum() == 1 and sc == 1 and d.whNum() == 1:
#             print '####!!!!#### Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
    for d in thDigi:
        sc = d.scNum()+1
        if d.stNum() == 1 and sc == 1 and d.whNum() == 0:
            for pos in xrange(8):
                if d.position(pos) > 0:
#                     print 'Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' pos: ', pos
                    printed = True
    return printed

def printDigisTruely(phDigi, thDigi):
    printed = False
    for d in phDigi:
        sc = d.scNum()+1
        print str(d.stNum()), ' ', str(d.scNum()), ' ', str(d.whNum())
        if d.stNum() == 1 and sc == 1 and d.whNum() == 0:
            print 'Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
        if d.stNum() == 1 and sc == 12 and d.whNum() == 0:
            print '####!!!!#### Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
        if d.stNum() == 1 and sc == 2 and d.whNum() == 0:
            print '####!!!!#### Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
        if d.stNum() == 1 and sc == 1 and d.whNum() == -1:
            print '####!!!!#### Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
        if d.stNum() == 1 and sc == 1 and d.whNum() == 1:
            print '####!!!!#### Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
            printed = True
    for d in thDigi:
        sc = d.scNum()+1
        if d.stNum() == 1 and sc == 1 and d.whNum() == 0:
            for pos in xrange(8):
                if d.position(pos) > 0:
                    print 'Station: ', d.stNum(), ' Sector: ', sc, ' Wheel: ', d.whNum(), ' pos: ', pos
                    printed = True
    return printed

def matchesHO(phDigi, thDigi, hoEntries, qualityCodes2d): #DONE
    # Two cases: from station 2, wheel 0, sector 1: use all
    # from station 2. wheel +/-1 sector 12/2: check if the muon would go through MB1, sector 1, wheel 0
    # if yes: do the extrapolation and check
    # Do correction if possible here
    phSc = phDigi.scNum()+1
    iphi = 5
    phi = Utils.getTrigPos(phDigi)
#     print 'Trigger position: ', str(phi)
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
        thSc = thDigi.scNum()+1
        ieta = -19
        for pos in xrange(8):
            if thDigi.code(pos) > 0:
                if thDigi.whNum() == 0 and thSc == 1 and thDigi.stNum() == 1:
                    if thDigi.whNum() == -2 or thDigi.whNum() == -1 or ( thDigi.whNum() == 0 and (thDigi.scNum() == 0 or thDigi.scNum() == 3 or thDigi.scNum() == 4 or thDigi.scNum() == 7 or thDigi.scNum() == 8 or thDigi.scNum() == 11)):
                        pos = 6-pos
                    ieta = pos - 3
                    ieta = -1*ieta

#     print 'Muon expected at phi: ', str(iphi), ' eta: ', str(ieta) 
    for i in range(hoEntries.size()):
        bg = hoEntries.__getitem__(i)
        if bg.energy() > .2 and bg.energy() < 1.5:
            detId = bg.id()
            if detId.iphi() == iphi:
                testEta = detId.ieta()
                if testEta > 0:
                    testEta = testEta-1
                if testEta == ieta:
                    qualityCodes2d.Fill(0,0)
                    return 7
                if testEta == ieta - 1:
                    qualityCodes2d.Fill(-1,0)
                    return 6
                if testEta == ieta + 1:
                    qualityCodes2d.Fill(1,0)
                    return 6
                for j in range(-4,4):
                    if testEta == j:
                        qualityCodes2d.Fill(testEta-ieta, 0)
                        return 5
                if ieta == -20: #Falls keine info fuer eta da ist
                    qualityCodes2d.Fill(-10, 0)
                    return 4
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
    

    
    
def getPhiFromDigi(phDigi):
    scNum = phDigi.scNum()+1
    phi = phDigi.phi()/4096.
    if Utils.hasPositiveRF(phDigi):
        phi = -1.*phi
    phi = phi -.14 #Shift of DT station
    scTransition = scNum-((scNum/7)*-12)-1
    phi = phi+.174532925 #pi/36*2
    return (phi+(scTransition*math.pi/6.))
    
    # Return phi from digi
    # Perhaps correct for bending
    
def getEtaFromDigi(thDigi): # More than one positive possible! Prepared to return all! Has to be reviewed in rest of code before!
    etas = []
    stNum = thDigi.stNum()
    wheel = thDigi.whNum()
    sector = thDigi.scNum()
    for pos in xrange(8):
         if thDigi.code(pos) > 0:
             if wheel == -2 or wheel == -1 or ( wheel == 0 and (sector == 0 or sector == 3 or sector == 4 or sector == 7 or sector == 8 or sector == 11) ):
                 pos = 6-pos
             if stNum == 1:
                 etas.append(Utils.getEta(3.850, (.32*pos) - 1.12))
                 return etas[0]
             if stNum == 2:
                 etas.append(Utils.getEta(4.645, (.32*pos) - 1.12))
                 return etas[0]
             if stNum == 3:
                 etas.append(Utils.getEta(5.635, (.32*pos) - 1.12))
                 return etas[0]
             if stNum == 4:
                 etas.append(Utils.getEta(6.920, (.32*pos) - 1.12))
                 return etas[0]
    return 0
             
    # Return eta from digi
    # (give eta at the middle of station if no eta available)
    
def getMuonCandidates(phDigi, thDigi, hoEntries, qualityCodes2d, stNum): #DONE

    candidates = []
    # look for phi and theta and match to phi eta tile of ho. add to list of candidates if ho gives signal
    for dP in phDigi:
        if dP.stNum() != stNum:
#             print 'Station is ', str(dP.stNum()), ' ... continue'
            continue
        if dP.scNum()+1 != 1:
#             print 'Sector is ', str(dP.scNum()), ' ... continue'
            continue
        if dP.whNum() != 0:
#             print 'Wheel is ', str(dP.whNum()), ' ... continue'
            continue
        hasThDigi = False
        for dT in thDigi:
            if dP.stNum() == dT.stNum() and dP.scNum() == dT.scNum() and dP.whNum() == dT.whNum():
                    # Here we have high quality and check for HO in eta and phi
                hasThDigi = True
                quality = matchesHO(dP, dT, hoEntries, qualityCodes2d)
                if quality >= 0:
                        candidates.append(HOMuon(-1.*getEtaFromDigi(dT), getPhiFromDigi(dP), Utils.getPtFromDigi(dP), quality))
        if hasThDigi == False:
            quality = matchesHO(dP, None, hoEntries, qualityCodes2d)
            if quality >= 0:
                candidates.append(HOMuon(0, getPhiFromDigi(dP), Utils.getPtFromDigi(dP), quality))
    return candidates

def writeHOEntries(entries, plot):
    for i in range(entries.size()):
        bg = entries.__getitem__(i)
        if bg.energy() > .2:
            detId = bg.id()
            plot.Fill(detId.ieta(), detId.iphi())

def analyze(deltaR, relPt, stNum, download):
    # deltaR: DeltaR of the matching cone
    # relPt: allowed relative pT deviation (1 = no deviation, 0 = infinit deviation)
    if download == 1:
        for file in fileList:
            event = [threading.Event(), threading.Event()]
            eventList.append(event)
        t = threading.Thread(target=downloadAll)
        t.start()
    
    ROOT.gROOT.SetStyle('Plain') # white background
    
    
    ##    PLOTS   ##
    # Only RECO working / L1 working
    qualityCodes = ROOT.TH1D("QualityCodes", "QualityCodes", 100, -1.5, 98.5)
    qualityCodesBad = ROOT.TH1D("QualityCodesBad", "QualityCodesBad", 100, -1.5, 98.5)
    qualityCodes2d = ROOT.TH2D("Quality Codes 2D", "Quality Codes 2D", 20, -10.5, 9.5, 10, -5.5, 4.5)
    
    hoOccupancy = ROOT.TH2D("HO Occupancy", "HO Occupancy", 31, -15.5, 15.5, 72, 0.5, 72.5)
    
    matchingJetEnergy = ROOT.TH1D("Matching Jet Energy", "Matching Jet Energy", 5000, 0, 5000)
    
    realPtVsL1PtOA = (ROOT.TH2D("Real Pt vs L1 HO Pt OA", "Real Pt vs L1 HO Pt OA", 100, 0, 500, 100, 0, 500))
    realPtVsL1Pt = []
    realPtVsL1Pt.append(ROOT.TH2D("Real Pt vs L1 HO Pt Code 0", "Real Pt vs L1 HO Pt code 0", 100, 0, 500, 100, 0, 500))
    realPtVsL1Pt.append(ROOT.TH2D("Real Pt vs L1 HO Pt Code 1", "Real Pt vs L1 HO Pt code 1", 100, 0, 500, 100, 0, 500))
    realPtVsL1Pt.append(ROOT.TH2D("Real Pt vs L1 HO Pt Code 2", "Real Pt vs L1 HO Pt code 2", 100, 0, 500, 100, 0, 500))
    realPtVsL1Pt.append(ROOT.TH2D("Real Pt vs L1 HO Pt Code 3", "Real Pt vs L1 HO Pt code 3", 100, 0, 500, 100, 0, 500))
    realPtVsL1Pt.append(ROOT.TH2D("Real Pt vs L1 HO Pt Code 4", "Real Pt vs L1 HO Pt code 4", 100, 0, 500, 100, 0, 500))
    realPtVsL1Pt.append(ROOT.TH2D("Real Pt vs L1 HO Pt Code 5", "Real Pt vs L1 HO Pt code 5", 100, 0, 500, 100, 0, 500))
    realPtVsL1Pt.append(ROOT.TH2D("Real Pt vs L1 HO Pt Code 6", "Real Pt vs L1 HO Pt code 6", 100, 0, 500, 100, 0, 500))
    realPtVsL1Pt.append(ROOT.TH2D("Real Pt vs L1 HO Pt Code 7", "Real Pt vs L1 HO Pt code 7", 100, 0, 500, 100, 0, 500))
    
    realPhiVsL1PhiOA = (ROOT.TH2D("Real Phi vs L1 HO Pt OA", "Real Phi vs L1 HO Pt OA", 100, -.5, .5, 100, -.5, .5))
    realPhiVsL1Phi = []
    realPhiVsL1Phi.append(ROOT.TH2D("Real Phi vs L1 HO Pt Code 0", "Real Phi vs L1 HO Pt Code 0", 100, -.5, .5, 100, -.5, .5))
    realPhiVsL1Phi.append(ROOT.TH2D("Real Phi vs L1 HO Pt Code 1", "Real Phi vs L1 HO Pt Code 1", 100, -.5, .5, 100, -.5, .5))
    realPhiVsL1Phi.append(ROOT.TH2D("Real Phi vs L1 HO Pt Code 2", "Real Phi vs L1 HO Pt Code 2", 100, -.5, .5, 100, -.5, .5))
    realPhiVsL1Phi.append(ROOT.TH2D("Real Phi vs L1 HO Pt Code 3", "Real Phi vs L1 HO Pt Code 3", 100, -.5, .5, 100, -.5, .5))
    realPhiVsL1Phi.append(ROOT.TH2D("Real Phi vs L1 HO Pt Code 4", "Real Phi vs L1 HO Pt Code 4", 100, -.5, .5, 100, -.5, .5))
    realPhiVsL1Phi.append(ROOT.TH2D("Real Phi vs L1 HO Pt Code 5", "Real Phi vs L1 HO Pt Code 5", 100, -.5, .5, 100, -.5, .5))
    realPhiVsL1Phi.append(ROOT.TH2D("Real Phi vs L1 HO Pt Code 6", "Real Phi vs L1 HO Pt Code 6", 100, -.5, .5, 100, -.5, .5))
    realPhiVsL1Phi.append(ROOT.TH2D("Real Phi vs L1 HO Pt Code 7", "Real Phi vs L1 HO Pt Code 7", 100, -.5, .5, 100, -.5, .5))
    
    realEtaVsL1EtaOA = (ROOT.TH2D("Real Eta vs L1 HO Pt OA", "Real Eta vs L1 HO Pt OA", 100, -.5, .5, 100, -.5, .5))
    realEtaVsL1Eta = []
    realEtaVsL1Eta.append(ROOT.TH2D("Real Eta vs L1 HO Pt Code 0", "Real Eta vs L1 HO Pt Code 0", 100, -.5, .5, 100, -.5, .5))
    realEtaVsL1Eta.append(ROOT.TH2D("Real Eta vs L1 HO Pt Code 1", "Real Eta vs L1 HO Pt Code 1", 100, -.5, .5, 100, -.5, .5))
    realEtaVsL1Eta.append(ROOT.TH2D("Real Eta vs L1 HO Pt Code 2", "Real Eta vs L1 HO Pt Code 2", 100, -.5, .5, 100, -.5, .5))
    realEtaVsL1Eta.append(ROOT.TH2D("Real Eta vs L1 HO Pt Code 3", "Real Eta vs L1 HO Pt Code 3", 100, -.5, .5, 100, -.5, .5))
    realEtaVsL1Eta.append(ROOT.TH2D("Real Eta vs L1 HO Pt Code 4", "Real Eta vs L1 HO Pt Code 4", 100, -.5, .5, 100, -.5, .5))
    realEtaVsL1Eta.append(ROOT.TH2D("Real Eta vs L1 HO Pt Code 5", "Real Eta vs L1 HO Pt Code 5", 100, -.5, .5, 100, -.5, .5))
    realEtaVsL1Eta.append(ROOT.TH2D("Real Eta vs L1 HO Pt Code 6", "Real Eta vs L1 HO Pt Code 6", 100, -.5, .5, 100, -.5, .5))
    realEtaVsL1Eta.append(ROOT.TH2D("Real Eta vs L1 HO Pt Code 7", "Real Eta vs L1 HO Pt Code 7", 100, -.5, .5, 100, -.5, .5))
    
    recoPositionOfMuons = ROOT.TH2D("Reco Position", "Reco Position", 100, -.5, .5, 628, -1.*math.pi, math.pi)
    genPositionsOfRecMuons = ROOT.TH2D("Gen Position of reconstructed muons", "Gen Position of reconstructed muons", 100, -.5, .5, 628, -1.*math.pi, math.pi)
    # Failing
    qualityCodesWrong = ROOT.TH1D("QualityCodes Wrong", "QualityCodes Wrong", 100, -1.5, 98.5)
    qualityCodes2dWrong = ROOT.TH2D("Quality Codes 2D Wrong", "Quality Codes 2D Wrong", 20, -10.5, 9.5, 10, -5.5, 4.5)
    realPtVsL1PtWrong = ROOT.TH1D("Real Pt vs L1 HO Pt Wrong", "Real Pt vs L1 HO Pt Wrong", 100, 0, 500)
    realPhiVsL1PhiWrong = ROOT.TH1D("Real Phi vs L1 HO Pt Wrong", "Real Phi vs L1 HO Pt Wrong", 100, -.5, .5)
    realEtaVsL1EtaWrong = ROOT.TH1D("Real Eta vs L1 HO Pt Wrong", "Real Eta vs L1 HO Pt Wrong", 100, -.5, .5)
    # Failing but recovered
    qualityCodesWrongRecovered = ROOT.TH1D("QualityCodes Wrong Recovered", "QualityCodes Wrong Recovered", 100, -1.5, 98.5)
    realPtVsL1PtWrongRecovered = ROOT.TH1D("Real Pt vs L1 HO Pt Wrong Recovered", "Real Pt vs L1 HO Pt Wrong Recovered", 100, 0, 500)
    realPhiVsL1PhiWrongRecovered = ROOT.TH1D("Real Phi vs L1 HO Pt Wrong Recovered", "Real Phi vs L1 HO Pt Wrong Recovered", 100, -.5, .5)
    realEtaVsL1EtaWrongRecovered = ROOT.TH1D("Real Eta vs L1 HO Pt Wrong Recovered", "Real Eta vs L1 HO Pt Wrong Recovered", 100, -.5, .5)
    #recoYes,L1No
    qualityCodesRecoNoL1 = ROOT.TH1D("QualityCodes RecoNoL1", "QualityCodes RecoNoL1", 100, -1.5, 98.5)
    realPtVsL1PtRecoNoL1 = ROOT.TH1D("Real Pt vs L1 HO Pt RecoNoL1", "Real Pt vs L1 HO Pt RecoNoL1", 100, 0, 500)
    realPhiVsL1PhiRecoNoL1 = ROOT.TH1D("Real Phi vs L1 HO Pt RecoNoL1", "Real Phi vs L1 HO Pt RecoNoL1", 100, -.5, .5)
    realEtaVsL1EtaRecoNoL1 = ROOT.TH1D("Real Eta vs L1 HO Pt RecoNoL1", "Real Eta vs L1 HO Pt RecoNoL1", 100, -.5, .5)
    
    wrongCandidateEtaPhi  = ROOT.TH2D("Eta phi of wrong L1 HO muon candidates", "Eta phi of wrong L1 HO muon candidates", 30, -1.*Utils.getEta(4.02, 6.61), Utils.getEta(4.02, 6.61), 72, -1*math.pi, math.pi)
    
    pdgIdOfMatchingParticle = ROOT.TH1D("pdgId of matching PF Candidate", "pdgId of matching PF Candidate", 10000, -4999.5, 5000.5)
    
    
    numberOfFails = 0
    numberOfRecoveries = 0
    numberOfRecEvents = 0
    numberOfTooMany = 0
    tooManyEventCounter = 0
    
    for f in range(len(fileList)):
        
        if download == 1:
            b1 = eventList[f][0].wait(600)#warten auf beide events event.wait()
            b2 = eventList[f][1].wait(600)
         
            if not b1 or not b2:
                print 'Download error. Ending'
                break
         
            print 'Files ', fileList[f][0], ' and ', fileList[f][1], ' are ready... analyzing them'
        
        eventsBad = Events(fileList[f][1]) #sample with dead MB1
        eventsGood = Events(fileList[f][0])

        eventsBad.toBegin()
        eventsGood.toBegin()
    
        eventsGood_iter = eventsGood.__iter__()
        eventsBad_iter = eventsBad.__iter__()
    
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
            
            badEvent.getByLabel(labelJetContainer, jetContainerHandle)
            jetContainer = jetContainerHandle.product()
            
            goodEvent.getByLabel(labelPfCandidate, pfCandidateHandle)
            pfCandidateContainer = pfCandidateHandle.product()
        
            badEvent.getByLabel(labelRpcDigiContainer, rpcDigiContainerHandle)
            rpcDigiContainer = rpcDigiContainerHandle.product()
            
            #return
             
            #badEvent.getByLabel(labelPfJetContainer, pfJetContainerHandle)
            #jetContainer = pfJetContainerHandle.product()
            
            
            #----- END GET THE HANDLES -----
            phiDigis = phiContainer.getContainer()
        
        
            badEvent.getByLabel(labelThContainer, thContainerHandle)
            thContainer = thContainerHandle.product()
            #----- END GET THE HANDLES -----
            thDigis = thContainer.getContainer()
            
        
            writeHOEntries(badHoEntries, hoOccupancy)
        
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
            
            failEvent = False
            tooManyEvent = False
            for j in range(len(l1MuonTuple)):
                
                element = l1MuonTuple[j]
                if not element[matchingGoodMuon] == None:
                    if element[matchingBadMuon] == None:
                        if abs(element[recoMuon].eta()) < Utils.getEta(3.85, 1.28):
                            if element[recoMuon].phi() >= -10.*math.pi/180. and element[recoMuon].phi() < 20./180.*math.pi:
                                numberOfFails = numberOfFails + 1
                                failEvent = True
                                
            if failEvent == True:
                if printDigis(phiDigis, thDigis):
                    candidates = getMuonCandidates(phiDigis, thDigis, badHoEntries, qualityCodes2d, stNum)
                    if candidates:
                        numberOfRecEvents = numberOfRecEvents+1
                        genPositionsOfRecMuons.Fill(element[recoMuon].eta(), element[recoMuon].phi())
                    for c in candidates:
#                         c.printInfo()
                        qualityCodes.Fill(c.quality)
                        element = Utils.findNearestRecoMuon(c, l1MuonTuple)
                        if not element:
                            continue
                        realPtVsL1PtOA.Fill(element[recoMuon].pt(), c.pt())
                        realPhiVsL1PhiOA.Fill(element[recoMuon].phi(), c.phi())
                        realEtaVsL1EtaOA.Fill(element[recoMuon].eta(), c.eta())
                        if c.quality > -1:
                            realPtVsL1Pt[c.quality].Fill(element[recoMuon].pt(), c.pt())
                            realPhiVsL1Phi[c.quality].Fill(element[recoMuon].phi(), c.phi())
                            realEtaVsL1Eta[c.quality].Fill(element[recoMuon].eta(), c.eta())
                        recoPositionOfMuons.Fill(c.eta(), c.phi())
                        numberOfRecoveries = numberOfRecoveries + 1
                        if not Utils.getMatch(c, goodL1Muons, .3, .5):
                            qualityCodesBad.Fill(c.quality)
                    if not candidates:
                        qualityCodes.Fill(-1)
                            
#                                 print 'Event ' + str(i) + ', RECO (gen), pT: ', str(element[recoMuon].pt()), ' eta: ', str(element[recoMuon].eta()), 'phi ', str(element[recoMuon].phi())
                                
#                                     print '--------------------------- '
            else:
                if printDigis(phiDigis, thDigis):
                    candidates = getMuonCandidates(phiDigis, thDigis, badHoEntries, qualityCodes2dWrong, stNum) #change plots!
                    pT = 0
                    
                    if isGetHighestCandidate == 1:
                        for c in candidates:
                            if c.pt() > pT:
                                #print "c.pt " , str(c.pt()) , " highPT " , str(pT)
                                highestCandidate = c
                                pT = c.pt()
                            
                    
                        candidates = []
                        if pT > 0:
                            candidates.append(highestCandidate)
                    
                    for c in candidates:
                        if not Utils.getMatch(c, badL1Muons, .3, .5):
                            if not Utils.getMatch(c, goodL1Muons, .3, .5):
                                if Utils.getMatch(c, goodRecoMuons, .3, .5) or Utils.getMatch(c, genParticles, .3, .5) or Utils.matchJet(c, pfCandidateContainer, .3):
                                    if Utils.matchJet(c, pfCandidateContainer, .3):
                                        jet = Utils.matchJet(c, pfCandidateContainer, .3)
                                        matchingJetEnergy.Fill(jet.pt())
                                        pdgIdOfMatchingParticle.Fill(jet.pdgId())
                                        #print 'Matching jet: ', str(jet.energy()), ' pdgId: ', str(jet.pdgId()), ' phi: ', str(c.phi()-jet.phi()), ' eta: ' , str(c.eta()-jet.eta())
                                        #print 'GEN: pT: ' ,genParticles.at(0).pt() , 'phi: ', genParticles.at(0).phi(), ' eta: ', genParticles.at(0).eta()
#                                     c.printInfo()
                                    #if Utils.getMatch(c, genParticles, .3, .5):
                                        #print 'Matching gen'
                                    qualityCodesRecoNoL1.Fill(c.quality)
                                    realPtVsL1PtRecoNoL1.Fill(c.pt())
                                    realPhiVsL1PhiRecoNoL1.Fill(c.phi())
                                    realEtaVsL1EtaRecoNoL1.Fill(c.eta())
                                else:
#                                     c.printInfo()
                                    qualityCodesWrong.Fill(c.quality)
                                    realPtVsL1PtWrong.Fill(c.pt())
                                    realPhiVsL1PhiWrong.Fill(c.phi())
                                    realEtaVsL1EtaWrong.Fill(c.eta())
                                    if c.quality > 5:
                                        wrongCandidateEtaPhi.Fill(c.eta(), c.phi())
                                    numberOfTooMany = numberOfTooMany + 1
                                    tooManyEvent = True
                                    print 'File: ', str(f+1), ' Event: ' , str(i)
                                    printDigisTruely(phiDigis, thDigis)
                            else:
                                c.printInfo()
                                qualityCodesWrongRecovered.Fill(c.quality)
                                realPtVsL1PtWrongRecovered.Fill(c.pt())
                                realPhiVsL1PhiWrongRecovered.Fill(c.phi())
                                realEtaVsL1EtaWrongRecovered.Fill(c.eta())
            if tooManyEvent:
                tooManyEventCounter = tooManyEventCounter + 1
                        
                    
                    # Here we have the muons that are detected in L1 for the working detector, but are not detected in the non working detector anymore
                    # element[recoMuon] is the corresponding RECO muon (meaning the 'GEN' muon)
        #files Loeschen
        if download == 12:
            print 'Removing file: ', fileList[f][1]
            os.remove(fileList[f][1]) #sample with dead MB1
            print 'Removing file: ', fileList[f][0]
            os.remove(fileList[f][0])
    print 'Number of additional fails: ', str(numberOfFails)
    print 'Number of recovered events: ', str(numberOfRecEvents)
    print 'Number of recoveries : ' , str(numberOfRecoveries)
    print 'Number of too many: ', str(numberOfTooMany)
    print 'Number of events with too many: ', str(tooManyEventCounter)
    save('Quality.root',pdgIdOfMatchingParticle, wrongCandidateEtaPhi,matchingJetEnergy, hoOccupancy, qualityCodesRecoNoL1,realPtVsL1PtRecoNoL1,realPtVsL1PtOA,realPhiVsL1PhiOA,realEtaVsL1EtaOA, realPhiVsL1PhiRecoNoL1, realEtaVsL1EtaRecoNoL1, qualityCodesWrongRecovered,realPtVsL1PtWrongRecovered,realPhiVsL1PhiWrongRecovered,realEtaVsL1EtaWrongRecovered, qualityCodes, realPtVsL1Pt[0], realPtVsL1Pt[1], realPtVsL1Pt[2], realPtVsL1Pt[3], realPtVsL1Pt[4], realPtVsL1Pt[5], realPtVsL1Pt[6], realPtVsL1Pt[7], qualityCodes2d, realPhiVsL1Phi[0], realPhiVsL1Phi[1], realPhiVsL1Phi[2], realPhiVsL1Phi[3], realPhiVsL1Phi[4], realPhiVsL1Phi[5], realPhiVsL1Phi[6], realPhiVsL1Phi[7], genPositionsOfRecMuons, realEtaVsL1Eta[0], realEtaVsL1Eta[1], realEtaVsL1Eta[2], realEtaVsL1Eta[3], realEtaVsL1Eta[4], realEtaVsL1Eta[5], realEtaVsL1Eta[6], realEtaVsL1Eta[7], recoPositionOfMuons, qualityCodes2dWrong, qualityCodesWrong, realPtVsL1PtWrong, realPhiVsL1PhiWrong, realEtaVsL1EtaWrong, qualityCodesBad)
#for i in xrange(100):
analyze(.2, .5, 1, 0)

#save('Data.root', deltaZ)
