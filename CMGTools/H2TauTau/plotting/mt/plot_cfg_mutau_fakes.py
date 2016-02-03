import os
import copy
import shutil
import shelve
import ROOT
from FakeFactors import fake_factors_regions, signal_selections, inverted_selections

#from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50_LO, WJetsToLNu_LO, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, T_tWch, TBar_tWch, TToLeptons_tch_amcatnlo, TToLeptons_sch_amcatnlo
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, BasicHistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram, setSumWeights
#from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from HistDrawerFake import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars
from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer

from Data import CompatibilityData

#from CMGTools.H2TauTau.proto.plotter.Samples import samples


#fakeFactorsType = 'ZMuMu'
#histo_version = 'v_1_2016-02-02'
#
#fakeFactorsType = 'HighMT'
#histo_version = 'v_4_2016-02-02'
#
#fakeFactorsType = 'QCDSS'
#histo_version = 'v_1_2016-02-02'
#
fakeFactorsType = 'Combined'
histo_version = 'v_1_2016-02-03'

## input samples
int_lumi = 2094.2 # from Alexei's email
analysis_dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/Trees/mt/151215/'
tree_prod_name = 'H2TauTauTreeProducerTauMu'
samples_mc, samples_data, samples_tmp, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, tree_prod_name=tree_prod_name)

## Output
version  = 'v160202'
plot_dir = "fakeplots/FakeFactorType_{FAKETYPE}/{VERSION}/".format(FAKETYPE=fakeFactorsType,VERSION=version)
publish_plots = True
publication_dir = "/afs/cern.ch/user/j/jsauvan/www/H2Taus/FakeRate/BackgroundEstimation/FakeFactorType_{FAKETYPE}/{VERSION}/".format(FAKETYPE=fakeFactorsType,VERSION=version)

## templates for histogram and file names
histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/{FAKETYPE}'.format(FAKETYPE=fakeFactorsType)
histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/fakerates_MuTau_{SAMPLE}.root'
histo_template_name = '{DIR}hFakeRate_{SEL}_{VAR}_vs_match5' ## '_vs_match5' is for gen_match=6

# samples to be used
Name = "Name"
DirName = "DirName"
XSection = "XSection"
SumWeights = "SumWeights"
samples = [
    {Name:'ZJ'          , DirName:'DYJetsToLL_M50_LO', XSection:sampleDict['ZJ'].xsec          , SumWeights:sampleDict['ZJ'].sumweights          },
    {Name:'W'           , DirName:'WJetsToLNu_LO'    , XSection:sampleDict['W'].xsec           , SumWeights:sampleDict['W'].sumweights           },
    {Name:'TT'          , DirName:'TT_pow'           , XSection:sampleDict['TT'].xsec          , SumWeights:sampleDict['TT'].sumweights          },
    {Name:'T_tWch'      , DirName:'T_tWch'           , XSection:sampleDict['T_tWch'].xsec      , SumWeights:sampleDict['T_tWch'].sumweights      },
    {Name:'TBar_tWch'   , DirName:'TBar_tWch'        , XSection:sampleDict['TBar_tWch'].xsec   , SumWeights:sampleDict['TBar_tWch'].sumweights   },
    {Name:'QCD'         , DirName:'QCD_Mu15'         , XSection:sampleDict['QCD'].xsec         , SumWeights:sampleDict['QCD'].sumweights         },
    {Name:'ZZTo2L2Q'    , DirName:'ZZTo2L2Q'         , XSection:sampleDict['ZZTo2L2Q'].xsec    , SumWeights:sampleDict['ZZTo2L2Q'].sumweights    },
    {Name:'WZTo3L'      , DirName:'WZTo3L'           , XSection:sampleDict['WZTo3L'].xsec      , SumWeights:sampleDict['WZTo3L'].sumweights      },
    {Name:'WZTo2L2Q'    , DirName:'WZTo2L2Q'         , XSection:sampleDict['WZTo2L2Q'].xsec    , SumWeights:sampleDict['WZTo2L2Q'].sumweights    },
    {Name:'WZTo1L3Nu'   , DirName:'WZTo1L3Nu'        , XSection:sampleDict['WZTo1L3Nu'].xsec   , SumWeights:sampleDict['WZTo1L3Nu'].sumweights   },
    {Name:'WZTo1L1Nu2Q' , DirName:'WZTo1L1Nu2Q'      , XSection:sampleDict['WZTo1L1Nu2Q'].xsec , SumWeights:sampleDict['WZTo1L1Nu2Q'].sumweights },
    {Name:'VVTo2L2Nu'   , DirName:'VVTo2L2Nu'        , XSection:sampleDict['VVTo2L2Nu'].xsec   , SumWeights:sampleDict['VVTo2L2Nu'].sumweights   },
    {Name:'WWTo1L1Nu2Q' , DirName:'WWTo1L1Nu2Q'      , XSection:sampleDict['WWTo1L1Nu2Q'].xsec , SumWeights:sampleDict['WWTo1L1Nu2Q'].sumweights },
    #{Name:'ZZTo4L'      , DirName:'ZZTo4L'           , XSection:sampleDict['ZZTo4L'].xsec      , SumWeights:sampleDict['ZZTo4L'].sumweights      }   ,
]
sample_groups = [['ZJ'], ['W'], ['TT'], ['WWTo1L1Nu2Q', 'VVTo2L2Nu', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'WZTo3L', 'ZZTo2L2Q', 'T_tWch', 'TBar_tWch'], ['QCD'], [s[Name] for s in samples]]



