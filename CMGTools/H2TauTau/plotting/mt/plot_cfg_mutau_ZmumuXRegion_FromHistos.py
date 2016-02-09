import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg, BasicHistogramCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram, setSumWeights
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars
from CMGTools.H2TauTau.proto.plotter.cut import Cut

#from CMGTools.H2TauTau.proto.plotter.Samples import samples
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.SamplesFromHisto import createSampleListsFromHisto
#from samples import samples

int_lumi = 2094.2 # from Alexei's email

## Output
version = 'v160205'
plot_dir = "controlregions/ZJet/{VERSION}/".format(VERSION=version)
publish_plots = False
publication_dir = "/afs/cern.ch/user/j/jsauvan/www/H2Taus/FakeRate/ControlRegions/ZJet/{VERSION}/".format(VERSION=version)

## templates for histogram and file names
#histo_version = 'v_2_2016-01-28'
histo_version = 'v_3_2016-02-05'
histo_base_dir = '/afs/cern.ch/work/j/jsauvan/Projects/Htautau_Run2/Histos/StudyFakeRate/MuMu/'
histo_file_template_name = histo_base_dir+'/{SAMPLE}/'+histo_version+'/fakerates_ZMuMu_{SAMPLE}.root'
histo_template_name = '{DIR}hFakeRate_{SEL}_{VAR}' 



# -> Command line
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mm/190116/'
tree_prod_name = 'H2TauTauTreeProducerMuMu'
data_dir = analysis_dir
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleListsFromHisto(analysis_dir=analysis_dir, tree_prod_name=tree_prod_name)


selections = []
selections.append('NoIso')


#for sample in all_samples:
    ### SumWeights seems to be not correctly filled
    ### Filled them from SkimAnalyzerCount pickle file
    #setSumWeights(sample)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = [
    VariableCfg(name='l1l2_mass', binning={'nbinsx':70, 'xmin':50., 'xmax':120.}, unit='GeV', xtitle='m_{#mu#mu}'),
    VariableCfg(name='l1l2_highmass', binning={'nbinsx':45, 'xmin':0., 'xmax':900.}, unit='GeV', xtitle='m_{#mu#mu}'),
    VariableCfg(name='l1l2_pt', binning={'nbinsx':20, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{#mu#mu}'),
    VariableCfg(name='nvertices', binning={'nbinsx':12, 'xmin':0., 'xmax':40.}, unit='', xtitle='N_{PV}'),
    VariableCfg(name='tau_pt', binning={'nbinsx':14, 'xmin':20., 'xmax':200.}, unit='GeV', xtitle='p_{T}^{#tau}'),
    VariableCfg(name='tau_pt_fixedbin', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='p_{T}^{#tau}'),
    VariableCfg(name='tau_iso', binning={'nbinsx':200, 'xmin':0., 'xmax':20.}, unit='GeV', xtitle='iso^{#tau}'),
    VariableCfg(name='tau_decayMode', binning={'nbinsx':15, 'xmin':-0.5, 'xmax':14.5}, unit='', xtitle='decay mode'),
]

sampleHistoNames = {
    'DYJetsToLL_M50_LO':'Z',
    'WJetsToLNu_LO':'W',
    'TT_pow_ext':'TT',
    'T_tWch':'T_tWch',
    'TBar_tWch':'TBar_tWch',
    'QCD_Mu15':'QCD',
    'SingleMuon_Run2015D_v4':'Data_Run15D_v4',
    'SingleMuon_Run2015D_05Oct':'Data_Run15D_05Oct',
    'ZZTo2L2Q':'ZZTo2L2Q',
    'WZTo3L':'WZTo3L',
    'WZTo2L2Q':'WZTo2L2Q',
    'WZTo1L3Nu':'WZTo1L3Nu',
    'WZTo1L1Nu2Q':'WZTo1L1Nu2Q',
    'VVTo2L2Nu':'VVTo2L2Nu',
    'WWTo1L1Nu2Q':'WWTo1L1Nu2Q',
}



for selection in selections:
    for variable in variables:
        samples_copy = copy.deepcopy(all_samples)
        for sample in samples_copy:
            sampleName = sampleHistoNames[sample.dir_name]
            sample.histo_file_name = histo_file_template_name.format(SAMPLE=sampleName) 
            #sample.histo_name = histo_template_name.format(DIR='NoPUReweight/',SEL=selection,VAR=variable.name)
            sample.histo_name = histo_template_name.format(DIR='',SEL=selection,VAR=variable.name)
        cfg = HistogramCfg(name='{SEL}_{VAR}'.format(SEL=selection,VAR=variable), var=variable, cfgs=samples_copy, lumi=int_lumi)
        plot = createHistogram(cfg, verbose=True)
        #plot.Group('VV', ['ZZTo4L','ZZTo2L2Q','WZTo3L','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','VVTo2L2Nu','WWTo1L1Nu2Q', 'T_tWch', 'TBar_tWch'])
        plot.Group('VV', ['ZZTo2L2Q','WZTo3L','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','VVTo2L2Nu','WWTo1L1Nu2Q', 'T_tWch', 'TBar_tWch'])
        HistDrawer.draw(plot, plot_dir=plot_dir, plot_name='{VAR}_{SEL}_Log'.format(VAR=variable.name,SEL=selection), SetLogy=True)
        HistDrawer.draw(plot, plot_dir=plot_dir, plot_name='{VAR}_{SEL}_Lin'.format(VAR=variable.name,SEL=selection), SetLogy=False)










