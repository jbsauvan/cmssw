import FWCore.ParameterSet.Config as cms

hgc3DTriggerCellGenMatchSelector = cms.EDProducer(
    "HGC3DTriggerCellGenMatchSelector",
    src = cms.InputTag('hgcalConcentratorProducer:HGCalConcentratorProcessorSelection'),
    genSrc = cms.InputTag('genParticles'),
    dR = cms.double(0.3)
)
