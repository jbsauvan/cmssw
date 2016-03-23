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



def setPlotStyle():
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat()
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetFrameLineWidth(1)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.13)
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetPadRightMargin(0.03)

    ROOT.gStyle.SetLabelFont(42,"X")
    ROOT.gStyle.SetLabelFont(42,"Y")
    ROOT.gStyle.SetLabelSize(0.04,"X")
    ROOT.gStyle.SetLabelSize(0.04,"Y")
    ROOT.gStyle.SetLabelOffset(0.01,"Y")
    ROOT.gStyle.SetTickLength(0.03,"X")
    ROOT.gStyle.SetTickLength(0.03,"Y")
    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetTickLength(0.04 ,"Z")

    ROOT.gStyle.SetTitleSize(0.1)
    ROOT.gStyle.SetTitleFont(42,"X")
    ROOT.gStyle.SetTitleFont(42,"Y")
    ROOT.gStyle.SetTitleSize(0.07,"X")
    ROOT.gStyle.SetTitleSize(0.07,"Y")
    ROOT.gStyle.SetTitleOffset(0.8,"X")
    ROOT.gStyle.SetTitleOffset(0.9,"Y")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("3.2f")
    ROOT.gROOT.ForceStyle()


analysis_dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/Trees/mt/151215/'
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

for sample in all_samples:
    setSumWeights(sample, directory='MCWeighter')

## Output
version  = 'v160313'
plot_dir = "signalRegion/FakeRateEstimation_postfit_sys/{VERSION}/"

histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/CMSSW/CMSSW_7_4_15/src/CMGTools/H2TauTau/plotting/mt/'
histo_file_template_name = histo_base_dir+'/shapes_postfit_sys.root'
histo_template_name = '{SAMPLE}'

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

sysdirs = ['mt_inclusive_FakeFactorHighMTUp', 'mt_inclusive_FakeFactorQCDSSUp']


## Variables to use
variable = VariableCfg(name='mvis_stdbins', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}')


setPlotStyle()

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
plot = createHistogram(config, sys=True, verbose=True)
# Add systematics
samples_sys_tmp = {}
for sys in sysdirs:
    samples_sys_tmp[sys] = []
    for sample in histo_samples:
        if sample[Name] is not 'data_obs':
            config = BasicHistogramCfg(name=sample[Name],
                                     dir_name='',
                                     ana_dir=analysis_dir,
                                     histo_file_name=histo_file_template_name.format(SAMPLE=sample),
                                     histo_name=sys+'/'+histo_template_name.format(SAMPLE=sample[Name]),
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
        samples_sys_tmp[sys].append(copy.deepcopy(config))

plot_sys = {}
config_sys = {}
for sys in sysdirs:
    config_sys[sys] = HistogramCfg(name='config_'+sys, var=variable, cfgs=samples_sys_tmp[sys], lumi=1.)
    plot_sys[sys] = createHistogram(config_sys[sys], verbose=True)
    
setPlotStyle()
plot.AddSystematics(plot_sys)
HistDrawer.draw(plot, plot_dir=plot_dir.format(VERSION=version), plot_name=variable.name, SetLogy=False)
