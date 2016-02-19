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

#total_weight = ''
total_weight = 'weight'
#total_weight = 'weight * ' + getPUWeight()

print total_weight

cuts = {}


#qcdcut = '!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_againstMuon3>1.5 && l2_againstElectronMVA5>0.5 && l2_pt> 20'
#qcdcut += ' && l1_muonid_medium>0.5 && l1_pt>19 '
#qcdcut += ' && l2_decayModeFinding'
#qcdcut += " && ( !( pfmet_pt < 0.2 && pfmet_phi > 0 && pfmet_phi < 2 ) ) "   # remove events at MET=0
#qcdcut += " && l1_charge == l2_charge "
#qcdcut += " && mt<40 "

#inc_sig = Cut(qcdcut)

inc_sig_mu = Cut('l1_muonid_medium>0.5')
inc_sig_mu &= Cut('l1_pt>19')
#
inc_sig_tau = Cut('l2_againstMuon3>1.5')
inc_sig_tau &= Cut('l2_againstElectronMVA5>0.5')
inc_sig_tau &= Cut('l2_decayModeFinding')
inc_sig_tau &= Cut('l2_pt>20')
#
inc_sig_event = Cut('l1_charge*l2_charge>0')
inc_sig_event &= Cut('mt<40')
inc_sig_event &= Cut('veto_dilepton<0.5')
inc_sig_event &= Cut('veto_thirdlepton<0.5')
inc_sig_event &= Cut('veto_otherlepton<0.5')
inc_sig_event &= Cut('( !( pfmet_pt < 0.2 && pfmet_phi > 0 && pfmet_phi < 2 ) )')# remove events at MET=0


isomu_medium = Cut('l1_reliso05<0.12 && l1_reliso05>0.05')
isomu_anti   = Cut('l1_reliso05>0.12')
isomu   = Cut('l1_reliso05<0.05')

inc_sig = inc_sig_mu & inc_sig_tau  & inc_sig_event & isomu 
inc_sig_medium = inc_sig_mu & inc_sig_tau  & inc_sig_event & isomu_medium
inc_sig_anti = inc_sig_mu & inc_sig_tau  & inc_sig_event & isomu_anti

cuts['QCDSS_Tree'] = inc_sig
cuts['QCDSS_IsoMuMedium_Tree'] = inc_sig_medium
cuts['QCDSS_IsoMuAnti_Tree'] = inc_sig_anti


# -> Command line
analysis_dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/Trees/mt/151215/'
tree_prod_name = 'H2TauTauTreeProducerTauMu'
data_dir = analysis_dir
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, tree_prod_name=tree_prod_name)


for sample in all_samples:
    #sample.ana_dir = analysis_dir
    #sample.tree_prod_name = tree_prod_name
    ## SumWeights seems to be not correctly filled
    ## Filled them from SkimAnalyzerCount pickle file
    setSumWeights(sample, directory='MCWeighter')

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = [
    VariableCfg(name='mvis', binning={'nbinsx':60, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='m_{vis}'),
    VariableCfg(name='mt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T}'),
    #VariableCfg(name='l2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau p_{T}'),
    #VariableCfg(name='l2_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='tau #eta'),
    #VariableCfg(name='l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx':100, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau delta-beta corr. 3-hit isolation'), 
    #VariableCfg(name='n_vertices', binning={'nbinsx':51, 'xmin':-0.5, 'xmax':50.5}, unit=None, xtitle='N_{vertices}'),
    VariableCfg(name='l1_reliso05', binning={'nbinsx':500, 'xmin':0., 'xmax':1.0}, unit='', xtitle='iso^{#mu}'),
]

for name,cut in cuts.items():
    cfg_example = HistogramCfg(name='example', var=None, cfgs=all_samples, cut=str(cut), lumi=int_lumi, weight=total_weight)

    for variable in variables:
        cfg_example.var = variable
        plot = createHistogram(cfg_example, verbose=True)
        plot.Group('VV', ['ZZTo2L2Q','WZTo3L','WZTo2L2Q','WZTo1L3Nu','WZTo1L1Nu2Q','VVTo2L2Nu','WWTo1L1Nu2Q', 'T_tWch', 'TBar_tWch'])
        HistDrawer.draw(plot, plot_dir='controlregions/{CUT}/'.format(CUT=name))
        #HistDrawer.draw(plot, plot_dir='controlregions/{CUT}/'.format(CUT=name), SetLogy=True)

        plot.WriteDataCard(filename='controlregions/{CUT}/datacard_{VAR}.root'.format(CUT=name,VAR=variable.name))



