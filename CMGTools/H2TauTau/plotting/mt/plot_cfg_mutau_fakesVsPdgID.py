import os
import copy
import shutil
import shelve
import ROOT

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50_LO, WJetsToLNu_LO, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, T_tWch, TBar_tWch, TToLeptons_tch_amcatnlo, TToLeptons_sch_amcatnlo

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, BasicHistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram, setSumWeights
#from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from HistDrawerFake import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars

from Data import CompatibilityData

#from CMGTools.H2TauTau.proto.plotter.Samples import samples

## input samples
int_lumi = 1560.
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mt/18112015/'

## Publication on web
publish_plots = True
publication_dir = "/afs/cern.ch/user/j/jsauvan/www/H2Taus/FakeRate/BackgroundEstimation_PdgIdSplit/"

## templates for histogram and file names
histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau/'
histo_version = 'v_10_2015-12-09'
histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/fakerates_MuTau_{SAMPLE}.root'
histo_template_name = '{DIR}hFakeRate_{SEL}_{VAR}_vs_pdgid{PDGID}' ## 

# samples to be used
Name = "Name"
DirName = "DirName"
XSection = "XSection"
SumWeights = "SumWeights"
samples = [
    {Name:'ZJ'       , DirName:'DYJetsToLL_M50_LO', XSection:DYJetsToLL_M50_LO.xSection, SumWeights:DYJetsToLL_M50_LO.nGenEvents},
    {Name:'W'        , DirName:'WJetsToLNu_LO'    , XSection:WJetsToLNu_LO.xSection    , SumWeights:WJetsToLNu_LO.nGenEvents},
    {Name:'TT'       , DirName:'TT_pow'           , XSection:TT_pow.xSection           , SumWeights:TT_pow.nGenEvents},
    {Name:'T_tWch'   , DirName:'T_tWch'           , XSection:T_tWch.xSection           , SumWeights:T_tWch.nGenEvents},
    {Name:'TBar_tWch', DirName:'TBar_tWch'        , XSection:TBar_tWch.xSection        , SumWeights:TBar_tWch.nGenEvents},
    {Name:'WW'       , DirName:'WWTo2L2Nu'        , XSection:WWTo2L2Nu.xSection        , SumWeights:WWTo2L2Nu.nGenEvents},
    {Name:'WZ'       , DirName:'WZ'               , XSection:WZp8.xSection             , SumWeights:WZp8.nGenEvents},
    {Name:'ZZ'       , DirName:'ZZp8'             , XSection:ZZp8.xSection             , SumWeights:ZZp8.nGenEvents},
    {Name:'QCD'      , DirName:'QCD_Mu15'         , XSection:QCD_Mu15.xSection         , SumWeights:1.},
]
#sample_groups = [['ZJ'], ['W'], ['TT'], ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'], ['QCD'], [s[Name] for s in samples]]
sample_groups = [['TT'], ['QCD'], ['W']]

# pdgIds to plot
pdgIds = [1,2,3,4,5,21]
#pdgIds = [1,2]

## Variables to use
variables = [
    VariableCfg(name='mvis', binning={'nbinsx':60, 'xmin':0, 'xmax':300}, unit='GeV', xtitle='m_{vis}'),
    #VariableCfg(name='mt'  , binning={'nbinsx':40, 'xmin':0, 'xmax':200}, unit='GeV', xtitle='m_{T}');
]

## Define fake factors and selections
global_selections = [
    "",
    "MT40_"
]

fake_factors = [
    ## IsoRaw > 1.5 GeV -> IsoRaw < 1.5 GeV 
    "Weight_IsoRaw_1_5_Inclusive",
    "Weight_IsoRaw_1_5_VsPt",
    "Weight_IsoRaw_1_5_VsDecay",
    "Weight_IsoRaw_1_5_VsPdgId",
    "Weight_IsoRaw_1_5_VsPtDecay",
    "Weight_IsoRaw_1_5_VsPtPdgId",
    ## !IsoMedium -> IsoMedium 
    "Weight_Iso_Medium_Inclusive",
    "Weight_Iso_Medium_VsPt",
    "Weight_Iso_Medium_VsDecay",
    "Weight_Iso_Medium_VsPdgId",
    "Weight_Iso_Medium_VsPtDecay",
    "Weight_Iso_Medium_VsPtPdgId",
]


signal_selections = {
    ## IsoRaw > 1.5 GeV -> IsoRaw < 1.5 GeV 
    "Weight_IsoRaw_1_5_Inclusive":"IsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPt":"IsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsDecay":"IsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPdgId":"IsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPtDecay":"IsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPtPdgId":"IsoRaw_1_5",
    ## !IsoMedium -> IsoMedium 
    "Weight_Iso_Medium_Inclusive":"Iso_Medium",
    "Weight_Iso_Medium_VsPt":"Iso_Medium",
    "Weight_Iso_Medium_VsDecay":"Iso_Medium",
    "Weight_Iso_Medium_VsPdgId":"Iso_Medium",
    "Weight_Iso_Medium_VsPtDecay":"Iso_Medium",
    "Weight_Iso_Medium_VsPtPdgId":"Iso_Medium",
}

