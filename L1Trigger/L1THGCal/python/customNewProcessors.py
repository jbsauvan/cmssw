import FWCore.ParameterSet.Config as cms

def custom_clustering_standalone(process):
    process.hgcalBackEndLayer2Producer.ProcessorParameters.ProcessorName = cms.string('HGCalBackendLayer2Processor3DClusteringSA')
    return process

