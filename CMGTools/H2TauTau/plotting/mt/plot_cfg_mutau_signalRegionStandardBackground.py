import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg, BasicHistogramCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram, setSumWeights
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars
from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer,binning_svfitMass_mssm 

from FakeFactors import fake_factors_minimal, signal_selection, inverted_selection

int_lumi = 2094.2 # from Alexei's email


analysis_dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/Trees/mt/151215/'
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

for sample in all_samples:
    setSumWeights(sample, directory='MCWeighter')

## Output
version  = 'v160208'
plot_dir = "signalRegion/StandardBackground/{VERSION}/"

## templates for histogram and file names
histo_version = 'v_1_2016-02-08'
histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau_Signal/'
histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/h2tau_MuTau_{SAMPLE}.root'
histo_template_name = 'hFakeRate_{SEL}_{VAR}'

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
    {Name:'ZTT'         , DirName:'DYJetsToLL_M50_LO'  , HistoDir:'ZTT'          , XSection:sampleDict['ZJ'].xsec          , SumWeights:sampleDict['ZJ'].sumweights          },
    {Name:'ZL'          , DirName:'DYJetsToLL_M50_LO'  , HistoDir:'ZL'           , XSection:sampleDict['ZJ'].xsec          , SumWeights:sampleDict['ZJ'].sumweights          },
    {Name:'ZJ'          , DirName:'DYJetsToLL_M50_LO'  , HistoDir:'ZJ'           , XSection:sampleDict['ZJ'].xsec          , SumWeights:sampleDict['ZJ'].sumweights          },
    {Name:'W'           , DirName:'WJetsToLNu_LO'      , HistoDir:'W'            , XSection:sampleDict['W'].xsec           , SumWeights:sampleDict['W'].sumweights           },
    {Name:'W'           , DirName:'WJetsToLNu_LO'      , HistoDir:'W_L'          , XSection:sampleDict['W'].xsec           , SumWeights:sampleDict['W'].sumweights           },
    {Name:'TT'          , DirName:'TT_pow'             , HistoDir:'TT_L'         , XSection:sampleDict['TT'].xsec          , SumWeights:sampleDict['TT'].sumweights          },
    {Name:'TT'          , DirName:'TT_pow'             , HistoDir:'TT'         , XSection:sampleDict['TT'].xsec          , SumWeights:sampleDict['TT'].sumweights          },
    {Name:'T_tWch'      , DirName:'T_tWch'             , HistoDir:'T_tWch_L'     , XSection:sampleDict['T_tWch'].xsec      , SumWeights:sampleDict['T_tWch'].sumweights      },
    {Name:'T_tWch'      , DirName:'T_tWch'             , HistoDir:'T_tWch'     , XSection:sampleDict['T_tWch'].xsec      , SumWeights:sampleDict['T_tWch'].sumweights      },
    {Name:'TBar_tWch'   , DirName:'TBar_tWch'          , HistoDir:'TBar_tWch_L'  , XSection:sampleDict['TBar_tWch'].xsec   , SumWeights:sampleDict['TBar_tWch'].sumweights   },
    {Name:'TBar_tWch'   , DirName:'TBar_tWch'          , HistoDir:'TBar_tWch'  , XSection:sampleDict['TBar_tWch'].xsec   , SumWeights:sampleDict['TBar_tWch'].sumweights   },
    {Name:'ZZTo2L2Q'    , DirName:'ZZTo2L2Q'           , HistoDir:'ZZTo2L2Q_L'   , XSection:sampleDict['ZZTo2L2Q'].xsec    , SumWeights:sampleDict['ZZTo2L2Q'].sumweights    },
    {Name:'ZZTo2L2Q'    , DirName:'ZZTo2L2Q'           , HistoDir:'ZZTo2L2Q'   , XSection:sampleDict['ZZTo2L2Q'].xsec    , SumWeights:sampleDict['ZZTo2L2Q'].sumweights    },
    {Name:'WZTo3L'      , DirName:'WZTo3L'             , HistoDir:'WZTo3L_L'     , XSection:sampleDict['WZTo3L'].xsec      , SumWeights:sampleDict['WZTo3L'].sumweights      },
    {Name:'WZTo3L'      , DirName:'WZTo3L'             , HistoDir:'WZTo3L'     , XSection:sampleDict['WZTo3L'].xsec      , SumWeights:sampleDict['WZTo3L'].sumweights      },
    {Name:'WZTo2L2Q'    , DirName:'WZTo2L2Q'           , HistoDir:'WZTo2L2Q_L'   , XSection:sampleDict['WZTo2L2Q'].xsec    , SumWeights:sampleDict['WZTo2L2Q'].sumweights    },
    {Name:'WZTo2L2Q'    , DirName:'WZTo2L2Q'           , HistoDir:'WZTo2L2Q'   , XSection:sampleDict['WZTo2L2Q'].xsec    , SumWeights:sampleDict['WZTo2L2Q'].sumweights    },
    {Name:'WZTo1L3Nu'   , DirName:'WZTo1L3Nu'          , HistoDir:'WZTo1L3Nu_L'  , XSection:sampleDict['WZTo1L3Nu'].xsec   , SumWeights:sampleDict['WZTo1L3Nu'].sumweights   },
    {Name:'WZTo1L3Nu'   , DirName:'WZTo1L3Nu'          , HistoDir:'WZTo1L3Nu'  , XSection:sampleDict['WZTo1L3Nu'].xsec   , SumWeights:sampleDict['WZTo1L3Nu'].sumweights   },
    {Name:'WZTo1L1Nu2Q' , DirName:'WZTo1L1Nu2Q'        , HistoDir:'WZTo1L1Nu2Q_L', XSection:sampleDict['WZTo1L1Nu2Q'].xsec , SumWeights:sampleDict['WZTo1L1Nu2Q'].sumweights },
    {Name:'WZTo1L1Nu2Q' , DirName:'WZTo1L1Nu2Q'        , HistoDir:'WZTo1L1Nu2Q', XSection:sampleDict['WZTo1L1Nu2Q'].xsec , SumWeights:sampleDict['WZTo1L1Nu2Q'].sumweights },
    {Name:'VVTo2L2Nu'   , DirName:'VVTo2L2Nu'          , HistoDir:'VVTo2L2Nu_L'  , XSection:sampleDict['VVTo2L2Nu'].xsec   , SumWeights:sampleDict['VVTo2L2Nu'].sumweights   },
    {Name:'VVTo2L2Nu'   , DirName:'VVTo2L2Nu'          , HistoDir:'VVTo2L2Nu'  , XSection:sampleDict['VVTo2L2Nu'].xsec   , SumWeights:sampleDict['VVTo2L2Nu'].sumweights   },
    {Name:'WWTo1L1Nu2Q' , DirName:'WWTo1L1Nu2Q'        , HistoDir:'WWTo1L1Nu2Q_L', XSection:sampleDict['WWTo1L1Nu2Q'].xsec , SumWeights:sampleDict['WWTo1L1Nu2Q'].sumweights },
    {Name:'WWTo1L1Nu2Q' , DirName:'WWTo1L1Nu2Q'        , HistoDir:'WWTo1L1Nu2Q', XSection:sampleDict['WWTo1L1Nu2Q'].xsec , SumWeights:sampleDict['WWTo1L1Nu2Q'].sumweights },
    #{Name:'ZZTo4L'      , DirName:'ZZTo4L'           , XSection:sampleDict['ZZTo4L'].xsec      , SumWeights:sampleDict['ZZTo4L'].sumweights      }   ,
]



