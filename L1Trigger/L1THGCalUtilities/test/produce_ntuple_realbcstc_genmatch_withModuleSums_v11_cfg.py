import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2C9_cff import Phase2C9
process = cms.Process('DIGI',Phase2C9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC14TeV_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

process.source = cms.Source("PoolSource",
       fileNames = cms.untracked.vstring('/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DoublePhoton_FlatPt-1To100/FEVT/NoPU_111X_mcRun4_realistic_T15_v1-v1/110000/001C5D05-8192-054B-827B-F1D34DFDDB96.root'),
       inputCommands=cms.untracked.vstring(
           'keep *',
           'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
           'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
           'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
           'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
           'drop l1tEMTFTrack2016s_simEmtfDigis__HLT',
           'drop FTLClusteredmNewDetSetVector_mtdClusters_FTLBarrel_RECO',
           'drop FTLClusteredmNewDetSetVector_mtdClusters_FTLEndcap_RECO',
           'drop MTDTrackingRecHitedmNewDetSetVector_mtdTrackingRecHits__RECO',
           'drop BTLDetIdBTLSampleFTLDataFrameTsSorted_mix_FTLBarrel_HLT',
           'drop ETLDetIdETLSampleFTLDataFrameTsSorted_mix_FTLEndcap_HLT',
           'drop l1tTkPrimaryVertexs_L1TkPrimaryVertex__RECO'
           )
        )
process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('SingleElectronPt10_cfi nevts:10'),
    name = cms.untracked.string('Applications')
)

# Output definition
process.TFileService = cms.Service(
    "TFileService",
    #  fileName = cms.string("/home/llr/cms/manoni/CMSSW_12_5_2_patch1/src/L1Trigger/L1THGCalUtilities/test/prod/ntuple_96Imp3_300ev.root")
    fileName = cms.string("ntuple.root")
    )

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T15', '')

# load HGCAL TPG simulation
process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
process.load('L1Trigger.L1THGCalUtilities.HGC3DClusterGenMatchSelector_cff')
process.load('L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cff')


# Use old geometry version Imp2 to be able to run with signal-driven elinks mapping
from L1Trigger.L1THGCal.customTriggerGeometry import custom_geometry_V11_Imp3
process = custom_geometry_V11_Imp3(process)
#process.l1tHGCalTriggerGeometryESProducer.TriggerGeometry.L1TLinksMapping = cms.FileInPath('L1Trigger/L1THGCal/data/links_mapping_V11_decentralized_signaldriven_1_max4.txt')

# Use all TC in modules for triggerSums
from L1Trigger.L1THGCal.customTriggerSums import custom_full_trigger_sums
process = custom_full_trigger_sums(process)

# Use BC+STC ECON-T algorithm
from L1Trigger.L1THGCal.customTriggerCellSelect import custom_triggercellselect_mixedBestChoiceSuperTriggerCell_decentralized
process = custom_triggercellselect_mixedBestChoiceSuperTriggerCell_decentralized(process)

import L1Trigger.L1THGCalUtilities.vfe as vfe
import L1Trigger.L1THGCalUtilities.concentrator as concentrator
import L1Trigger.L1THGCalUtilities.clustering2d as clustering2d
import L1Trigger.L1THGCalUtilities.clustering3d as clustering3d
import L1Trigger.L1THGCalUtilities.selectors as selectors
import L1Trigger.L1THGCalUtilities.customNtuples as ntuple

# fill cluster layer info
process.ntuple_multiclusters.FillLayerInfo = True

# Remove towers from sequence
#process.hgcalTriggerPrimitives.remove(process.hgcalTowerMap)
#process.hgcalTriggerPrimitives.remove(process.hgcalTower)


process.hgcl1tpg_step = cms.Path(process.L1THGCalTriggerPrimitives)
process.selector_step = cms.Path(process.L1THGCalTriggerSelector)

# load ntuplizer

ntuple_list = ['event', 'gen', 'multiclusters','triggercells','triggersums']

process.ntuple_step = cms.Path(process.L1THGCalTriggerNtuples)

# Schedule definition
process.schedule = cms.Schedule(process.hgcl1tpg_step, process.selector_step, process.ntuple_step)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
