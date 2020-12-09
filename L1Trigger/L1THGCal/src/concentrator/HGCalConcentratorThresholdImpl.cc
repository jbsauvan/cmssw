#include "L1Trigger/L1THGCal/interface/concentrator/HGCalConcentratorThresholdImpl.h"
#include "DataFormats/ForwardDetId/interface/HGCalTriggerDetId.h"

#include <fstream>

HGCalConcentratorThresholdImpl::HGCalConcentratorThresholdImpl(const edm::ParameterSet& conf)
    : use_threshold_map_(conf.getParameter<bool>("UseThresholdMap")),
      thresholdMapping_(conf.getParameter<edm::FileInPath>("ThresholdMapping")),
      threshold_silicon_(conf.getParameter<double>("threshold_silicon")),
      threshold_scintillator_(conf.getParameter<double>("threshold_scintillator")) {}

void HGCalConcentratorThresholdImpl::select(const std::vector<l1t::HGCalTriggerCell>& trigCellVecInput,
                                            std::vector<l1t::HGCalTriggerCell>& trigCellVecOutput,
                                            std::vector<l1t::HGCalTriggerCell>& trigCellVecNotSelected) {
  for (const auto& trigCell : trigCellVecInput) {
    if (trigCell.mipPt() >= threshold(trigCell.detId())) {
      trigCellVecOutput.push_back(trigCell);
    } else {
      trigCellVecNotSelected.push_back(trigCell);
    }
  }
}

double HGCalConcentratorThresholdImpl::threshold(const DetId& id) const {
  double threshold = 0.;
  bool isTriggerDetId = (id.det() == DetId::HGCalTrigger &&
             (HGCalTriggerDetId(id).subdet() == HGCalTriggerSubdetector::HGCalEETrigger ||
              HGCalTriggerDetId(id).subdet() == HGCalTriggerSubdetector::HGCalHSiTrigger));
  if(use_threshold_map_ && isTriggerDetId) {
    unsigned layer = triggerTools_.layerWithOffset(id);
    int waferu = HGCalTriggerDetId(id).waferU();
    int waferv = HGCalTriggerDetId(id).waferV();
    auto uv = uv0(layer, waferu, waferv);
    unsigned packed_wafer = packLayerWaferId(layer, uv.first, uv.second);
    auto module_itr = threshold_map_.find(packed_wafer);
    if (module_itr == threshold_map_.end()) {
      throw cms::Exception("MissingValue") << "Cannot find module with layer="<<layer<<",waferu="<<uv.first<<",waferv="<<uv.second<<" in the threshold map\n";
    }
    threshold = module_itr->second;
  } 
  else {
    bool isScintillator = triggerTools_.isScintillator(id);
    threshold = (isScintillator ? threshold_scintillator_ : threshold_silicon_);
  }
  return threshold;
}


unsigned HGCalConcentratorThresholdImpl::packLayerWaferId(unsigned layer, int waferU, int waferV) const {
  unsigned packed_value = 0;
  unsigned subdet = HGCalTriggerSubdetector::HGCalEETrigger;
  unsigned layer_offset = triggerTools_.lastLayerEE();
  if (layer > layer_offset) {
    layer -= layer_offset;
    subdet = HGCalTriggerSubdetector::HGCalHSiTrigger;
  }
  unsigned waferUsign = (waferU >= 0) ? 0 : 1;
  unsigned waferVsign = (waferV >= 0) ? 0 : 1;
  packed_value |= ((std::abs(waferU) & HGCalTriggerDetId::kHGCalWaferUMask) << HGCalTriggerDetId::kHGCalWaferUOffset);
  packed_value |= ((waferUsign & HGCalTriggerDetId::kHGCalWaferUSignMask) << HGCalTriggerDetId::kHGCalWaferUSignOffset);
  packed_value |= ((std::abs(waferV) & HGCalTriggerDetId::kHGCalWaferVMask) << HGCalTriggerDetId::kHGCalWaferVOffset);
  packed_value |= ((waferVsign & HGCalTriggerDetId::kHGCalWaferVSignMask) << HGCalTriggerDetId::kHGCalWaferVSignOffset);
  packed_value |= ((layer & HGCalTriggerDetId::kHGCalLayerMask) << HGCalTriggerDetId::kHGCalLayerOffset);
  packed_value |= ((subdet & HGCalTriggerDetId::kHGCalSubdetMask) << HGCalTriggerDetId::kHGCalSubdetOffset);
  return packed_value;
}

void HGCalConcentratorThresholdImpl::fillThresholdMap() {
  std::ifstream thresholdMappingStream(thresholdMapping_.fullPath());
  if (!thresholdMappingStream.is_open()) {
    throw cms::Exception("MissingDataFile") << "Cannot open HGCalConcentratorThreshold ThresholdMapping file\n";
  }

  unsigned layer = 0;
  int waferu = 0;
  int waferv = 0;
  float threshold = 0;
  for (; thresholdMappingStream >> layer >> waferu >> waferv >> threshold;) {
    threshold_map_.emplace(packLayerWaferId(layer, waferu, waferv), threshold);
  }
  if (!thresholdMappingStream.eof()) {
    throw cms::Exception("BadDataFile")
        << "Error reading ThresholdMapping '" << layer << " " << waferu << " " << waferv << " " << threshold << "' \n";
  }
  thresholdMappingStream.close();
}

std::pair<int,int> HGCalConcentratorThresholdImpl::uv0(unsigned layer, int u, int v) const {
  unsigned sector = 0;
  int offset = 0;

  if(layer<=28) { // CE-E    
    if(u>0 && v>=0) sector = 0;
    else {
      offset=0;
      if(u>=v && v<0) sector=2;
      else sector=1;
    }
  } else if((layer%2)==1) { // CE-H Odd
    if(u>=0 && v>=0) sector=0;
    else {
      offset=-1;    
      if(u>v && v<0) sector=2;
      else sector=1;
    }
  } else { // CE-H Even
    if(u>=1 && v>=1) sector=0;
    else {
      offset=1;
      if(u>=v && v<1) sector=2;
      else sector=1;
    }
  }

  int u0=u,v0=v;
  if(sector==1) {
    u0=v-u;
    v0=-u+offset;    
  } else if(sector==2){
    u0=-v+offset;
    v0=u-v+offset;
  }

  return std::make_pair(u0, v0);
}
