import FWCore.ParameterSet.Config as cms

dtTriggerSynchMonitor = cms.EDAnalyzer("DTLocalTriggerSynchTask",
    staticBooking = cms.untracked.bool(True),
    # labels of DDU/DCC data and 4D segments
    DCCInputTag    = cms.InputTag('dttfDigis'),
    DDUInputTag    = cms.InputTag('muonDTDigis'),
    SEGInputTag    = cms.InputTag('dt4DSegments'),
    bxTimeInterval = cms.double(25),
    rangeWithinBX  = cms.bool(True),
    nBXHigh        = cms.int32(0),
    nBXLow         = cms.int32(1),
    angleRange     = cms.double(30.),
    minHitsPhi     = cms.int32(7),
    baseDir        = cms.string("DT/90-LocalTriggerSynch/"),
    tTrigModeConfig = cms.PSet(
            vPropWire = cms.double(24.4),
            doTOFCorrection = cms.bool(False),
            tofCorrType = cms.int32(0),
            wirePropCorrType = cms.int32(0),
            doWirePropCorrection = cms.bool(False),
            doT0Correction = cms.bool(False),
            debug = cms.untracked.bool(False),
            tTrigLabel = cms.string('')
    ),
    tTrigMode = cms.string('DTTTrigSyncFromDB')
)


