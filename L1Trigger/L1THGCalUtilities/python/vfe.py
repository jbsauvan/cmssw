import FWCore.ParameterSet.Config as cms

from L1Trigger.L1THGCal.l1tHGCalVFEProducer_cfi import vfe_proc

hgcroc3c_layers = [23, 24, 25, 26] + [l for l in range(38, 48)]
class CreateVfeToTZeoring(object):
    def __init__(self,
                 layers=hgcroc3c_layers
            ):
        self.processor = vfe_proc.clone(
            linearizationCfg_si = vfe_proc.linearizationCfg_si.clone(zero_tot_layers=layers),
            linearizationCfg_sc = vfe_proc.linearizationCfg_sc.clone(zero_tot_layers=layers),
        )

    def __call__(self, process):
        producer = process.l1tHGCalVFEProducer.clone(
            ProcessorParameters = self.processor
        )
        return producer


class CreateVfe(object):
    def __init__(self,
            linearization_si=vfe_proc.linearizationCfg_si,
            linearization_sc=vfe_proc.linearizationCfg_sc,
            compression_ldm=vfe_proc.compressionCfg_ldm,
            compression_hdm=vfe_proc.compressionCfg_hdm,
            ):
        self.processor = vfe_proc.clone(
            linearizationCfg_si = linearization_si,
            linearizationCfg_sc = linearization_sc,
            compressionCfg_ldm = compression_ldm,
            compressionCfg_hdm = compression_hdm,
        )

    def __call__(self, process):
        producer = process.l1tHGCalVFEProducer.clone(
            ProcessorParameters = self.processor
        )
        return producer
