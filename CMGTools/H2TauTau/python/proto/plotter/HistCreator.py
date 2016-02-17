import pickle

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg,BasicHistogramCfg
from CMGTools.H2TauTau.proto.plotter.DataMCSysPlot import DataMCSysPlot

from CMGTools.RootTools.DataMC.Histogram import Histogram

from ROOT import TH1F, TFile, gROOT

def initHist(hist, vcfg):
    hist.Sumw2()
    xtitle = vcfg.xtitle
    if vcfg.unit:
        xtitle += ' ({})'.format(vcfg.unit)
    hist.GetXaxis().SetTitle(xtitle)
    hist.SetStats(False)

def createHistogram(hist_cfg, all_stack=False, verbose=False):
    '''Method to create actual histogram (DataMCPlot) instance from histogram 
    config.
    '''
    plot = DataMCSysPlot(hist_cfg.var.name)
    plot.lumi = hist_cfg.lumi
    vcfg = hist_cfg.var
    for cfg in hist_cfg.cfgs:
        # First check whether it's a sub-histo or not
        if isinstance(cfg, HistogramCfg):
            hist = createHistogram(cfg, all_stack=True)
            hist._BuildStack(hist._SortedHistograms(), ytitle='Events')

            total_hist = plot.AddHistogram(cfg.name, hist.stack.totalHist.weighted, stack=True)

            if cfg.norm_cfg is not None:
                norm_hist = createHistogram(cfg.norm_cfg, all_stack=True)
                norm_hist._BuildStack(norm_hist._SortedHistograms(), ytitle='Events')
                total_hist.Scale(hist.stack.integral/total_hist.Yield())

            if cfg.total_scale is not None:
                total_hist.Scale(cfg.total_scale)
        elif isinstance(cfg, BasicHistogramCfg):
            print "Opening file", cfg.histo_file_name
            histo_file = TFile.Open(cfg.histo_file_name)
            print "Retrieving histo", cfg.histo_name
            hist = histo_file.Get(cfg.histo_name)
            hist.__class__ = TH1F
            hist.SetDirectory(0)
            hist.SetTitle("")
            initHist(hist, vcfg)
            histo_file.Close()
            gROOT.cd()
            #
            stack = all_stack or (not cfg.is_data and not cfg.is_signal)
            #
            if cfg.rebin>1: hist.Rebin(cfg.rebin)
            hist.Scale(cfg.scale)
            #
            if cfg.name in plot:
                plot[cfg.name].Add(Histogram(cfg.name, hist))
            else:
                plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)

            if not cfg.is_data:
                plot_hist.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights) 
        else:
            # It's a sample cfg
            hname = '_'.join([hist_cfg.name, cfg.name, vcfg.name, cfg.dir_name])
            if 'xmin' in vcfg.binning:
                hist = TH1F(hname, '', vcfg.binning['nbinsx'], 
                    vcfg.binning['xmin'], vcfg.binning['xmax'])
            else:
                hist = TH1F(hname, '', len(vcfg.binning)-1, vcfg.binning)

            initHist(hist, vcfg)

            file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

            ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose)

            norm_cut = hist_cfg.cut
            shape_cut = hist_cfg.cut

            if cfg.norm_cut:
                norm_cut = cfg.norm_cut

            if cfg.shape_cut:
                shape_cut = cfg.shape_cut

            weight = hist_cfg.weight
            if cfg.weight_expr:
                weight = '*'.join([weight, cfg.weight_expr])

            if hist_cfg.weight:
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we=weight)
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we=weight)


            ttree.Project(hname, vcfg.drawname, norm_cut)

            if shape_cut != norm_cut:
                scale = hist.Integral()
                ttree.Project(hname, vcfg.drawname, shape_cut)
                hist.Scale(scale/hist.Integral())

            stack = all_stack or (not cfg.is_data and not cfg.is_signal)

            hist.Scale(cfg.scale)

            if cfg.name in plot:
                plot[cfg.name].Add(Histogram(cfg.name, hist))
            else:
                plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)

            if not cfg.is_data:
                plot_hist.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)

    plot._ApplyPrefs()
    return plot

def setSumWeights(sample, directory='SkimAnalyzerCount'):
    if isinstance(sample, HistogramCfg) or sample.is_data:
        return

    pckfile = '/'.join([sample.ana_dir, sample.dir_name, directory, 'SkimReport.pck'])
    try:
        pckobj  = pickle.load(open(pckfile,'r'))
        counters = dict(pckobj)
        if 'Sum Weights' in counters:
            sample.sumweights = counters['Sum Weights']
    except IOError:
        pass
        
