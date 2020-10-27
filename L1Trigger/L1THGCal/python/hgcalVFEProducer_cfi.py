from __future__ import absolute_import
import FWCore.ParameterSet.Config as cms

from L1Trigger.L1THGCal.hgcalTriggerGeometryESProducer_cfi import *

import SimCalorimetry.HGCalSimProducers.hgcalDigitizer_cfi as digiparam
import RecoLocalCalo.HGCalRecProducers.HGCalUncalibRecHit_cfi as recoparam
import RecoLocalCalo.HGCalRecProducers.HGCalRecHit_cfi as recocalibparam 
from . import hgcalLayersCalibrationCoefficients_cfi as layercalibparam

newDigi = False

feCfg_si = digiparam.hgceeDigitizer.digiCfg.feCfg
feCfg_sc = digiparam.hgchebackDigitizer.digiCfg.feCfg

# trigger cell LSB before compression is the LSB of the ADC
#  triggerCellLsbBeforeCompression_si = float(feCfg_si.adcSaturation_fC.value())/(2**float(feCfg_si.adcNbits.value()))
triggerCellLsbBeforeCompression_si = 1./80.
triggerCellLsbBeforeCompression_sc = float(feCfg_sc.adcSaturation_fC.value())/(2**float(feCfg_sc.adcNbits.value()))

# Radiation map info
integLumi=3000.
from SimCalorimetry.HGCalSimProducers.hgcalDigitizer_cfi import HGCAL_ileakParam_toUse,HGCAL_cceParams_toUse

# Linearization parameters for EE
linearization_params_ee = cms.PSet(
        linLSB = cms.double(triggerCellLsbBeforeCompression_si),
        adcsaturation = feCfg_si.adcSaturation_fC,
        tdcnBits = feCfg_si.tdcNbits,
        tdcOnset = feCfg_si.tdcOnset_fC,
        adcnBits = feCfg_si.adcNbits,
        tdcsaturation = feCfg_si.tdcSaturation_fC,
        linnBits = cms.uint32(17),
         oot_coefficients = cms.vdouble(0., 0.), # OOT PU subtraction coeffs for samples (bx-2, bx-1). (0,0) = no OOT PU subtraction
         newDigi = cms.bool(newDigi),
        doseMap           = cms.string('SimCalorimetry/HGCalSimProducers/data/doseParams_3000fb_fluka-3.7.20.txt'),
        scaleByDoseAlgo   = cms.uint32(0),
        scaleByDoseFactor = cms.double(integLumi/3000.),
        ileakParam        = HGCAL_ileakParam_toUse,
        cceParams         = HGCAL_cceParams_toUse,
        )

# Linearization parameters for HE silicon
linearization_params_hesi = cms.PSet(
        linLSB = cms.double(triggerCellLsbBeforeCompression_si),
        adcsaturation = feCfg_si.adcSaturation_fC,
        tdcnBits = feCfg_si.tdcNbits,
        tdcOnset = feCfg_si.tdcOnset_fC,
        adcnBits = feCfg_si.adcNbits,
        tdcsaturation = feCfg_si.tdcSaturation_fC,
        linnBits = cms.uint32(17),
         oot_coefficients = cms.vdouble(0., 0.), # OOT PU subtraction coeffs for samples (bx-2, bx-1). (0,0) = no OOT PU subtraction
         newDigi = cms.bool(newDigi),
        doseMap           = cms.string('SimCalorimetry/HGCalSimProducers/data/doseParams_3000fb_fluka-3.7.20.txt'),
        scaleByDoseAlgo   = cms.uint32(0),
        scaleByDoseFactor = cms.double(integLumi/3000.),
        ileakParam        = HGCAL_ileakParam_toUse,
        cceParams         = HGCAL_cceParams_toUse,
        )

# Linearization parameters for HE scintillator
linearization_params_hesc = cms.PSet(
        linLSB = cms.double(triggerCellLsbBeforeCompression_sc),
        adcsaturation = feCfg_sc.adcSaturation_fC,
        tdcnBits = feCfg_sc.tdcNbits,
        tdcOnset = feCfg_sc.tdcOnset_fC,
        adcnBits = feCfg_sc.adcNbits,
        tdcsaturation = feCfg_sc.tdcSaturation_fC,
        linnBits = cms.uint32(17),
        oot_coefficients = cms.vdouble(0., 0.), # OOT PU subtraction coeffs for samples (bx-2, bx-1). (0,0) = no OOT PU subtraction
        newDigi = cms.bool(False),
        )

summation_params = cms.PSet(
        siliconCellLSB_fC =  cms.double(triggerCellLsbBeforeCompression_si),
        scintillatorCellLSB_MIP = cms.double(triggerCellLsbBeforeCompression_sc),
        noiseSilicon = cms.PSet(),
        noiseScintillator = cms.PSet(),
        # cell thresholds before TC sums
        # Cut at 3sigma of the noise
        #  noiseThreshold = cms.double(3), # in units of sigmas of the noise
        noiseThreshold = cms.double(0), # in units of sigmas of the noise
        )

# Compression parameters for low density modules
compression_params_ldm = cms.PSet(
        exponentBits = cms.uint32(4),
        mantissaBits = cms.uint32(3),
        truncationBits = cms.uint32(1),
        rounding = cms.bool(True),
        )
# Compression parameters for high density modules
compression_params_hdm = cms.PSet(
        exponentBits = cms.uint32(4),
        mantissaBits = cms.uint32(3),
        truncationBits = cms.uint32(3),
        rounding = cms.bool(True),
        )

