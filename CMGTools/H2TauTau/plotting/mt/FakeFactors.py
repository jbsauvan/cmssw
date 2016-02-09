import copy


fake_factors_regions = {}
fake_factors_minimal = {}

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
fake_factors_minimal['generic'] = [
    ## !IsoMedium -> IsoMedium 
    "{TAG}_Iso_Medium_VsPt",
    "{TAG}_Iso_Medium_VsDecay",
    "{TAG}_Iso_Medium_VsPtDecay",
]

fake_factors_regions['ZMuMu'] = []
fake_factors_regions['HighMT'] = []
fake_factors_regions['HighMTRaw'] = []
fake_factors_regions['QCDSS'] = []
fake_factors_regions['Combined'] = []
for fakefactor in fake_factors_regions['generic']:
    fake_factors_regions['ZMuMu'].append(fakefactor.format(TAG='Weight'))
    fake_factors_regions['HighMTRaw'].append(fakefactor.format(TAG='Weight_HighMTRaw'))
    fake_factors_regions['HighMT'].append(fakefactor.format(TAG='Weight_HighMT'))
    fake_factors_regions['QCDSS'].append(fakefactor.format(TAG='Weight_QCDSS'))
    fake_factors_regions['Combined'].append(fakefactor.format(TAG='Weight_Combined'))

fake_factors_minimal['ZMuMu'] = []
fake_factors_minimal['HighMT'] = []
fake_factors_minimal['HighMTRaw'] = []
fake_factors_minimal['QCDSS'] = []
fake_factors_minimal['Combined'] = []
for fakefactor in fake_factors_minimal['generic']:
    fake_factors_minimal['ZMuMu'].append(fakefactor.format(TAG='Weight'))
    fake_factors_minimal['HighMTRaw'].append(fakefactor.format(TAG='Weight_HighMTRaw'))
    fake_factors_minimal['HighMT'].append(fakefactor.format(TAG='Weight_HighMT'))
    fake_factors_minimal['QCDSS'].append(fakefactor.format(TAG='Weight_QCDSS'))
    fake_factors_minimal['Combined'].append(fakefactor.format(TAG='Weight_Combined'))


def signal_selection(fake_factor):
    sel = ''
    if 'IsoRaw_1_5' in fake_factor:
        sel = 'IsoRaw_1_5'
    elif 'Iso_Medium' in fake_factor:
        sel = 'Iso_Medium'
    else:
        raise StandardError('No signal selections associated with fake factor '+fake_factor)
    return sel

def inverted_selection(fake_factor):
    sel = ''
    if 'IsoRaw_1_5' in fake_factor:
        sel = 'InvertIsoRaw_1_5'
    elif 'Iso_Medium' in fake_factor:
        sel = 'InvertIso_Medium'
    else:
        raise StandardError('No inverted selections associated with fake factor '+fake_factor)
    return sel

def create_selections(fake_factors):
    signal_selections = {}
    inverted_selections = {}
    for fake_factor in fake_factors:
        signal_selections[fake_factor] = signal_selection(fake_factor)
        inverted_selections[fake_factor] = inverted_selection(fake_factor)
    return signal_selections, inverted_selections

def create_selection_list(selections):
    selection_list = []
    for selection in selections:
        if not selection in signal_selections_list:
            signal_selections_list.append(selection)
    return selection_list

signal_selections, inverted_selections = create_selections(fake_factors_regions['generic'])
signal_selections_minimal, inverted_selections_minimal = create_selections(fake_factors_minimal['generic'])

signal_selections_list = list(set(signal_selections.values()))
inverted_selections_list = list(set(inverted_selections.values()))
signal_selections_minimal_list = list(set(signal_selections_minimal.values()))
inverted_selections_minimal_list = list(set(inverted_selections_minimal.values()))



