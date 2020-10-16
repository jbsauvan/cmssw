#ifndef __L1Trigger_L1THGCal_HGCalVFELinearizationImpl_h__
#define __L1Trigger_L1THGCal_HGCalVFELinearizationImpl_h__

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HGCDigi/interface/HGCDigiCollections.h"
#include "L1Trigger/L1THGCal/interface/HGCalTriggerTools.h"
#include "SimCalorimetry/HGCalSimAlgos/interface/HGCalSiNoiseMap.h"

#include <vector>
#include <utility>

class HGCalVFELinearizationImpl {
public:
  HGCalVFELinearizationImpl(const edm::ParameterSet& conf);
  void eventSetup(const edm::EventSetup& es, DetId::Detector det);

  void linearize(const std::vector<HGCalDataFrame>&, std::vector<std::pair<DetId, uint32_t>>&);

private:
  double adcLSB_;
  double linLSB_;
  double adcsaturation_;
  uint32_t tdcnBits_;
  double tdcOnset_;
  uint32_t adcnBits_;
  double tdcsaturation_;
  double tdcLSB_;
  //
  uint32_t linMax_;
  uint32_t linnBits_;
  std::vector<double> oot_coefficients_;
  //
  HGCalTriggerTools triggerTools_;
  bool new_digi_ = false;
  mutable HGCalSiNoiseMap noise_map_;
};

#endif
