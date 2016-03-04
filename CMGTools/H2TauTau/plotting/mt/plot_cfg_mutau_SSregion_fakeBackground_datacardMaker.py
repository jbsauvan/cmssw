import ROOT
import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg, BasicHistogramCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram, setSumWeights
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars
from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer,binning_svfitMass_mssm 

from FakeFactors import fake_factors_minimal, fake_factors_veryminimal, signal_selection, inverted_selection

int_lumi = 2094.2 # from Alexei's email


fakeFactorsTypes = ['CombinedSS']
histo_version = 'v_2_2016-03-04'

analysis_dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/Trees/mt/151215/'
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

for sample in all_samples:
    setSumWeights(sample, directory='MCWeighter')

## Output
version  = 'v160304'
plot_dir = "SSRegion/FakeRateEstimation/Datacards/{VERSION}/"

## templates for histogram and file names
histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/FakeFactorUncertainties_SS/'
histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/fakerates_MuTau_{SAMPLE}.root'
histo_template_name = '{DIR}hFakeRate_{SEL}_{VAR}'

fakeFactorStatShifts = {
    'QCDSS_Stat':[],
    'HighMT_Stat':[],
    'ZMuMu_Stat':[],
    'All_Stat':[],
}
fractionStatShifts = []

file = ROOT.TFile.Open(histo_file_template_name.format(SAMPLE='W_L'))
keys = file.GetListOfKeys()
for key in keys:
    keyname = key.GetName()
    if not key.IsFolder(): continue
    if not 'ShiftStat' in keyname: continue
    #if 'Up' in keyname: continue
    if 'FractionW' in keyname:
        extension = keyname.split('_ShiftStatFractionW_')[-1]
        fractionStatShifts.append('ShiftStatFractionW_'+extension)
    elif 'FractionQCD' in keyname:
        extension = keyname.split('_ShiftStatFractionQCD_')[-1]
        fractionStatShifts.append('ShiftStatFractionQCD_'+extension)
    elif 'QCDSS' in keyname:
        extension = keyname.split('_ShiftStatQCDSS_')[-1]
        fakeFactorStatShifts['QCDSS_Stat'].append('ShiftStatQCDSS_'+extension)
        fakeFactorStatShifts['All_Stat'].append('ShiftStatQCDSS_'+extension)
    elif 'HighMTRaw' in keyname:
        extension = keyname.split('_ShiftStatHighMTRaw_')[-1]
        fakeFactorStatShifts['HighMT_Stat'].append('ShiftStatHighMTRaw_'+extension)
        fakeFactorStatShifts['All_Stat'].append('ShiftStatHighMTRaw_'+extension)
    elif 'ZMuMu' in keyname:
        extension = keyname.split('_ShiftStatZMuMu_')[-1]
        fakeFactorStatShifts['ZMuMu_Stat'].append('ShiftStatZMuMu_'+extension)
        fakeFactorStatShifts['All_Stat'].append('ShiftStatZMuMu_'+extension)

file.Close()
for name,l in fakeFactorStatShifts.items():
    print name, len(l)
    print l

systematics = {}
systematics['CombinedSS'] = {
    'Nominal':'',
    'FakeFactorHighMT0Up': 'ShiftNonClosure_HighMTSS_0',
    'FakeFactorHighMT0Down': '',
    'FakeFactorHighMT1Up': 'ShiftNonClosure_HighMTSS_1',
    'FakeFactorHighMT1Down': '',
    'FakeFactorHighMT2Up': 'ShiftNonClosure_HighMTSS_2',
    'FakeFactorHighMT2Down': '',
    'FakeFactorHighMT3Up': 'ShiftNonClosure_HighMTSS_3',
    'FakeFactorHighMT3Down': '',
    'FakeFactorQCDSS0Up': 'ShiftNonClosure_QCDSS_0',
    'FakeFactorQCDSS0Down': '',
    'FakeFactorQCDSS1Up': 'ShiftNonClosure_QCDSS_1',
    'FakeFactorQCDSS1Down': '',
    'FakeFactorQCDSS2Up': 'ShiftNonClosure_QCDSS_2',
    'FakeFactorQCDSS2Down': '',
    'FakeFactorQCDSS3Up': 'ShiftNonClosure_QCDSS_3',
    'FakeFactorQCDSS3Down': '',
    'MTCorrStatUp': 'ShiftStatMTCorr_Up',
    'MTCorrStatDown': 'ShiftStatMTCorr_Down',
    'MTCorrBinUp': 'ShiftBinningMTCorr_Up',
    'MTCorrBinDown': 'ShiftBinningMTCorr_Down',
    'FractionsWUp':'ShiftFractionSSW_Up',
    'FractionsWDown':'ShiftFractionSSW_Down',
    'FractionsQCDUp':'ShiftFractionSSQCD_Up',
    'FractionsQCDDown':'ShiftFractionSSQCD_Down',
    'FractionsTTUp':'ShiftFractionSSTT_Up',
    'FractionsTTDown':'ShiftFractionSSTT_Down',
    #+fractionStatShifts
    #'AllStat': fakeFactorStatShifts['All_Stat'],
    #'FractionStat':fractionStatShifts,
}

