import ROOT


def newShift(nominal, systematic, newnominal):
    newsystematic = newnominal.Clone(newnominal.GetName())
    newsystematic.Multiply(systematic)
    newsystematic.Divide(nominal)
    return newsystematic



prefitfile = ROOT.TFile.Open('signalRegion/FakeRateEstimation/Datacards/v160308/MT40_/Weight_Combined_Iso_Medium_VsPtDecay/datacard_mvis_stdbins.root')
postfitfile = ROOT.TFile.Open('../../../../../../CMSSW_7_1_21_patch2/src/CombineHarvester/HttFakes/scripts/output/LIMITS/OS/v160308/mt/shapes_postfit.root')
outputfile = ROOT.TFile.Open('shapes_postfit_sys.root','recreate')


histos = ['TT','VV','W','ZL','ZTT','data_obs','fakes_data']
nomprefit  = 'mt_inclusive'
nompostfit = 'mt_inclusive_postfit'
sysdirs = ['mt_inclusive_FakeFactorHighMTUp', 'mt_inclusive_FakeFactorQCDSSUp']

for h in histos:
    hprenom = prefitfile.Get(nomprefit+'/'+h)
    hpostnom = postfitfile.Get(nompostfit+'/'+h)
    outputfile.cd()
    hpostnom.Write()
    for sys in sysdirs:
        hpresys = prefitfile.Get(sys+'/'+h)
        outputfile.mkdir(sys)
        outputfile.cd(sys)
        hpostsys = newShift(hprenom, hpresys, hpostnom)
        hpostsys.Write()


outputfile.Close()
postfitfile.Close()
prefitfile.Close()


