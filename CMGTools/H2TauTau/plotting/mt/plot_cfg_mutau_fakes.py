import copy
import shelve
import ROOT

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50_LO, WJetsToLNu_LO, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, T_tWch, TBar_tWch, TToLeptons_tch_amcatnlo, TToLeptons_sch_amcatnlo

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, BasicHistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
#from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from HistDrawerFake import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars

from Data import CompatibilityData

#from CMGTools.H2TauTau.proto.plotter.Samples import samples

int_lumi = 1560.

## templates for histogram and file names
histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/'
histo_version = 'v_5_2015-11-25'
histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/fakerates_MuTau_{SAMPLE}.root'
histo_template_name = '{DIR}hFakeRate_{SEL}_{VAR}_vs_match5' ## '_vs_match5' is for gen_match=6

# samples to be used
Name = "Name"
XSection = "XSection"
SumWeights = "SumWeights"
samples = [
    #{Name:'ZL'       , XSection:DYJetsToLL_M50_LO.xSection, SumWeights:DYJetsToLL_M50_LO.nGenEvents},
    {Name:'ZJ'       , XSection:DYJetsToLL_M50_LO.xSection, SumWeights:DYJetsToLL_M50_LO.nGenEvents},
    {Name:'W'        , XSection:WJetsToLNu_LO.xSection    , SumWeights:WJetsToLNu_LO.nGenEvents},
    {Name:'TT'       , XSection:TT_pow.xSection           , SumWeights:TT_pow.nGenEvents},
    {Name:'T_tWch'   , XSection:T_tWch.xSection           , SumWeights:T_tWch.nGenEvents},
    {Name:'TBar_tWch', XSection:TBar_tWch.xSection        , SumWeights:TBar_tWch.nGenEvents},
    {Name:'WW'       , XSection:WWTo2L2Nu.xSection        , SumWeights:WWTo2L2Nu.nGenEvents},
    {Name:'WZ'       , XSection:WZp8.xSection             , SumWeights:WZp8.nGenEvents},
    {Name:'ZZ'       , XSection:ZZp8.xSection             , SumWeights:ZZp8.nGenEvents},
    {Name:'QCD'      , XSection:QCD_Mu15.xSection         , SumWeights:1.},
]
sample_groups = [['ZJ'], ['W'], ['TT'], ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'], ['QCD'], [s[Name] for s in samples]]



## Variables to use
variables = [
    VariableCfg(name='mvis', binning={'nbinsx':60, 'xmin':0, 'xmax':300}, unit='GeV', xtitle='m_{vis}'),
    #VariableCfg(name='mt'  , binning={'nbinsx':40, 'xmin':0, 'xmax':200}, unit='GeV', xtitle='m_{T}');
]

## Define fake factors and selections
fake_factors = [
    "Weight_Inclusive",
    "Weight_VsNVtx",
    "Weight_VsPt",
    "Weight_VsEta",
    "Weight_VsDecay",
    "Weight_VsPdgId",
]
signal_selection = "StandardIso"
inverted_selection = "InvertIso"

## Output 
plot_dir = "fakeplots/"
outFile = ROOT.TFile("fakeplots/histos.root", "RECREATE")


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
                                               histo_file_name=histo_file_template_name.format(SAMPLE=sample[Name]),
                                               histo_name='',
                                               rebin=2,
                                               xsec=sample[XSection],
                                               sumweights=sample[SumWeights]
                                              ))

    histo_config_dict = {cfg.name:cfg for cfg in histo_configs}



    ## Create Data/MC plots
    for fake_factor in fake_factors:
        for variable in variables:
            ## Store information about the plot
            data.append(CompatibilityData())
            data[-1].weight_name = fake_factor
            data[-1].variable = variable.name
            data[-1].binning = variable.binning
            for c in histo_configs:
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
                config.histo_name = histo_template_name.format(DIR='',SEL=signal_selection,VAR=variable.name)
                config.name = "Data"
                config.is_data = True ## treated as pseudo-data
                config.scale  = int_lumi*config.xsec/config.sumweights ## have to scale each component by hand
            # create background region config
            for config in configs_inverted:
                config.histo_name = histo_template_name.format(DIR=fake_factor+'/',SEL=inverted_selection,VAR=variable.name)
            # append both configs
            configs = configs_signal + configs_inverted

            name = "{VAR}_{WEIGHT}_{BACK}".format(VAR=variable.name, WEIGHT=fake_factor, BACK=backgrounds)
            cfg = HistogramCfg(name=name, var=variable, cfgs=configs, lumi=int_lumi)
            plot = createHistogram(cfg, verbose=True)
            plot.name = name
            plot.histPref['Data']['legend'] = 'Actual background'
            plot.histPref['ZJ']['legend'] = 'Z + Jets'
            if 'ZZ' in sample_group: plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
            HistDrawer.draw(plot, plot_dir=plot_dir)
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
    chi2Ondf = actual_background.Chi2Test(estimated_background, "WW CHI2/NDF P")
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

print "Number of stored compatibily tests = ", len(data_persist)
for dat in data_persist:
    print data_persist[dat], "\n"

data_persist.close()
outFile.Close()