# samples to be used
Name = "Name"
DirName = "DirName"
HistoDir = 'HistoDir'
XSection = "XSection"
SumWeights = "SumWeights"
IsData = 'IsData'
histo_samples = [
    {Name:'data_obs'    , DirName:'SingleMuon_Run2015D_v4'   , HistoDir:'Data_Run15D_v4', IsData:True},
    {Name:'data_obs'    , DirName:'SingleMuon_Run2015D_05Oct', HistoDir:'Data_Run15D_05Oct', IsData:True},
    {Name:'ZTT'         , DirName:'DYJetsToLL_M50_LO'        , HistoDir:'ZTT'          , XSection:sampleDict['ZJ'].xsec          , SumWeights:sampleDict['ZJ'].sumweights          },
    {Name:'ZL'          , DirName:'DYJetsToLL_M50_LO'        , HistoDir:'ZL'           , XSection:sampleDict['ZJ'].xsec          , SumWeights:sampleDict['ZJ'].sumweights          },
    {Name:'W'           , DirName:'WJetsToLNu_LO'            , HistoDir:'W_L', XSection:sampleDict['W'].xsec           , SumWeights:sampleDict['W'].sumweights           },
    {Name:'TT'          , DirName:'TT_pow'                   , HistoDir:'TT_L'         , XSection:sampleDict['TT'].xsec          , SumWeights:sampleDict['TT'].sumweights          },
    {Name:'T_tWch'      , DirName:'T_tWch'                   , HistoDir:'T_tWch_L'     , XSection:sampleDict['T_tWch'].xsec      , SumWeights:sampleDict['T_tWch'].sumweights      },
    {Name:'TBar_tWch'   , DirName:'TBar_tWch'                , HistoDir:'TBar_tWch_L'  , XSection:sampleDict['TBar_tWch'].xsec   , SumWeights:sampleDict['TBar_tWch'].sumweights   },
    #{Name:'QCD'         , DirName:'QCD_Mu15'           , HistoDir:'', XSection:sampleDict['QCD'].xsec         , SumWeights:sampleDict['QCD'].sumweights         },
    {Name:'ZZTo2L2Q'    , DirName:'ZZTo2L2Q'           , HistoDir:'ZZTo2L2Q_L'   , XSection:sampleDict['ZZTo2L2Q'].xsec    , SumWeights:sampleDict['ZZTo2L2Q'].sumweights    },
    {Name:'WZTo3L'      , DirName:'WZTo3L'             , HistoDir:'WZTo3L_L'     , XSection:sampleDict['WZTo3L'].xsec      , SumWeights:sampleDict['WZTo3L'].sumweights      },
    {Name:'WZTo2L2Q'    , DirName:'WZTo2L2Q'           , HistoDir:'WZTo2L2Q_L'   , XSection:sampleDict['WZTo2L2Q'].xsec    , SumWeights:sampleDict['WZTo2L2Q'].sumweights    },
    {Name:'WZTo1L3Nu'   , DirName:'WZTo1L3Nu'          , HistoDir:'WZTo1L3Nu_L'  , XSection:sampleDict['WZTo1L3Nu'].xsec   , SumWeights:sampleDict['WZTo1L3Nu'].sumweights   },
    {Name:'WZTo1L1Nu2Q' , DirName:'WZTo1L1Nu2Q'        , HistoDir:'WZTo1L1Nu2Q_L', XSection:sampleDict['WZTo1L1Nu2Q'].xsec , SumWeights:sampleDict['WZTo1L1Nu2Q'].sumweights },
    {Name:'VVTo2L2Nu'   , DirName:'VVTo2L2Nu'          , HistoDir:'VVTo2L2Nu_L'  , XSection:sampleDict['VVTo2L2Nu'].xsec   , SumWeights:sampleDict['VVTo2L2Nu'].sumweights   },
    {Name:'WWTo1L1Nu2Q' , DirName:'WWTo1L1Nu2Q'        , HistoDir:'WWTo1L1Nu2Q_L', XSection:sampleDict['WWTo1L1Nu2Q'].xsec , SumWeights:sampleDict['WWTo1L1Nu2Q'].sumweights },
    #{Name:'ZZTo4L'      , DirName:'ZZTo4L'           , XSection:sampleDict['ZZTo4L'].xsec      , SumWeights:sampleDict['ZZTo4L'].sumweights      }   ,
]