inverted_selections = {
    ## IsoRaw > 1.5 GeV -> IsoRaw < 1.5 GeV 
    "Weight_IsoRaw_1_5_Inclusive":"InvertIsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPt":"InvertIsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsDecay":"InvertIsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPdgId":"InvertIsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPtEta":"InvertIsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPtDecay":"InvertIsoRaw_1_5",
    "Weight_IsoRaw_1_5_VsPtPdgId":"InvertIsoRaw_1_5",
    ## !IsoMedium -> IsoMedium 
    "Weight_Iso_Medium_Inclusive":"InvertIso_Medium",
    "Weight_Iso_Medium_VsPt":"InvertIso_Medium",
    "Weight_Iso_Medium_VsDecay":"InvertIso_Medium",
    "Weight_Iso_Medium_VsPdgId":"InvertIso_Medium",
    "Weight_Iso_Medium_VsPtDecay":"InvertIso_Medium",
    "Weight_Iso_Medium_VsPtPdgId":"InvertIso_Medium",
}




## Output 
plot_dir = "fakeVsPdgIdPlots/"
outFile = ROOT.TFile("fakeVsPdgIdPlots/histos.root", "RECREATE")

for global_selection in global_selections:
    for fake_factor in fake_factors:
        if publish_plots:
           if not os.path.exists(publication_dir+"/"+global_selection+"/"+fake_factor):
               os.makedirs(publication_dir+"/"+global_selection+"/"+fake_factor) 
           shutil.copy(publication_dir+"/index.php.back", publication_dir+"/"+global_selection+"/"+fake_factor+"/index.php")


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
                                               rebin=2,
                                               xsec=sample[XSection],
                                               sumweights=sample[SumWeights]
                                              ))
        ## SumWeights seems to be not correctly filled
        ## Filled them from SkimAnalyzerCount pickle file
        setSumWeights(histo_configs[-1])


    histo_config_dict = {cfg.name:cfg for cfg in histo_configs}



    ## Create Data/MC plots
    ## Loop over samples split by pdgID
    for pdgId in pdgIds:
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
                    backgrounds = ""
                    for c in histo_configs:
                        backgrounds += c.name + "."
                        data[-1].backgrounds.append(c.name+"_"+str(pdgId))
                    #
                    backgrounds = backgrounds[:-1]
                    #
                    ## Produce the plot
                    configs_signal   = copy.deepcopy(histo_configs)
                    configs_inverted = copy.deepcopy(histo_configs)
                    # create signal region config
                    for config in configs_signal:
                        config.histo_name = histo_template_name.format(DIR='',SEL=global_selection+signal_selections[fake_factor],VAR=variable.name,PDGID=pdgId-1)
                        config.name = "Data"
                        config.is_data = True ## treated as pseudo-data
                        config.scale  = int_lumi*config.xsec/config.sumweights ## have to scale each component by hand
                    # create background region config
                    for config in configs_inverted:
                        config.histo_name = histo_template_name.format(DIR=fake_factor+'/',SEL=global_selection+inverted_selections[fake_factor],VAR=variable.name,PDGID=pdgId-1)
                    # append both configs
                    configs = configs_signal + configs_inverted

                    name = "{VAR}_{SEL}{WEIGHT}_{BACK}_{PDGID}".format(SEL=global_selection,VAR=variable.name, WEIGHT=fake_factor, BACK=backgrounds,PDGID=pdgId)
                    cfg = HistogramCfg(name=name, var=variable, cfgs=configs, lumi=int_lumi)
                    plot = createHistogram(cfg, verbose=True)
                    plot.name = name
                    plot.histPref['Data']['legend'] = 'Actual background'
                    plot.histPref['ZJ']['legend'] = 'Z + Jets'
                    #plot.histPref['TT']['legend'] = 't#bar{t}, pdg='+str(pdgId)
                    #plot.histPref['QCD*']['legend'] = 'QCD, id={}'.format(pdgId)
                    if 'ZZ' in sample_group: plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
                    HistDrawer.draw(plot, plot_dir=plot_dir)
                    if publish_plots:
                        for ext in [".png",".eps",".pdf",".C"]:
                            shutil.copy(plot_dir+"/"+plot.name+ext, publication_dir+"/"+global_selection+"/"+fake_factor)
                    plots.append(plot)
                    ## Save sums in signal regions and background regions
                    outFile.cd()

                    histo_estimated = plot.GetStack().totalHist.weighted.Clone("{VAR}_estimated_{BACK}_{PDGID}_{WEIGHT}".format(VAR=variable.name,BACK=backgrounds,WEIGHT=fake_factor,PDGID=pdgId))
                    histo_estimated.__class__ = ROOT.TH1F
                    if not histo_estimated.GetName() in written_histos: histo_estimated.Write() # Background region
                    written_histos.append(histo_estimated.GetName())
                    for hist in plot._SortedHistograms():  # Have to retrieve signal region by hand (the non-stacked component)
                        if hist.stack is False:
                            histo_actual = hist.obj.Clone("{VAR}_actual_{BACK}_{PDGID}".format(VAR=variable.name,BACK=backgrounds,PDGID=pdgId))
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
    chiNorm = 999.
    if estimated_integralError+actual_integralError>0: chi2Norm = (estimated_integral-actual_integral)**2/(estimated_integralError**2+actual_integralError**2)
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



