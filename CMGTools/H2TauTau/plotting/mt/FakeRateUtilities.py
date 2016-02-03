import ROOT
import os
import datetime
from FakeFactors import fake_factors_regions, signal_selections_list, inverted_selections_list



def getBackgroundFractions(filename='datacard_mutau_qcdFromSS.root', dir='lowMT_mvis'):
    file = ROOT.TFile.Open(filename)
    histos = {'VV':None,'TT':None,'QCD':None,'W':None,'ZJ':None}
    histo_tot = None
    for name in histos:
        histo = file.Get('{DIR}/{HIST}'.format(DIR=dir,HIST=name))
        histo.__class__ = ROOT.TH1F
        histos[name] = histo
        if not histo_tot:
            histo_tot = histo.Clone('ALL')
        else:
            histo_tot.Add(histo)
    fractions = {}
    for name,histo in histos.items():
        fraction = histo.Clone('{NAME}_Fraction'.format(NAME=name))
        fraction.SetDirectory(0)
        fraction.Divide(histo_tot)
        fractions[name] = fraction
    file.Close()
    return fractions


class FakeFactor:
    def __init__(self):
        self.name = None
        self.version = None
        self.root_file = None
        #self.directories = None
        self.background_fraction = None

fakeFactors = {}
## ZMuMu
fakeFactors['ZMuMu'] = FakeFactor()
fakeFactors['ZMuMu'].name = 'ZMuMu'
fakeFactors['ZMuMu'].version = 'v_1_2016-02-02'
fakeFactors['ZMuMu'].root_file = '/afs/cern.ch/user/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/{FACTORS}/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root'
fakeFactors['ZMuMu'].directory_tag = 'Weight'
fakeFactors['ZMuMu'].background_fraction = ['VV','TT','ZJ']
## HighMT
fakeFactors['HighMT'] = FakeFactor()
fakeFactors['HighMT'].name = 'HighMT'
fakeFactors['HighMT'].version = 'v_4_2016-02-02'
fakeFactors['HighMT'].root_file = '/afs/cern.ch/user/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/{FACTORS}/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root'
fakeFactors['HighMT'].directory_tag = 'Weight_HighMT'
fakeFactors['HighMT'].background_fraction = ['W']
## QCDSS
fakeFactors['QCDSS'] = FakeFactor()
fakeFactors['QCDSS'].name = 'QCDSS'
fakeFactors['QCDSS'].version = 'v_1_2016-02-02'
fakeFactors['QCDSS'].root_file = '/afs/cern.ch/user/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/{FACTORS}/{SAMPLE}/{VERSION}/fakerates_MuTau_{SAMPLE}.root'
fakeFactors['QCDSS'].directory_tag = 'Weight_QCDSS'
fakeFactors['QCDSS'].background_fraction = ['QCD']


selections = signal_selections_list + inverted_selections_list
selectionsMT40 = ['MT40_'+sel for sel in selections]
selections.extend(selectionsMT40)