# Reco calibration parameters
fCperMIPee = recoparam.HGCalUncalibRecHit.HGCEEConfig.fCPerMIP
fCperMIPhe = recoparam.HGCalUncalibRecHit.HGCHEFConfig.fCPerMIP
fCperMIPnose = recoparam.HGCalUncalibRecHit.HGCHFNoseConfig.fCPerMIP
layerWeights = layercalibparam.TrgLayer_dEdX_weights
layerWeightsNose = recocalibparam.dEdX.weightsNose
thicknessCorrectionSi = recocalibparam.HGCalRecHit.thicknessCorrection
thicknessCorrectionSc = recocalibparam.HGCalRecHit.sciThicknessCorrection
thicknessCorrectionNose = recocalibparam.HGCalRecHit.thicknessNoseCorrection


NTHICKNESS = 3
calibration_params_ee = cms.PSet(
        lsb = cms.double(triggerCellLsbBeforeCompression_si),
        fCperMIP = fCperMIPee,
        dEdXweights = layerWeights,
        thicknessCorrection = cms.vdouble(thicknessCorrectionSi[0:NTHICKNESS]),
        chargeCollectionEfficiency = cms.PSet(),

        newDigi = cms.bool(newDigi),
        doseMap           = cms.string('SimCalorimetry/HGCalSimProducers/data/doseParams_3000fb_fluka-3.7.20.txt'),
        scaleByDoseAlgo   = cms.uint32(0),
        scaleByDoseFactor = cms.double(integLumi/3000.),
        ileakParam        = HGCAL_ileakParam_toUse,
        cceParams         = HGCAL_cceParams_toUse,
        )

calibration_params_hesi = cms.PSet(
        lsb = cms.double(triggerCellLsbBeforeCompression_si),
        fCperMIP = fCperMIPhe,
        dEdXweights = layerWeights,
        thicknessCorrection = cms.vdouble(thicknessCorrectionSi[NTHICKNESS:2*NTHICKNESS]),
        chargeCollectionEfficiency = cms.PSet(),

        newDigi = cms.bool(newDigi),
        doseMap           = cms.string('SimCalorimetry/HGCalSimProducers/data/doseParams_3000fb_fluka-3.7.20.txt'),
        scaleByDoseAlgo   = cms.uint32(0),
        scaleByDoseFactor = cms.double(integLumi/3000.),
        ileakParam        = HGCAL_ileakParam_toUse,
        cceParams         = HGCAL_cceParams_toUse,
        )

calibration_params_hesc = cms.PSet(
        lsb = cms.double(triggerCellLsbBeforeCompression_sc),
        fCperMIP = cms.vdouble(1.),
        dEdXweights = layerWeights,
        thicknessCorrection = cms.vdouble(thicknessCorrectionSc.value()),
        chargeCollectionEfficiency = cms.PSet(values=cms.vdouble(1.)),
        newDigi = cms.bool(False),
        )

calibration_params_nose = cms.PSet(
        lsb = cms.double(triggerCellLsbBeforeCompression_si),
        fCperMIP = fCperMIPnose,
        dEdXweights = layerWeightsNose,
        thicknessCorrection = thicknessCorrectionNose,
        chargeCollectionEfficiency = cms.PSet(),
        newDigi = cms.bool(False),
        )

vfe_proc = cms.PSet( ProcessorName = cms.string('HGCalVFEProcessorSums'),
                     linearizationCfg_ee = linearization_params_ee,
                     linearizationCfg_hesi = linearization_params_hesi,
                     linearizationCfg_hesc = linearization_params_hesc,
                     summationCfg = summation_params,
                     compressionCfg_ldm = compression_params_ldm,
                     compressionCfg_hdm = compression_params_hdm,
                     calibrationCfg_ee = calibration_params_ee,
                     calibrationCfg_hesi = calibration_params_hesi,
                     calibrationCfg_hesc = calibration_params_hesc,
                     calibrationCfg_nose = calibration_params_nose,
                     )

# isolate these refs in case they aren't available in some other WF
from Configuration.Eras.Modifier_phase2_hgcal_cff import phase2_hgcal
phase2_hgcal.toModify(summation_params,
    noiseSilicon = cms.PSet(refToPSet_ = cms.string("HGCAL_noise_fC")),
    noiseScintillator = cms.PSet(refToPSet_ = cms.string("HGCAL_noise_heback")),
)

phase2_hgcal.toModify(calibration_params_ee,
    chargeCollectionEfficiency = cms.PSet(refToPSet_ = cms.string("HGCAL_chargeCollectionEfficiencies")),
)
phase2_hgcal.toModify(calibration_params_hesi,
    chargeCollectionEfficiency = cms.PSet(refToPSet_ = cms.string("HGCAL_chargeCollectionEfficiencies")),
)
phase2_hgcal.toModify(calibration_params_nose,
    chargeCollectionEfficiency = cms.PSet(refToPSet_ = cms.string("HGCAL_chargeCollectionEfficiencies")),
)



hgcalVFEProducer = cms.EDProducer(
        "HGCalVFEProducer",
        eeDigis = cms.InputTag('simHGCalUnsuppressedDigis:EE'),
        fhDigis = cms.InputTag('simHGCalUnsuppressedDigis:HEfront'),
        bhDigis = cms.InputTag('simHGCalUnsuppressedDigis:HEback'),
        ProcessorParameters = vfe_proc.clone()
       )

hfnoseVFEProducer = cms.EDProducer(
        "HFNoseVFEProducer",
        noseDigis = cms.InputTag('simHFNoseUnsuppressedDigis:HFNose'),
        ProcessorParameters = vfe_proc.clone()
       )