## Variables to use
variables = [
    VariableCfg(name='mvis_stdbins', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}'),
]

## Define fake factors and selections
global_selections = [
    "MT40_"
]

# Loop over fake factors
for fakeFactorsType in fakeFactorsTypes:
    fake_factors = fake_factors_veryminimal[fakeFactorsType]
    # Loop on variables
    for variable in variables:
        # Loop on global selections
        for global_selection in global_selections:
            # Loop on fake factors
            for fake_factor in fake_factors:
                mode = 'RECREATE'
                for sysGroup,systematic in systematics[fakeFactorsType].items():
                    ## Prepare histos configs
                    samples_tmp = []
                    fakes = []
                    for sample in histo_samples:
                        config = BasicHistogramCfg(name=sample[Name],
                                                 dir_name=sample[DirName],
                                                 ana_dir=analysis_dir,
                                                 histo_file_name=histo_file_template_name.format(SAMPLE=sample[HistoDir]),
                                                 histo_name=histo_template_name.format(
                                                     DIR='',
                                                     SEL=global_selection+signal_selection(fake_factor),
                                                     VAR=variable.name),
                                                 is_data=sample.get(IsData, False),
                                                 xsec=sample.get(XSection, 1),
                                                 sumweights=sample.get(SumWeights,1)
                                                 )

                        # Take fakes from the fake-factor directory, inverted isolation
                        config_fake = BasicHistogramCfg(name=sample[Name],
                                                 dir_name=sample[DirName],
                                                 ana_dir=analysis_dir,
                                                 histo_file_name=histo_file_template_name.format(SAMPLE=sample[HistoDir]),
                                                 histo_name=histo_template_name.format(
                                                     DIR=fake_factor+('' if systematic is '' else '_'+systematic)+'/',
                                                     SEL=global_selection+inverted_selection(fake_factor),
                                                     VAR=variable.name),
                                                 is_data=sample.get(IsData, False),
                                                 xsec=sample.get(XSection, 1),
                                                 sumweights=sample.get(SumWeights,1)
                                                 )
                        # Remove non-fake contamination from fake backgrounds
                        if config_fake.name!='data_obs': config_fake.scale = -1
                        fakes.append(copy.deepcopy(config_fake))
                        samples_tmp.append(copy.deepcopy(config))

                    # Add fakes component
                    samples_tmp.append( HistogramCfg(name='fakes_data', var=variable, cfgs=fakes, lumi=int_lumi) )
                    config = HistogramCfg(name='config', var=variable, cfgs=samples_tmp, lumi=int_lumi)
                    plot = createHistogram(config, sys=False, verbose=True)
                    plot.Group('VV', ['WWTo1L1Nu2Q', 'VVTo2L2Nu', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'WZTo3L', 'ZZTo2L2Q', 'T_tWch', 'TBar_tWch'])

                    HistDrawer.draw(plot, plot_dir=plot_dir.format(FAKETYPE=fakeFactorsType,VERSION=version)+'/'+global_selection+'/'+fake_factor+'/', plot_name=variable.name+'_'+sysGroup, SetLogy=False)
                    plot.WriteDataCard(
                        filename=plot_dir.format(FAKETYPE=fakeFactorsType,VERSION=version)+'/'+global_selection+'/'+fake_factor+'/datacard_{VAR}.root'.format(VAR=variable.name),
                        dir='mt_inclusive_'+sysGroup+'/' if sysGroup is not 'Nominal' else 'mt_inclusive/',
                        mode=mode
                    )
                    mode = 'UPDATE'
