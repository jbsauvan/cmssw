import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars

from CMGTools.H2TauTau.proto.plotter.Samples import samples
#from samples import samples

int_lumi = 1560.

cuts = {}

inc_cut = '&&'.join([cat_Inc])
inc_cut += '&& l2_decayModeFinding'

cuts['inclusive'] = inc_cut + '&& l1_charge != l2_charge'
# cuts['OSlowMT'] = inc_cut + '&& l1_charge != l2_charge && mt<40'
# cuts['SSlowMT'] = inc_cut + '&& l1_charge == l2_charge && mt<40'

# cuts['OShighMT'] = inc_cut + '&& l1_charge != l2_charge && mt>40'
# cuts['SShighMT'] = inc_cut + '&& l1_charge == l2_charge && mt>40'

inv_cuts = {}
for cut in cuts:
    inv_cuts[cut+'invmu'] = cuts[cut].replace('l1_reliso05<0.1', 'l1_reliso05>0.1')
    inv_cuts[cut+'invtau'] = cuts[cut].replace('ll2_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits>1.5')

# cuts = inv_cuts

qcd_from_same_sign = True

# -> Command line
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mt/18112015'
tree_prod_name = 'H2TauTauTreeProducerTauMu'
data_dir = analysis_dir


if qcd_from_same_sign:
    samples_qcdfromss = [s for s in samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

    scale = 1.06

    for sample in samples_ss:
        sample.scale = scale
        if sample.name != 'Data':
            # Subtract background from data
            sample.scale = -scale

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, lumi=int_lumi)

    samples_qcdfromss.append(qcd)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = all_vars
variables = getVars(['mt'])
variables = [
    VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
]

for cut_name in cuts:
    if  qcd_from_same_sign and not 'SS' in cut_name :
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples_qcdfromss, cut=inc_cut, lumi=int_lumi)
    else:
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi)
        

    cfg_example.cut = cuts[cut_name]
    if qcd_from_same_sign and 'OS' in cut_name:
        qcd.cut = cuts[cut_name].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    for variable in variables:
        cfg_example.var = variable
        if qcd_from_same_sign:
            qcd.var = variable # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
        
        plot = createHistogram(cfg_example, verbose=True)
        plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
        # plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
        # plot.Group('ZLL', ['Ztt_ZL', 'Ztt_ZJ'], style=plot.Hist('Ztt_ZL').style)
        HistDrawer.draw(plot, plot_dir='plots/'+cut_name)

        plot.WriteDataCard(filename='datacard_mt.root', dir='mt_' + cut_name)
