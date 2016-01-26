import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram, setSumWeights
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars
from CMGTools.H2TauTau.proto.plotter.cut import Cut
from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

#from CMGTools.H2TauTau.proto.plotter.Samples import samples
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
#from samples import samples

int_lumi = 2094.2 # from Alexei's email

total_weight = 'weight'
#total_weight = 'weight * ' + getPUWeight()

print total_weight

cuts = {}

inc_sig_mu1 = Cut('l1_reliso05<0.1')
inc_sig_mu1 &= Cut('l1_muonid_medium>0.5')
inc_sig_mu1 &= Cut('l1_pt>19')
#
inc_sig_mu2 = Cut('l2_reliso05<0.1')
inc_sig_mu2 &= Cut('l2_muonid_medium>0.5')
inc_sig_mu2 &= Cut('l2_pt>10')
#
inc_sig_dimu = Cut('l1_charge*l2_charge<0')
#
inc_sig_tau = Cut('tau1_againstMuon3>1.5')
inc_sig_tau &= Cut('tau1_againstElectronMVA5>0.5')
inc_sig_tau &= Cut('tau1_pt>20')
inc_sig_tau &= Cut('tau1_decayModeFinding')

inc_sig = inc_sig_mu1 & inc_sig_mu2 & inc_sig_dimu & inc_sig_tau

cuts['Zjet_Tree'] = inc_sig


# -> Command line
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mm/190116/'
tree_prod_name = 'H2TauTauTreeProducerMuMu'
data_dir = analysis_dir
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, tree_prod_name=tree_prod_name)