## Variables to use
variables = [
    #VariableCfg(name='mvis', binning={'nbinsx':60, 'xmin':0, 'xmax':300}, unit='GeV', xtitle='m_{vis}'),
    VariableCfg(name='mvis_stdbins', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}'),
    VariableCfg(name='mvis_mssmbins', binning=binning_svfitMass_mssm, unit='GeV', xtitle='m_{vis}'),
    VariableCfg(name='mt'  , binning={'nbinsx':40, 'xmin':0, 'xmax':200}, unit='GeV', xtitle='m_{T}'),
]

## Define  selections
global_selections = [
    "{SIGN}Iso_Medium",
    "{SIGN}MT40_Iso_Medium"
]


# Loop on variables
for variable in variables:
    # Loop on global selections
    for global_selection in global_selections:
        ## Prepare histos configs
        samples_tmp = []
        qcd = []
        for sample in histo_samples:
            config = BasicHistogramCfg(name=sample[Name],
                                     dir_name=sample[DirName],
                                     ana_dir=analysis_dir,
                                     histo_file_name=histo_file_template_name.format(SAMPLE=sample[HistoDir]),
                                     histo_name=histo_template_name.format(SEL=global_selection.format(SIGN=''),VAR=variable.name),
                                     is_data=sample.get(IsData, False),
                                     xsec=sample.get(XSection, 1),
                                     sumweights=sample.get(SumWeights,1)
                                     )
            # Take QCD from SS region
            config_qcd = BasicHistogramCfg(name=sample[Name],
                                     dir_name=sample[DirName],
                                     ana_dir=analysis_dir,
                                     histo_file_name=histo_file_template_name.format(SAMPLE=sample[HistoDir]),
                                     histo_name=histo_template_name.format(SEL=global_selection.format(SIGN='SS_'),VAR=variable.name),
                                     is_data=sample.get(IsData, False),
                                     xsec=sample.get(XSection, 1),
                                     sumweights=sample.get(SumWeights,1)
                                     )

            if sample[Name]=='data_obs': config_qcd.scale = 1.06
            else: config_qcd.scale = -1.06
            qcd.append(config_qcd)
            samples_tmp.append(config)
        # Add QCD component
        samples_tmp.append( HistogramCfg(name='QCD', var=variable, cfgs=qcd, lumi=int_lumi) )
        config = HistogramCfg(name='config', var=variable, cfgs=samples_tmp, lumi=int_lumi)
        plot = createHistogram(config, verbose=True)
        plot.Group('VV', ['WWTo1L1Nu2Q', 'VVTo2L2Nu', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'WZTo3L', 'ZZTo2L2Q', 'T_tWch', 'TBar_tWch'])
        HistDrawer.draw(plot, plot_dir=plot_dir.format(VERSION=version)+'/'+global_selection.format(SIGN=''), SetLogy=False)
