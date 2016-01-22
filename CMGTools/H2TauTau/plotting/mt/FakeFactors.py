

fake_factors_regions = {}

fake_factors_regions['ZMuMu'] = [
    ## IsoRaw > 1.5 GeV -> IsoRaw < 1.5 GeV 
    "Weight_IsoRaw_1_5_Inclusive",
    #"Weight_IsoRaw_1_5_VsNVtx",
    "Weight_IsoRaw_1_5_VsPt",
    #"Weight_IsoRaw_1_5_VsEta",
    "Weight_IsoRaw_1_5_VsDecay",
    "Weight_IsoRaw_1_5_VsPdgId",
    "Weight_IsoRaw_1_5_VsJetPt",
    #"Weight_IsoRaw_1_5_VsPtEta",
    "Weight_IsoRaw_1_5_VsPtDecay",
    "Weight_IsoRaw_1_5_VsPtPdgId",
    "Weight_IsoRaw_1_5_VsJetPtDecay",
    "Weight_IsoRaw_1_5_VsJetPtPt",
    ## !IsoMedium -> IsoMedium 
    "Weight_Iso_Medium_Inclusive",
    #"Weight_Iso_Medium_VsNVtx",
    "Weight_Iso_Medium_VsPt",
    #"Weight_Iso_Medium_VsEta",
    "Weight_Iso_Medium_VsDecay",
    "Weight_Iso_Medium_VsPdgId",
    "Weight_Iso_Medium_VsJetPt",
    #"Weight_Iso_Medium_VsPtEta",
    "Weight_Iso_Medium_VsPtDecay",
    "Weight_Iso_Medium_VsPtPdgId",
    "Weight_Iso_Medium_VsJetPtDecay",
    "Weight_Iso_Medium_VsJetPtPt",
]

fake_factors_regions['HighMT'] = [
    ## IsoRaw > 1.5 GeV -> IsoRaw < 1.5 GeV 
    "Weight_HighMT_IsoRaw_1_5_Inclusive",
    #"Weight_HighMT_IsoRaw_1_5_VsNVtx",
    "Weight_HighMT_IsoRaw_1_5_VsPt",
    #"Weight_HighMT_IsoRaw_1_5_VsEta",
    "Weight_HighMT_IsoRaw_1_5_VsDecay",
    "Weight_HighMT_IsoRaw_1_5_VsPdgId",
    "Weight_HighMT_IsoRaw_1_5_VsJetPt",
    #"Weight_HighMT_IsoRaw_1_5_VsPtEta",
    "Weight_HighMT_IsoRaw_1_5_VsPtDecay",
    "Weight_HighMT_IsoRaw_1_5_VsPtPdgId",
    "Weight_HighMT_IsoRaw_1_5_VsJetPtDecay",
    "Weight_HighMT_IsoRaw_1_5_VsJetPtPt",
    ## !IsoMedium -> IsoMedium 
    "Weight_HighMT_Iso_Medium_Inclusive",
    #"Weight_HighMT_Iso_Medium_VsNVtx",
    "Weight_HighMT_Iso_Medium_VsPt",
    #"Weight_HighMT_Iso_Medium_VsEta",
    "Weight_HighMT_Iso_Medium_VsDecay",
    "Weight_HighMT_Iso_Medium_VsPdgId",
    "Weight_HighMT_Iso_Medium_VsJetPt",
    #"Weight_HighMT_Iso_Medium_VsPtEta",
    "Weight_HighMT_Iso_Medium_VsPtDecay",
    "Weight_HighMT_Iso_Medium_VsPtPdgId",
    "Weight_HighMT_Iso_Medium_VsJetPtDecay",
    "Weight_HighMT_Iso_Medium_VsJetPtPt",
]

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

