import sys
sys.path.append('.')
from CRABClient.UserUtilities import config
import local

config = config()

config.section_("General")
config.General.requestName = 'GammaGun_Pt1_100_PU0_HLTSummer20ReRECOMiniAOD_{}_realbcstc4_DPH1_Imp2'.format(local.prod_name)
config.General.workArea = 'jobs'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'produce_ntuple_realbcstc_genmatch_withModuleSums_v11_cfg.py'
config.JobType.maxMemoryMB = 2500
#config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.inputDataset = '/DoublePhoton_FlatPt-1To100/Phase2HLTTDRSummer20ReRECOMiniAOD-NoPU_111X_mcRun4_realistic_T15_v1-v1/FEVT'
config.Data.inputDBS = 'global'
#/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DoublePhoton_FlatPt-1To100/FEVT/NoPU_111X_mcRun4_realistic_T15_v1-v1/110000/001C5D05-8192-054B-827B-F1D34DFDDB96.root

config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = local.outLFNDirBase
config.Data.publication = False
config.Data.outputDatasetTag = config.General.requestName

config.section_("Site")
config.Site.storageSite = local.storageSite