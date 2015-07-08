import ROOT
import math
from DataFormats.FWLite import Events, Handle
from Utils import *

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
#print 2**.5*math.pi/36

def save(name, *plot):
    file = ROOT.TFile(name, 'RECREATE')
    for x in plot:
        x.Write()
    file.Close()

def printDigis(phDigi, thDigi):
    for d in phDigi:
        if d.stNum() == 2:
            print 'Station: ', d.stNum(), ' Sector: ', d.scNum(), ' Wheel: ', d.whNum(), ' phi: ', d.phi(), 'phiB: ', d.phiB()
    for d in thDigi:
        if d.stNum() == 2:
            for pos in xrange(8):
                if d.position(pos) > 0:
                    print 'Station: ', d.stNum(), ' Sector: ', d.scNum(), ' Wheel: ', d.whNum(), ' pos: ', pos

def machtesHO(phDigi, thDigi, hoEntries):
    # Do correction if possible here
    phi = phDigi.phi()/2048.
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
     for pos in xrange(8):
         if d.code(pos) > 0:
             if d.whNum() == 0 and d.scNum() == 1 and d.stNum() == 2:
                 ieta = pos - 3

    for i in range(hoEntries.size()):
        bg = hoEntries.__getitem__(i)
        if bg.energy() > .2:
            detId = bg.id()
            if detId.iphi() == iphi:
                testEta = detId.ieta()
                if testEta < 0:
                    testEta = testEta+1
                if testEta == ieta:
                    return True
                if testEta == ieta - 1:
                    return True
                if testEta == ieta + 1:
                    return True
    return False

    # Falls ieta == -20, dann gibt es keinen eta eintrag
    # Falls vorhanden gucke in iphi und ieta im intervall 3 nach einem eintrag ueber threshold
    # Falls nicht, gucke in iphi und komplett eta
    # Checks if phDigi matches to an ok HO entry
    
def getPtFromDigi(phDigi, stNum):
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
        return n0/(phiB-n2)+n1
    else:
        return p0/(phiB-p2)+p1
    
    
def getPhiFromDigi(phDigi, stNum):
    # Return phi from digi
    
def getEtaFromDigi(thDigi, stNum):
    # Return eta from digi
    # (give eta at the middle of station if no eta available)
    