## Variables to use
variables = [
    #VariableCfg(name='mvis', binning={'nbinsx':60, 'xmin':0, 'xmax':300}, unit='GeV', xtitle='m_{vis}'),
    VariableCfg(name='mvis_stdbins', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}'),
    #VariableCfg(name='mt'  , binning={'nbinsx':40, 'xmin':0, 'xmax':200}, unit='GeV', xtitle='m_{T}'),
]

## Define fake factors and selections
global_selections = [
    "",
    "MT40_"
]

fake_factors = fake_factors_regions[fakeFactorsType]


## Output 
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
outFile = ROOT.TFile(plot_dir+"/histos.root", "RECREATE")

for global_selection in global_selections:
    for fake_factor in fake_factors:
        if publish_plots:
           if not os.path.exists(publication_dir+"/"+global_selection+"/"+fake_factor):
               os.makedirs(publication_dir+"/"+global_selection+"/"+fake_factor) 
           shutil.copy("/afs/cern.ch/user/j/jsauvan/www//index.php.back", publication_dir+"/"+global_selection+"/"+fake_factor+"/index.php")


plots = []
data = []
written_histos = []
## Loop over groups of samples
for sample_group in sample_groups:
    ## Create histo configs
    histo_configs = []
    for sample in samples:
        if not sample[Name] in sample_group: continue
        histo_configs.append(BasicHistogramCfg(name=sample[Name],
                                               dir_name=sample[DirName],
                                               ana_dir=analysis_dir,
                                               histo_file_name=histo_file_template_name.format(SAMPLE=sample[Name]),
                                               histo_name='',
                                               rebin=1,
                                               xsec=sample[XSection],
                                               sumweights=sample[SumWeights]
                                              ))
        ## SumWeights seems to be not correctly filled
        ## Filled them from SkimAnalyzerCount pickle file
        setSumWeights(histo_configs[-1], directory='MCWeighter')


    histo_config_dict = {cfg.name:cfg for cfg in histo_configs}



    ## Create Data/MC plots
    # Loop over global selections (e.g., with and without mT cut)
    for global_selection in global_selections:
        ## Loop over all the different types of fake factors (1D, 2D, etc.)
        for fake_factor in fake_factors:
            ## Loop over variables (currently only m_vis)
            for variable in variables:
                ## Store information about the plot
                data.append(CompatibilityData())
                data[-1].global_selection = global_selection
                data[-1].weight_name = fake_factor
                data[-1].variable = variable.name
                data[-1].binning = variable.binning
                for c in histo_configs:
                    if variable.name=='mvis': c.rebin=2
                    else: c.rebin = 1
                    data[-1].backgrounds.append(c.name)
                #
                backgrounds = ""
                for b in data[-1].backgrounds:
                    backgrounds += b + "."
                backgrounds = backgrounds[:-1]
                #
                ## Produce the plot
                configs_signal   = copy.deepcopy(histo_configs)
                configs_inverted = copy.deepcopy(histo_configs)
                # create signal region config
                for config in configs_signal:
                    config.histo_name = histo_template_name.format(DIR='',SEL=global_selection+signal_selections[fake_factor],VAR=variable.name)
                    config.name = "Data"
                    config.is_data = True ## treated as pseudo-data
                    config.scale  = int_lumi*config.xsec/config.sumweights ## have to scale each component by hand
                # create background region config
                for config in configs_inverted:
                    config.histo_name = histo_template_name.format(DIR=fake_factor+'/',SEL=global_selection+inverted_selections[fake_factor],VAR=variable.name)
                # append both configs
                configs = configs_signal + configs_inverted

                name = "{VAR}_{SEL}{WEIGHT}_{BACK}".format(SEL=global_selection,VAR=variable.name, WEIGHT=fake_factor, BACK=backgrounds)
                cfg = HistogramCfg(name=name, var=variable, cfgs=configs, lumi=int_lumi)
                plot = createHistogram(cfg, verbose=True)
                plot.name = name
                plot.histPref['Data']['legend'] = 'Actual background'
                plot.histPref['ZJ']['legend'] = 'Z + Jets'
                if 'VVTo2L2Nu' in sample_group: plot.Group('VV', ['WWTo1L1Nu2Q', 'VVTo2L2Nu', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'WZTo3L', 'ZZTo2L2Q', 'T_tWch', 'TBar_tWch'])
                HistDrawer.draw(plot, plot_dir=plot_dir)
                if publish_plots:
                    for ext in [".png",".eps",".pdf",".C"]:
                        shutil.copy(plot_dir+"/"+plot.name+ext, publication_dir+"/"+global_selection+"/"+fake_factor)
                plots.append(plot)
                ## Save sums in signal regions and background regions
                outFile.cd()

                histo_estimated = plot.GetStack().totalHist.weighted.Clone("{VAR}_estimated_{BACK}_{WEIGHT}".format(VAR=variable.name,BACK=backgrounds,WEIGHT=fake_factor))
                histo_estimated.__class__ = ROOT.TH1F
                if not histo_estimated.GetName() in written_histos: histo_estimated.Write() # Background region
                written_histos.append(histo_estimated.GetName())
                for hist in plot._SortedHistograms():  # Have to retrieve signal region by hand (the non-stacked component)
                    if hist.stack is False:
                        histo_actual = hist.obj.Clone("{VAR}_actual_{BACK}".format(VAR=variable.name,BACK=backgrounds))
                        histo_actual.__class__ = ROOT.TH1F
                        if not histo_actual.GetName() in written_histos: histo_actual.Write()
                        written_histos.append(histo_actual.GetName())

