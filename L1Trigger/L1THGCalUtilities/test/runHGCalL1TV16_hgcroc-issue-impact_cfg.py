import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9
process = cms.Process('DIGI',Phase2C17I13M9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D88Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D88_cff')
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
    input = cms.untracked.int32(-1)
)

# Input source
tag = 'vanilla-v4'
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:/data_cms_upgrade/sauvan/HGCAL/2502_hgcroc-issue-impact/test-files-from-pedro/SinglePhotonGun_eta1p8_CMSSW_14_1_0_pre1_D99_stucktot_{}/Events_0.root'.format(tag)),
       inputCommands=cms.untracked.vstring(
           'keep *',
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
    fileName = cms.string("ntuple-stucktot-cappedtc-{}.root".format(tag))
    )

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T21', '')

# load HGCAL TPG simulation
process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
process.load('L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cff')

from L1Trigger.L1THGCalUtilities.hgcalTriggerChains import HGCalTriggerChains
import L1Trigger.L1THGCalUtilities.vfe as vfe
import L1Trigger.L1THGCalUtilities.concentrator as concentrator
import L1Trigger.L1THGCalUtilities.clustering2d as clustering2d
import L1Trigger.L1THGCalUtilities.layer1 as layer1
import L1Trigger.L1THGCalUtilities.clustering3d as clustering3d
import L1Trigger.L1THGCalUtilities.selectors as selectors
import L1Trigger.L1THGCalUtilities.customNtuples as ntuple


chains = HGCalTriggerChains()
# Register algorithms
## VFE
chains.register_vfe("Default", vfe.CreateVfe())
chains.register_vfe("Totzeroing", vfe.CreateVfeToTZeoring())

## ECON
chains.register_concentrator("Bcstc", concentrator.CreateMixedFeOptions())
chains.register_concentrator("Bcstccapping", concentrator.CreateMixedFeOptionsTcCapping())
## BE1
chains.register_backend1("Dummy", clustering2d.CreateDummy())
## BE2
chains.register_backend2("Histomax", clustering3d.CreateHistoMax())
# Register selector
#  chains.register_selector("Genmatch", selectors.CreateGenMatch())


# Register ntuples
ntuple_list = ['event', 'digis', 'triggercells', 'gen', 'multiclusters']
chains.register_ntuple("Digintuple", ntuple.CreateNtuple(ntuple_list))

# Register trigger chains
chains.register_chain('Default', 'Bcstc', 'Dummy', 'Histomax', '', 'Digintuple')
chains.register_chain('Totzeroing', 'Bcstc', 'Dummy', 'Histomax', '', 'Digintuple')
chains.register_chain('Default', 'Bcstccapping', 'Dummy', 'Histomax', '', 'Digintuple')

process = chains.create_sequences(process)

# Remove towers from sequence
process.L1THGCalTriggerPrimitives.remove(process.L1THGCalTowerMap)
process.L1THGCalTriggerPrimitives.remove(process.L1THGCalTower)

process.hgcl1tpg_step = cms.Path(process.L1THGCalTriggerPrimitives)
process.selector_step = cms.Path(process.L1THGCalTriggerSelector)
process.ntuple_step = cms.Path(process.L1THGCalTriggerNtuples)

# Schedule definition
process.schedule = cms.Schedule(process.hgcl1tpg_step, process.ntuple_step)



# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
