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


analysis_dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/Trees/mt/151215/'
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

for sample in all_samples:
    setSumWeights(sample, directory='MCWeighter')

## Output
version  = 'v160308'
plot_dir = "signalRegion/FakeRateEstimation_postfit/{VERSION}/"

histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/CMSSW/CMSSW_7_1_21_patch2/src/CombineHarvester/HttFakes/scripts/output/LIMITS/OS/{VERSION}/mt/'.format(VERSION=version)
histo_file_template_name = histo_base_dir+'/shapes_postfit.root'
histo_template_name = 'mt_inclusive_postfit/{SAMPLE}'

## Raw histos
histo_version = 'v_8_2016-03-01'
histo_base_dir_raw = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/FakeFactorUncertainties/'
histo_file_template_name_raw = histo_base_dir_raw+'/{SAMPLE}/'+histo_version+'/fakerates_MuTau_{SAMPLE}.root'
histo_template_name_raw = '{DIR}hFakeRate_MT40_Iso_Medium_{VAR}'


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
    {Name:'ZTT'         },
    {Name:'ZL'          },
    {Name:'W'           },
    {Name:'TT'          },
    {Name:'VV'          },
    {Name:'fakes_data'  },
]



## Variables to use
variable = VariableCfg(name='mvis_stdbins', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}')



## Prepare histos configs
samples_tmp = []
for sample in histo_samples:
    if sample[Name] is not 'data_obs':
        config = BasicHistogramCfg(name=sample[Name],
                                 dir_name='',
                                 ana_dir=analysis_dir,
                                 histo_file_name=histo_file_template_name.format(SAMPLE=sample),
                                 histo_name=histo_template_name.format(SAMPLE=sample[Name]),
                                 is_data=sample.get(IsData, False),
                                 xsec=1.,
                                 sumweights=1.
                                 )
    else:
        config = BasicHistogramCfg(name=sample[Name],
                                 dir_name=sample.get(DirName,''),
                                 ana_dir=analysis_dir,
                                 histo_file_name=histo_file_template_name_raw.format(SAMPLE=sample[HistoDir]),
                                 histo_name=histo_template_name_raw.format(DIR='',VAR=variable.name),
                                 is_data=sample.get(IsData, False),
                                 xsec=sample.get(XSection, 1),
                                 sumweights=sample.get(SumWeights,1)
                                 )
    samples_tmp.append(copy.deepcopy(config))
#
config = HistogramCfg(name='config', var=variable, cfgs=samples_tmp, lumi=1.)
plot = createHistogram(config, sys=False, verbose=True)
HistDrawer.draw(plot, plot_dir=plot_dir.format(VERSION=version), plot_name=variable.name, SetLogy=False)
