import FWCore.ParameterSet.Config as cms


def custom_stage1_truncation(process):
    process.hgcalBackEndLayer1Producer.ProcessorParameters.ProcessorName = cms.string('HGCalBackendStage1Processor')
    process.hgcalBackEndLayer2Producer.InputCluster = cms.InputTag('hgcalBackEndLayer1Producer:HGCalBackendStage1Processor')
    process.hgcalTowerProducer.InputTriggerCells = cms.InputTag('hgcalBackEndLayer1Producer:HGCalBackendStage1Processor')
    return process

def custom_clustering_standalone(process):
    process.hgcalBackEndLayer2Producer.ProcessorParameters.ProcessorName = cms.string('HGCalBackendLayer2Processor3DClusteringSA')
    return process

def custom_tower_standalone(process):
    process.hgcalTowerProducer.ProcessorParameters.ProcessorName = cms.string('HGCalTowerProcessorSA')
    return process

