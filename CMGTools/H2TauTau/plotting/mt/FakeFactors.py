import copy


fake_factors_regions = {}

fake_factors_regions['generic'] = [
    ## IsoRaw > 1.5 GeV -> IsoRaw < 1.5 GeV 
    "{TAG}_IsoRaw_1_5_Inclusive",
    #"{TAG}_IsoRaw_1_5_VsNVtx",
    "{TAG}_IsoRaw_1_5_VsPt",
    #"{TAG}_IsoRaw_1_5_VsEta",
    "{TAG}_IsoRaw_1_5_VsDecay",
    "{TAG}_IsoRaw_1_5_VsPdgId",
    "{TAG}_IsoRaw_1_5_VsJetPt",
    #"{TAG}_IsoRaw_1_5_VsPtEta",
    "{TAG}_IsoRaw_1_5_VsPtDecay",
    "{TAG}_IsoRaw_1_5_VsPtPdgId",
    "{TAG}_IsoRaw_1_5_VsJetPtDecay",
    "{TAG}_IsoRaw_1_5_VsJetPtPt",
    ## !IsoMedium -> IsoMedium 
    "{TAG}_Iso_Medium_Inclusive",
    #"{TAG}_Iso_Medium_VsNVtx",
    "{TAG}_Iso_Medium_VsPt",
    #"{TAG}_Iso_Medium_VsEta",
    "{TAG}_Iso_Medium_VsDecay",
    "{TAG}_Iso_Medium_VsPdgId",
    "{TAG}_Iso_Medium_VsJetPt",
    #"{TAG}_Iso_Medium_VsPtEta",
    "{TAG}_Iso_Medium_VsPtDecay",
    "{TAG}_Iso_Medium_VsPtPdgId",
    "{TAG}_Iso_Medium_VsJetPtDecay",
    "{TAG}_Iso_Medium_VsJetPtPt",
]

fake_factors_regions['ZMuMu'] = []
fake_factors_regions['HighMT'] = []
fake_factors_regions['QCDSS'] = []
fake_factors_regions['Combined'] = []
for fakefactor in fake_factors_regions['generic']:
    fake_factors_regions['ZMuMu'].append(fakefactor.format(TAG='Weight'))
    fake_factors_regions['HighMT'].append(fakefactor.format(TAG='Weight_HighMT'))
    fake_factors_regions['QCDSS'].append(fakefactor.format(TAG='Weight_QCDSS'))
    fake_factors_regions['Combined'].append(fakefactor.format(TAG='Weight_Combined'))


signal_selections = {}
inverted_selections ={}
for region,fake_factors in fake_factors_regions.items():
    for fake_factor in fake_factors:
        if 'IsoRaw_1_5' in fake_factor:
            signal_selections[fake_factor] = 'IsoRaw_1_5'
            inverted_selections[fake_factor] = 'InvertIsoRaw_1_5'
        elif 'Iso_Medium' in fake_factor:
            signal_selections[fake_factor] = 'Iso_Medium'
            inverted_selections[fake_factor] = 'InvertIso_Medium'
        else:
            raise StandardError('No signal and inverted selections associated with fake factor '+fake_factor)

signal_selections_list = []
inverted_selections_list = []
for selection in signal_selections.values():
    if not selection in signal_selections_list:
        signal_selections_list.append(selection)
for selection in inverted_selections.values():
    if not selection in inverted_selections_list:
        inverted_selections_list.append(selection)

