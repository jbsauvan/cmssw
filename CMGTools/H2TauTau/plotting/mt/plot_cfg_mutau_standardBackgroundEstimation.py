import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram, setSumWeights
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars
from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer

int_lumi = 2094.2 # from Alexei's email

## Output
version  = 'v160229'
plot_dir = "signalRegion/StandardBackground_FromTree/{VERSION}/"

total_weight = 'weight'


cuts = {}

inc_cut = '&&'.join([cat_Inc])
inc_cut += '&& l2_decayModeFinding'

cuts['inclusive'] = inc_cut + '&& l1_charge != l2_charge && !(met_pt < 0.15 && met_phi > 0. && met_phi < 1.8)'

#cuts['lowMT'] = cuts['inclusive'] + '&& mt < 40'
cuts['highMT'] = cuts['inclusive'] + '&& mt > 70'


qcd_from_same_sign = True

analysis_dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/Trees/mt/151215/'
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

for sample in all_samples:
    setSumWeights(sample, directory='MCWeighter')

if qcd_from_same_sign:
    samples_qcdfromss = [s for s in all_samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

    scale = 1.06

    for sample in samples_ss:
        sample.scale = scale
        if sample.name != 'data_obs':
            # Subtract background from data
            sample.scale = -scale

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, lumi=int_lumi)

    samples_qcdfromss.append(qcd)


#variables = getVars(['mvis', 'mt'])
variables = [
    #VariableCfg(name='mvis', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}'),
    VariableCfg(name='mt', binning={'nbinsx':14, 'xmin':70, 'xmax':210}, unit='GeV', xtitle='m_{T}')
]


outputMode = 'RECREATE'
for cut_name in cuts:
    if qcd_from_same_sign and not 'SS' in cut_name :
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples_qcdfromss, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    else:
        cfg_example = HistogramCfg(name='example', var=None, cfgs=all_samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)
        

    cfg_example.cut = cuts[cut_name]
    if qcd_from_same_sign and not 'SS' in cut_name:
        qcd.cut = cuts[cut_name].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    for variable in variables:
        cfg_example.var = variable
        if qcd_from_same_sign:
            qcd.var = variable
        
        plot = createHistogram(cfg_example, verbose=True)
        plot.Group('VV', ['WWTo1L1Nu2Q', 'VVTo2L2Nu', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'WZTo3L', 'ZZTo2L2Q', 'T_tWch', 'TBar_tWch'])
        HistDrawer.draw(plot, plot_dir=plot_dir.format(VERSION=version)+'/'+cut_name, SetLogy=False)
        plot.WriteDataCard(filename=plot_dir.format(VERSION=version)+'/datacard_mutau_standardBackground.root', mode=outputMode, dir='{SEL}_{VAR}'.format(SEL=cut_name, VAR=variable.name))
        if outputMode=='RECREATE': outputMode = 'UPDATE'
