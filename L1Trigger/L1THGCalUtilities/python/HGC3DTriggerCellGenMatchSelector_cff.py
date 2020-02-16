import FWCore.ParameterSet.Config as cms

from L1Trigger.L1THGCalUtilities.HGC3DTriggerCellGenMatchSelector_cfi import *

hgcalTriggerSelector = cms.Sequence(hgc3DTriggerCellGenMatchSelector)