def weightBackgrounds(
    factors=fakeFactors,
    histo_templates=['hFakeRate_{SEL}_mvis_stdbins_vs_match5'],
    out_dir='/afs/cern.ch/user/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/Combined/{SAMPLE}/{VERSION}'
    ):
    #
    samples = ['Data_Run15D_05Oct',
               'Data_Run15D_v4',
               'QCD',
               'TT',
               'VVTo2L2Nu',
               'WZTo1L3Nu',
               'WZTo3L',
               'TBar_tWch',
               'T_tWch',
               'W',
               'WWTo1L1Nu2Q',
               'WZTo1L1Nu2Q',
               'WZTo2L2Q',
               'ZJ',
               'ZZTo2L2Q',
              ]
    # Combine trees in each sample
    for sample in samples:
        ## Find version
        version = "v_1_{DATE}".format(DATE=datetime.date.today())
        if os.path.isdir(out_dir.format(SAMPLE=sample,VERSION='')):
            listdirs= [f for f in os.listdir(out_dir.format(SAMPLE=sample,VERSION='')) if os.path.isdir(os.path.join(out_dir.format(SAMPLE=sample,VERSION=''),f))]
            numberMax = 0
            for d in listdirs:
                if "v_" in d:
                    number = int(d.split("_")[1])
                    if number > numberMax:
                        numberMax = number
            version = "v_{NUM}_{DATE}".format(NUM=numberMax+1, DATE=datetime.date.today())
        print '>> Producing combined sample {SAMPLE} version {VERSION}'.format(SAMPLE=sample,VERSION=version)
        # Open output file for this sample
        if not os.path.exists(out_dir.format(SAMPLE=sample,VERSION=version)):
            os.makedirs(out_dir.format(SAMPLE=sample,VERSION=version))
        fileOut = ROOT.TFile.Open(out_dir.format(SAMPLE=sample,VERSION=version)+'/fakerates_MuTau_{SAMPLE}.root'.format(SAMPLE=sample), 'RECREATE')
        # Open input files for this sample, for each type of fake factors
        files = {}
        for name,fakeFactor in fakeFactors.items():
            files[name] = ROOT.TFile.Open(fakeFactor.root_file.format(FACTORS=fakeFactor.name,SAMPLE=sample,VERSION=fakeFactor.version))
        # Copy each declared histo in the / directory, for each of the different signal and inverted selections 
        for histo_template in histo_templates:
            for selection in selections:
                histos = []
                histoOut = None
                ## Check that all histos in the / directory are the same for all types of fake factors (because there is no fake factor applied here)
                ## Then write it in the output file
                for name,fakeFactor in fakeFactors.items():
                    file = files[name]
                    histos.append(file.Get(histo_template.format(SEL=selection)))
                    histos[-1].__class__ = ROOT.TH1F
                    if not histoOut: histoOut = histos[-1]
                    else:
                        # Check binning
                        if histoOut.GetNbinsX()!=histos[-1].GetNbinsX():
                            raise StandardError('ERROR: Different binnings for the different types of fake factors')
                        # Check bin contents
                        for b in xrange(1,histoOut.GetNbinsX()+1):
                            if histoOut.GetBinContent(b)!=histos[-1].GetBinContent(b):
                                raise StandardError('ERROR: Different bin contents in the root directory for the different types of fake factors')
                fileOut.cd()
                histoOut.Write()
        ## FIXME: need to be changed according to variable
        background_fractions = getBackgroundFractions()
        # Loop over each fake factor directory 
        for directory in fake_factors_regions['generic']:
            # Create directory in output file
            fileOut_dir = fileOut.mkdir(directory.format(TAG='Weight_Combined'))
            # weight and sum histos from the different types of fake factors
            for histo_template in histo_templates:
                for selection in selections:
                    histos = []
                    histoOut = None
                    histoFractionSum = None ## Used to check that the sum of background fractions is 1
                    ## FIXME: check that the sum of background fractions is equal to 1
                    for name,fakeFactor in fakeFactors.items():
                        # Retrieve histo in fake-factor directory
                        file = files[name]
                        histos.append(file.Get(directory.format(TAG=fakeFactor.directory_tag)+'/'+histo_template.format(SEL=selection)))
                        histos[-1].__class__ = ROOT.TH1F
                        # Check binning with background fractions
                        for background_fraction in background_fractions.values():
                            if histos[-1].GetNbinsX()!=background_fraction.GetNbinsX():
                                raise StandardError('ERROR: Different binnings ({BIN1} vs {BIN2})between {HISTO} and background fractions'.format(BIN1=histos[-1].GetNbinsX(),BIN2=background_fraction.GetNbinsX(),HISTO=histos[-1].GetName()))
                        if not histoOut: 
                            histoOut = histos[-1].Clone()
                            histoFractionSum = histos[-1].Clone('fraction_sums')
                            for b in xrange(0,histoOut.GetNbinsX()+2): # includes overflows
                                content = histoOut.GetBinContent(b)
                                background_fraction = sum([background_fractions[bf].GetBinContent(b) for bf in fakeFactor.background_fraction])
                                histoOut.SetBinContent(b,content*background_fraction)
                                histoFractionSum.SetBinContent(b,background_fraction)
                        else:
                            for b in xrange(0,histoOut.GetNbinsX()+2): # includes overflows
                                fractionOld = histoFractionSum.GetBinContent(b)
                                contentOld = histoOut.GetBinContent(b)
                                contentAdd = histos[-1].GetBinContent(b)
                                background_fraction = sum([background_fractions[bf].GetBinContent(b) for bf in fakeFactor.background_fraction])
                                histoOut.SetBinContent(b,contentOld + contentAdd*background_fraction)
                                histoFractionSum.SetBinContent(b,fractionOld+background_fraction)
                    ## Check the sum of background fractions
                    for b in range(0,histoFractionSum.GetNbinsX()+2): # includes overflows
                        content = histoFractionSum.GetBinContent(b)
                        if content>0. and abs(content-1.)>1.e-6: 
                            raise StandardError('ERROR: Sum of background fractions not equal to 1 ({SUM})'.format(SUM=content))
                        ## FIXME: add the check back
                        #elif content==0:
                            #print 'WARNING: Sum of fractions equal to 0 in bin {BIN}'.format(BIN=b)
                    fileOut_dir.cd()
                    histoOut.Write()

        ## Check that histos in root dir are the same 
        ## read histos for each fake factor
        ### Check binning
        ### Scale and sum each bin according to background fractions
        ## Write output
        fileOut.Close()
        for file in files.values():
            file.Close()
