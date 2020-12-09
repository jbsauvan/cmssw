#ifndef __L1Trigger_L1THGCal_HGCalConcentratorThresholdImpl_h__
#define __L1Trigger_L1THGCal_HGCalConcentratorThresholdImpl_h__

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/L1THGCal/interface/HGCalTriggerCell.h"
#include "L1Trigger/L1THGCal/interface/HGCalTriggerTools.h"
#include <vector>
#include <unordered_map>

class HGCalConcentratorThresholdImpl {
public:
  HGCalConcentratorThresholdImpl(const edm::ParameterSet& conf);

  void select(const std::vector<l1t::HGCalTriggerCell>& trigCellVecInput,
              std::vector<l1t::HGCalTriggerCell>& trigCellVecOutput,
              std::vector<l1t::HGCalTriggerCell>& trigCellVecNotSelected);

  void eventSetup(const edm::EventSetup& es) { 
    triggerTools_.eventSetup(es);
    if(use_threshold_map_ && threshold_map_.empty()) {
      fillThresholdMap();
    }
  }

private:
  double threshold(const DetId&) const;
  void fillThresholdMap();
  unsigned packLayerWaferId(unsigned, int, int) const;
  std::pair<int,int> uv0(unsigned, int, int) const;
  
  bool use_threshold_map_ = false;
  edm::FileInPath thresholdMapping_;
  double threshold_silicon_;
  double threshold_scintillator_;
  std::unordered_map<unsigned,float> threshold_map_;

  HGCalTriggerTools triggerTools_;
};

#endif