## Make test compatibility between actual background in signal region
## and background estimated from background region
for dat,plot in zip(data,plots):
    name = plot.name
    estimated_background = plot.GetStack().totalHist.weighted
    actual_background = None
    for hist in plot._SortedHistograms():  # Have to retrieve signal region by hand (the non-stacked component)
        if hist.stack is False:
            actual_background = hist.obj
    pvalue   = actual_background.Chi2Test(estimated_background, "WW P")
    chi2Ondf = actual_background.Chi2Test(estimated_background, "WW CHI2/NDF")
    dat.chi2.append(pvalue)
    dat.chi2.append(chi2Ondf)
    estimated_integralError = ROOT.Double(0.)
    estimated_integral = estimated_background.IntegralAndError(1, estimated_background.GetNbinsX()+1, estimated_integralError)
    actual_integralError = ROOT.Double(0.)
    actual_integral = actual_background.IntegralAndError(1, actual_background.GetNbinsX()+1, actual_integralError)
    chi2Norm = (estimated_integral-actual_integral)**2/(estimated_integralError**2+actual_integralError**2)
    dat.chi2.append(chi2Norm)


## Store persistently the compatibility results
data_persist = shelve.open(plot_dir+"/background_compatibility.db")
data_persist.clear()
for dat in data:
    if str(hash(dat)) in data_persist:
        print "Hash value", hash(dat), " already exists"
    data_persist[str(hash(dat))] = dat.toDict()

print "Number of stored compatibility tests = ", len(data_persist)
for dat in data_persist:
    print data_persist[dat], "\n"

data_persist.close()
outFile.Close()