for sample in all_samples:
    #sample.ana_dir = analysis_dir
    #sample.tree_prod_name = tree_prod_name
    ## SumWeights seems to be not correctly filled
    ## Filled them from SkimAnalyzerCount pickle file
    setSumWeights(sample)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = [
    VariableCfg(name='tau1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau p_{T}'),
    VariableCfg(name='tau1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='tau #eta'),
    VariableCfg(name='tau1_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx':100, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau delta-beta corr. 3-hit isolation'), 
    VariableCfg(name='n_vertices', binning={'nbinsx':51, 'xmin':-0.5, 'xmax':50.5}, unit=None, xtitle='N_{vertices}'),
]

for name,cut in cuts.items():
    cfg_example = HistogramCfg(name='example', var=None, cfgs=all_samples, cut=str(cut), lumi=int_lumi, weight=total_weight)

    for variable in variables:
        cfg_example.var = variable
        plot = createHistogram(cfg_example, verbose=True)
        plot.Group('VV', ['ZZTo4L','ZZTo2L2Q','WZTo3L','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','VVTo2L2Nu','WWTo1L1Nu2Q', 'T_tWch', 'TBar_tWch'])
        HistDrawer.draw(plot, plot_dir='controlregions/{CUT}/'.format(CUT=name))

        #plot.WriteDataCard(filename='datacard_mt.root', dir='mt_' + cut_name)









#import os
#import copy
#import shutil
#import shelve
#import ROOT

#from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow, DYJetsToLL_M50_LO, WJetsToLNu_LO, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, T_tWch, TBar_tWch, TToLeptons_tch_amcatnlo, TToLeptons_sch_amcatnlo

#from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, BasicHistogramCfg, VariableCfg
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
#from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram, setSumWeights
##from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
#from HistDrawerFake import HistDrawer
#from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars

#from Data import CompatibilityData

##from CMGTools.H2TauTau.proto.plotter.Samples import samples

### input samples
#int_lumi = 1560.
#analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mt/18112015/'

### Publication on web
#publish_plots = True
#publication_dir = "/afs/cern.ch/user/j/jsauvan/www/H2Taus/FakeRate/ControlRegions/HighMT/"

### templates for histogram and file names
#histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuTau_WJetsContamination/'
#histo_version = 'v_1_2016-01-18'
#histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/fakerates_MuTau_WJetsContamination_{SAMPLE}.root'
#histo_template_name = '{DIR}hFakeRate_{SEL}_{VAR}' ## '_vs_match5' is for gen_match=6

## samples to be used
#Name = "Name"
#DirName = "DirName"
#XSection = "XSection"
#SumWeights = "SumWeights"
#samples = [
    #{Name:'Z'        , DirName:'DYJetsToLL_M50_LO', XSection:DYJetsToLL_M50_LO.xSection, SumWeights:DYJetsToLL_M50_LO.nGenEvents},
    #{Name:'W'        , DirName:'WJetsToLNu_LO'    , XSection:WJetsToLNu_LO.xSection    , SumWeights:WJetsToLNu_LO.nGenEvents},
    #{Name:'TT'       , DirName:'TT_pow'           , XSection:TT_pow.xSection           , SumWeights:TT_pow.nGenEvents},
    #{Name:'T_tWch'   , DirName:'T_tWch'           , XSection:T_tWch.xSection           , SumWeights:T_tWch.nGenEvents},
    #{Name:'TBar_tWch', DirName:'TBar_tWch'        , XSection:TBar_tWch.xSection        , SumWeights:TBar_tWch.nGenEvents},
    #{Name:'WW'       , DirName:'WWTo2L2Nu'        , XSection:WWTo2L2Nu.xSection        , SumWeights:WWTo2L2Nu.nGenEvents},
    #{Name:'WZ'       , DirName:'WZ'               , XSection:WZp8.xSection             , SumWeights:WZp8.nGenEvents},
    #{Name:'ZZ'       , DirName:'ZZp8'             , XSection:ZZp8.xSection             , SumWeights:ZZp8.nGenEvents},
    #{Name:'QCD'      , DirName:'QCD_Mu15'         , XSection:QCD_Mu15.xSection         , SumWeights:1.},
#]
#sample_groups = [['Z'], ['W'], ['TT'], ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'], ['QCD'], [s[Name] for s in samples]]



### Variables to use
#variables = [
    #VariableCfg(name='mvis', binning={'nbinsx':60, 'xmin':0, 'xmax':300}, unit='GeV', xtitle='m_{vis}'),
    ##VariableCfg(name='mt'  , binning={'nbinsx':40, 'xmin':0, 'xmax':200}, unit='GeV', xtitle='m_{T}');
#]

### Define fake factors and selections
#selections = [
    #"HighMT_OS_",
#]


### Output 
#plot_dir = "controlregions/HighMT/"
#outFile = ROOT.TFile(plot_dir+"/histos.root", "RECREATE")

#for selection in selections:
    #if publish_plots:
       #if not os.path.exists(publication_dir+"/"+selection):
           #os.makedirs(publication_dir+"/"+global_selection) 
       #shutil.copy("/afs/cern.ch/user/j/jsauvan/www/index.php.back", publication_dir+"/"+global_selection+"/index.php")


#plots = []
#data = []
#written_histos = []
### Loop over groups of samples
#for sample_group in sample_groups:
    ### Create histo configs
    #histo_configs = []
    #for sample in samples:
        #if not sample[Name] in sample_group: continue
        #histo_configs.append(BasicHistogramCfg(name=sample[Name],
                                               #dir_name=sample[DirName],
                                               #ana_dir=analysis_dir,
                                               #histo_file_name=histo_file_template_name.format(SAMPLE=sample[Name]),
                                               #histo_name='',
                                               #rebin=2,
                                               #xsec=sample[XSection],
                                               #sumweights=sample[SumWeights]
                                              #))
        ### SumWeights seems to be not correctly filled
        ### Filled them from SkimAnalyzerCount pickle file
        #setSumWeights(histo_configs[-1])


    #histo_config_dict = {cfg.name:cfg for cfg in histo_configs}



    ### Create Data/MC plots
    ## Loop over global selections (e.g., with and without mT cut)
    #for global_selection in global_selections:
        ### Loop over all the different types of fake factors (1D, 2D, etc.)
        #for fake_factor in fake_factors:
            ### Loop over variables (currently only m_vis)
            #for variable in variables:
                ### Store information about the plot
                #data.append(CompatibilityData())
                #data[-1].global_selection = global_selection
                #data[-1].weight_name = fake_factor
                #data[-1].variable = variable.name
                #data[-1].binning = variable.binning
                #for c in histo_configs:
                    #data[-1].backgrounds.append(c.name)
                ##
                #backgrounds = ""
                #for b in data[-1].backgrounds:
                    #backgrounds += b + "."
                #backgrounds = backgrounds[:-1]
                ##
                ### Produce the plot
                #configs_signal   = copy.deepcopy(histo_configs)
                #configs_inverted = copy.deepcopy(histo_configs)
                ## create signal region config
                #for config in configs_signal:
                    #config.histo_name = histo_template_name.format(DIR='',SEL=global_selection+signal_selections[fake_factor],VAR=variable.name)
                    #config.name = "Data"
                    #config.is_data = True ## treated as pseudo-data
                    #config.scale  = int_lumi*config.xsec/config.sumweights ## have to scale each component by hand
                ## create background region config
                #for config in configs_inverted:
                    #config.histo_name = histo_template_name.format(DIR=fake_factor+'/',SEL=global_selection+inverted_selections[fake_factor],VAR=variable.name)
                ## append both configs
                #configs = configs_signal + configs_inverted

                #name = "{VAR}_{SEL}{WEIGHT}_{BACK}".format(SEL=global_selection,VAR=variable.name, WEIGHT=fake_factor, BACK=backgrounds)
                #cfg = HistogramCfg(name=name, var=variable, cfgs=configs, lumi=int_lumi)
                #plot = createHistogram(cfg, verbose=True)
                #plot.name = name
                #plot.histPref['Data']['legend'] = 'Actual background'
                #plot.histPref['ZJ']['legend'] = 'Z + Jets'
                #if 'ZZ' in sample_group: plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
                #HistDrawer.draw(plot, plot_dir=plot_dir)
                #if publish_plots:
                    #for ext in [".png",".eps",".pdf",".C"]:
                        #shutil.copy(plot_dir+"/"+plot.name+ext, publication_dir+"/"+global_selection+"/"+fake_factor)
                #plots.append(plot)
                ### Save sums in signal regions and background regions
                #outFile.cd()

                #histo_estimated = plot.GetStack().totalHist.weighted.Clone("{VAR}_estimated_{BACK}_{WEIGHT}".format(VAR=variable.name,BACK=backgrounds,WEIGHT=fake_factor))
                #histo_estimated.__class__ = ROOT.TH1F
                #if not histo_estimated.GetName() in written_histos: histo_estimated.Write() # Background region
                #written_histos.append(histo_estimated.GetName())
                #for hist in plot._SortedHistograms():  # Have to retrieve signal region by hand (the non-stacked component)
                    #if hist.stack is False:
                        #histo_actual = hist.obj.Clone("{VAR}_actual_{BACK}".format(VAR=variable.name,BACK=backgrounds))
                        #histo_actual.__class__ = ROOT.TH1F
                        #if not histo_actual.GetName() in written_histos: histo_actual.Write()
                        #written_histos.append(histo_actual.GetName())

### Make test compatibility between actual background in signal region
### and background estimated from background region
#for dat,plot in zip(data,plots):
    #name = plot.name
    #estimated_background = plot.GetStack().totalHist.weighted
    #actual_background = None
    #for hist in plot._SortedHistograms():  # Have to retrieve signal region by hand (the non-stacked component)
        #if hist.stack is False:
            #actual_background = hist.obj
    #pvalue   = actual_background.Chi2Test(estimated_background, "WW P")
    #chi2Ondf = actual_background.Chi2Test(estimated_background, "WW CHI2/NDF")
    #dat.chi2.append(pvalue)
    #dat.chi2.append(chi2Ondf)
    #estimated_integralError = ROOT.Double(0.)
    #estimated_integral = estimated_background.IntegralAndError(1, estimated_background.GetNbinsX()+1, estimated_integralError)
    #actual_integralError = ROOT.Double(0.)
    #actual_integral = actual_background.IntegralAndError(1, actual_background.GetNbinsX()+1, actual_integralError)
    #chi2Norm = (estimated_integral-actual_integral)**2/(estimated_integralError**2+actual_integralError**2)
    #dat.chi2.append(chi2Norm)


### Store persistently the compatibility results
#data_persist = shelve.open(plot_dir+"/background_compatibility.db")
#data_persist.clear()
#for dat in data:
    #if str(hash(dat)) in data_persist:
        #print "Hash value", hash(dat), " already exists"
    #data_persist[str(hash(dat))] = dat.toDict()

#print "Number of stored compatibility tests = ", len(data_persist)
#for dat in data_persist:
    #print data_persist[dat], "\n"

#data_persist.close()
#outFile.Close()