def getMuonCandidates(phDigi, thDigi):
    candidates = []
    # look for phi and theta and match to phi eta tile of ho. add to list of candidates if ho gives signal
    for dP in phDigi:
        if matchesHOinPhi(dP, hoEntries):
            for dT in thDigi:
                if dP.stNum() == dT.stNum() and dP.scNum() == dT.scNum() and dP.whNum() == dT.whNum():
                    # Here we have high quality and check for HO in eta and phi
                    if matchesHOinEta(dT, hoEntries):
                        # Create HQ HO muon status 10
                    else
                        # Create LQ HO muon status 5
                        # Check whole slice -> quality 7
                else
                # Here we have low quality. No matching entry in DT for eta. LQ HO Muon status 1
                # possibly check for whole eta slice -> think schould be done! quality 7



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
                deltaZ.Fill(element.vz())
                allRecoMuons.Fill(element.eta(), element.phi())
                allRecoMuonsPt.Fill(element.pt())
                thisTuple = [element, Utils.getMatch(element, badL1Muons, deltaR, relPt), Utils.getMatch(element, goodL1Muons, deltaR, relPt)]
                l1MuonTuple.append(thisTuple)
    
        for j in range(len(l1MuonTuple)):
            element = l1MuonTuple[j]
            if element[matchingGoodMuon] == None:
                allNonWorkingRecoMuonsGoodPt.Fill(element[recoMuon].pt())
                allNonWorkingRecoMuonsGood.Fill(element[recoMuon].eta(), element[recoMuon].phi())
                if not element[matchingBadMuon] == None:
                    diffGhostsEtaPhi.Fill(element[recoMuon].eta(), element[recoMuon].phi())
            else:
                allWorkingRecoMuonsPt.Fill(element[recoMuon].pt())
                allWorkingRecoMuons.Fill(element[recoMuon].eta(), element[recoMuon].phi())
                if element[matchingBadMuon] == None:
                    printDigis(phiDigis, thDigis)
                    print 'RECO (gen), pT: ', element[recoMuon].pt(), ' eta: ', element[recoMuon].eta(), 'phi ', element[recoMuon].phi()
                    print ' '
                    
                    # Here we have the muons that are detected in L1 for the working detector, but are not detected in the non working detector anymore
                    # element[recoMuon] is the corresponding RECO muon (meaning the 'GEN' muon)
                    numberOfAdditionals = numberOfAdditionals + 1
                    diffFailsEtaPhi.Fill(element[recoMuon].eta(), element[recoMuon].phi())
                    
                    hoEntry = Utils.getHoEntry(Utils.translateToIPhi(element[recoMuon].phi()), Utils.translateToIEta(element[recoMuon].eta()), badHoEntries)
                    highestEnergy3Phi = Utils.getHighestHoEntry3(Utils.translateToIPhi(element[recoMuon].phi()), Utils.translateToIEta(element[recoMuon].eta()), badHoEntries)
                    hoEntryPlot3Phi.Fill(highestEnergy3Phi)
                    if highestEnergy3Phi > 0.2:
                        numberOfHighHOEntries3Phi = numberOfHighHOEntries3Phi + 1
                    if hoEntry != None:
                        if hoEntry.energy() > 0.2:
                            numberOfHighHOEntries = numberOfHighHOEntries + 1
                        #print hoEntry.energy()
                        #print 'phi: ', Utils.translateToIEta(element[recoMuon].eta()) , ' phi: ', Utils.translateToIPhi(element[recoMuon].phi())
                        hoEntryPlot.Fill(hoEntry.energy())
                    else:
                        #print '000'
                        #print 'phi: ', Utils.translateToIEta(element[recoMuon].eta()) , ' phi: ', Utils.translateToIPhi(element[recoMuon].phi())
                        hoEntryPlot.Fill(0)
     
        for element in l1MuonTuple:
            if element[matchingBadMuon] == None:
                allNonWorkingRecoMuonsBadPt.Fill(element[recoMuon].pt())
                allNonWorkingRecoMuonsBad.Fill(element[recoMuon].eta(), element[recoMuon].phi())
             
             ########### Controll Plots   
        for j in range(len(l1MuonTuple)):
            element = l1MuonTuple[j]
            if element[matchingBadMuon] == None:
                if element[matchingGoodMuon] == None:
                    NGoodNBadPt.Fill(element[recoMuon].pt())
                    if Utils.isSame(element[recoMuon], matchedToGenRecoMuon):
                        numberOfNonGoodNonBadGen = numberOfNonGoodNonBadGen + 1
                    else:
                        numberOfNonGoodNonBad = numberOfNonGoodNonBad + 1
                else:
                    YGoodNBadPt.Fill(element[recoMuon].pt())
                    if Utils.isSame(element[recoMuon], matchedToGenRecoMuon):
                        numberOfGoodNonBadGen = numberOfGoodNonBadGen + 1
                    else:
                        numberOfGoodNonBad = numberOfGoodNonBad + 1
            else:
                if element[matchingGoodMuon] == None:
                    #print i
                    NGoodYBadPt.Fill(element[recoMuon].pt())
                    if Utils.isSame(element[recoMuon], matchedToGenRecoMuon):
                        numberOfNonGoodBadGen = numberOfNonGoodBadGen + 1
                    else:
                        numberOfNonGoodBad = numberOfNonGoodBad + 1
                else:
                    YGoodYBadPt.Fill(element[recoMuon].pt())
                    if Utils.isSame(element[recoMuon], matchedToGenRecoMuon):
                        numberOfGoodBadGen = numberOfGoodBadGen + 1
                    else:
                        numberOfGoodBad = numberOfGoodBad + 1
    ###### PLOTTING ######
           
    lowerPhi = -1*math.atan(65./355.)
    upperPhi = math.atan(126./355.)
    lowerEta = -1.*Utils.getEta(4.02, 1.268)
    upperEta = Utils.getEta(4.02, 1.268)
    
    line1 = ROOT.TLine(lowerEta, lowerPhi, lowerEta, upperPhi)
    line1.SetLineWidth(2)
    line2 = ROOT.TLine(upperEta, lowerPhi, upperEta, upperPhi)
    line2.SetLineWidth(2)           
    ## Phi lines
    line3 = ROOT.TLine(lowerEta, lowerPhi, upperEta, lowerPhi)
    line3.SetLineWidth(2)
    line4 = ROOT.TLine(lowerEta, upperPhi, upperEta, upperPhi)
    line4.SetLineWidth(2)  
    
    canvas1 = ROOT.TCanvas()
    allNonWorkingRecoMuonsGood.Draw('colz')
    line1.Draw('same')
    line2.Draw('same')
    line3.Draw('same')
    line4.Draw('same')
    #canvas1.SaveAs('EfficiencyEtaPhiGood.png')
    
    canvas2 = ROOT.TCanvas()
    allNonWorkingRecoMuonsBad.Draw('colz')
    efficiencyEtaPhiDiff = allNonWorkingRecoMuonsBad.Clone()
    efficiencyEtaPhiDiff.Add(allNonWorkingRecoMuonsGood, -1.)#
    line1.Draw('same')
    line2.Draw('same')
    line3.Draw('same')
    line4.Draw('same')
    #canvas2.SaveAs('EfficiencyEtaPhiBad.png')
    
    canvas3 = ROOT.TCanvas()
    efficiencyEtaPhiDiff.Draw('colz')
    line1.Draw('same')
    line2.Draw('same')
    line3.Draw('same')
    line4.Draw('same')
    #canvas3.SaveAs('EfficiencyEtaPhiDiff.png')
    
    canvas4 = ROOT.TCanvas()
    allRecoMuons.Draw('colz')
    line1.Draw('same')
    line2.Draw('same')
    line3.Draw('same')
    line4.Draw('same')
    #canvas4.SaveAs('AllRecoMuons.png')
    
    canvas5 = ROOT.TCanvas()
    relAllRecoMuons = efficiencyEtaPhiDiff.Clone()
    relAllRecoMuons.Divide(allRecoMuons)
    relAllRecoMuons.SetTitle('Additional missing L1 muons / number of all RECO (GEN) muons')
    relAllRecoMuons.Draw('colz')
    line1.Draw('same')
    line2.Draw('same')
    line3.Draw('same')
    line4.Draw('same')
    #canvas5.SaveAs('relAllRecoMuons.png')
    
    canvas6 = ROOT.TCanvas()
    allWorkingRecoMuons.Draw('colz')
    line1.Draw('same')
    line2.Draw('same')
    line3.Draw('same')
    line4.Draw('same')
    #canvas6.SaveAs('AllWorkingRecoMuons.png')
    
    canvas7 = ROOT.TCanvas()
    relAllWorkingRecoMuons = efficiencyEtaPhiDiff.Clone()
    relAllWorkingRecoMuons.Divide(allWorkingRecoMuons)
    relAllWorkingRecoMuons.SetTitle('Additional missing L1 muons / number of all RECO (GEN) muons with L1 match')
    relAllWorkingRecoMuons.Draw('colz')
    relAllWorkingRecoMuons.GetXaxis().SetTitle('#eta')
    relAllWorkingRecoMuons.GetXaxis().SetTitle('#phi')
    #line1.Draw('same')
    #line2.Draw('same')
    #line3.Draw('same')
    #line4.Draw('same')
    #canvas7.SaveAs('relAllWorkingRecoMuons.png')
    
    canvas8 = ROOT.TCanvas()
    diffFailsEtaPhi.Draw('colz')
    
    canvas9 = ROOT.TCanvas()
    temp1 = diffFailsEtaPhi.Clone()
    temp1.Divide(allWorkingRecoMuons)
    temp1.Draw('colz')
    
    ###### CALCULATE VALUES
    sumEntries = 0
    sumMean = 0
    nEntries = 0
    for eta in range(12,20):
        for phi in range(35,41):
            nEntries = nEntries+1
            sumEntries = sumEntries + diffFailsEtaPhi.GetBinContent(eta, phi)
            sumMean = sumMean + temp1.GetBinContent(eta,phi)
    sumMean = sumMean*1./nEntries/1.
    #print 'Summe der zusaetzlichen Fails im Bereich der abgeschalteten Kammer: ', sumEntries
    #print 'Anteil der zusaetzlichen Fails bezogen auf die vorher funktionierenden Identifikationen im Bereich der abgeschalteten Kammer: ', sumMean
    #print 'Anzahl der bins: ', nEntries        
    #print 'Anzahl zusaetzlich fehlenden L1 myonen: ', numberOfAdditionals
    #print 'Anzahl der hohen HO entries bei fehlendem L1: ', numberOfHighHOEntries
    #print 'Anzahl der hohen HO entries bei fehlendem L1 in 3 phi: ', numberOfHighHOEntries3Phi
    
    print relPt
    print 'numberOfNonGoodNonBad ', numberOfNonGoodNonBad
    print 'numberOfNonGoodBad ', numberOfNonGoodBad
    print 'numberOfGoodNonBad ', numberOfGoodNonBad
    print 'numberOfGoodBad ', numberOfGoodBad
    
    print 'numberOfNonGoodNonBadGen ', numberOfNonGoodNonBadGen
    print 'numberOfNonGoodBadGen ', numberOfNonGoodBadGen
    print 'numberOfGoodNonBadGen ', numberOfGoodNonBadGen
    print 'numberOfGoodBadGen ', numberOfGoodBadGen
    
    sumOfAll = numberOfNonGoodNonBad + numberOfNonGoodNonBadGen + numberOfNonGoodBad + numberOfNonGoodBadGen + numberOfGoodNonBad + numberOfGoodNonBadGen + numberOfGoodBad + numberOfGoodBadGen
    
    numberOfGoodNonBadByDeltaRPileUp.SetBinContent(numberOfGoodNonBadByDeltaRPileUp.FindBin(relPt), numberOfGoodNonBad*1./sumOfAll)
    numberOfNonGoodBadByDeltaRPileUp.SetBinContent(numberOfNonGoodBadByDeltaRPileUp.FindBin(relPt), numberOfNonGoodBad*1./sumOfAll)
    numberOfGoodBadByDeltaRPileUp.SetBinContent(numberOfGoodBadByDeltaRPileUp.FindBin(relPt), numberOfGoodBad*1./sumOfAll)
    numberOfNonGoodNonBadByDeltaRPileUp.SetBinContent(numberOfNonGoodNonBadByDeltaRPileUp.FindBin(relPt), numberOfNonGoodNonBad*1./sumOfAll)
   
    numberOfGoodNonBadByDeltaRPileUpGen.SetBinContent(numberOfGoodNonBadByDeltaRPileUpGen.FindBin(relPt), numberOfGoodNonBadGen*1./sumOfAll)
    numberOfNonGoodBadByDeltaRPileUpGen.SetBinContent(numberOfNonGoodBadByDeltaRPileUpGen.FindBin(relPt), numberOfNonGoodBadGen*1./sumOfAll)
    numberOfGoodBadByDeltaRPileUpGen.SetBinContent(numberOfGoodBadByDeltaRPileUpGen.FindBin(relPt), numberOfGoodBadGen*1./sumOfAll)
    numberOfNonGoodNonBadByDeltaRPileUpGen.SetBinContent(numberOfNonGoodNonBadByDeltaRPileUpGen.FindBin(relPt), numberOfNonGoodNonBadGen*1./sumOfAll)



#for i in xrange(100):
analyze(.2, .5)

#save('Data.root', deltaZ)
save('OverallData.root', numberOfGoodNonBadByDeltaRPileUp, numberOfNonGoodBadByDeltaRPileUp, numberOfGoodBadByDeltaRPileUp, numberOfNonGoodNonBadByDeltaRPileUp, numberOfGoodNonBadByDeltaRPileUpGen, numberOfNonGoodBadByDeltaRPileUpGen, numberOfGoodBadByDeltaRPileUpGen, numberOfNonGoodNonBadByDeltaRPileUpGen)