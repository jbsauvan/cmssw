from L1Trigger.L1THGCal.l1tHGCalVFEProducer_cfi import vfe_proc

def custom_hgcroc_oot(process,
                      oot_coefficients=vfe_proc.linearizationCfg_si.oot_coefficients
                      ):
    parameters = vfe_proc.clone(
            linearizationCfg_si = vfe_proc.linearizationCfg_si.clone(oot_coefficients=oot_coefficients),
            linearizationCfg_sc = vfe_proc.linearizationCfg_sc.clone(oot_coefficients=oot_coefficients),
            )
    process.l1tHGCalVFEProducer.ProcessorParameters = parameters
    return process


def custom_hgcroc_compression(process,
        exponentBits=vfe_proc.compressionCfg_ldm.exponentBits,
        mantissaBits=vfe_proc.compressionCfg_ldm.mantissaBits,
        rounding=vfe_proc.compressionCfg_ldm.rounding,
        truncationBits_ldm=vfe_proc.compressionCfg_ldm.truncationBits,
        truncationBits_hdm=vfe_proc.compressionCfg_hdm.truncationBits,
        ):
    parameters = vfe_proc.clone(
            compressionCfg_ldm = vfe_proc.compressionCfg_ldm.clone(
                exponentBits=exponentBits,
                mantissaBits=mantissaBits,
                truncationBits=truncationBits_ldm,
                rounding=rounding,
                ),
            compressionCfg_hdm = vfe_proc.compressionCfg_hdm.clone(
                exponentBits=exponentBits,
                mantissaBits=mantissaBits,
                truncationBits=truncationBits_hdm,
                rounding=rounding,
                ),
            )
    process.l1tHGCalVFEProducer.ProcessorParameters = parameters
    return process

hgcroc3c_layers = [23, 24, 25, 26] + [l for l in range(38, 48)]
def custom_hgcroc3c_tot_zeroing(process, layers=hgcroc3c_layers):
    parameters = vfe_proc.clone(
            linearizationCfg_si = vfe_proc.linearizationCfg_si.clone(zero_tot_layers=layers),
            linearizationCfg_sc = vfe_proc.linearizationCfg_sc.clone(zero_tot_layers=layers),
            )
    process.l1tHGCalVFEProducer.ProcessorParameters = parameters
    return process
