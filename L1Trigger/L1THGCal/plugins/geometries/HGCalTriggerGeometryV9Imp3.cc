#include "Geometry/HGCalCommonData/interface/HGCalGeomRotation.h"
#include "DataFormats/ForwardDetId/interface/ForwardSubdetector.h"
#include "DataFormats/ForwardDetId/interface/HFNoseTriggerDetId.h"
#include "DataFormats/ForwardDetId/interface/HGCScintillatorDetId.h"
#include "DataFormats/ForwardDetId/interface/HGCSiliconDetIdToROC.h"
#include "DataFormats/ForwardDetId/interface/HGCalDetId.h"
#include "DataFormats/ForwardDetId/interface/HGCalTriggerDetId.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "L1Trigger/L1THGCal/interface/HGCalTriggerGeometryBase.h"
#include "L1Trigger/L1THGCal/interface/HGCalModuleDetId.h"
#include "DataFormats/ForwardDetId/interface/HFNoseDetIdToModule.h"

#include "tbb/concurrent_unordered_set.h"
#include <fstream>
#include <iostream>
#include <regex>
#include <vector>

#include <nlohmann/json.hpp>
using json = nlohmann::json;

class HGCalTriggerGeometryV9Imp3 : public HGCalTriggerGeometryBase {
public:
  HGCalTriggerGeometryV9Imp3(const edm::ParameterSet& conf);

  void initialize(const CaloGeometry*) final;
  void initialize(const HGCalGeometry*, const HGCalGeometry*, const HGCalGeometry*) final;
  void initialize(const HGCalGeometry*, const HGCalGeometry*, const HGCalGeometry*, const HGCalGeometry*) final;
  void reset() final;

  unsigned getTriggerCellFromCell(const unsigned) const final;
  unsigned getModuleFromCell(const unsigned) const final;
  unsigned getModuleFromTriggerCell(const unsigned) const final;

  geom_set getCellsFromTriggerCell(const unsigned) const final;
  geom_set getCellsFromModule(const unsigned) const final;
  geom_set getTriggerCellsFromModule(const unsigned) const final;

  geom_ordered_set getOrderedCellsFromModule(const unsigned) const final;
  geom_ordered_set getOrderedTriggerCellsFromModule(const unsigned) const final;

  geom_set getNeighborsFromTriggerCell(const unsigned) const final;

  geom_set getStage1FpgasFromStage2Fpga(const unsigned) const final;
  geom_set getLbgbtsFromStage1Fpga(const unsigned) const final;
  geom_set getStage2FpgasFromStage1Fpga(const unsigned) const final;
  unsigned getStage1FpgaFromLpgbt(const unsigned) const final;
  geom_set getModulesFromLpgbt(const unsigned) const final;
  geom_set getLpgbtsFromModule(const unsigned) const final;

  unsigned getLinksInModule(const unsigned module_id) const final;
  unsigned getModuleSize(const unsigned module_id) const final;

  GlobalPoint getTriggerCellPosition(const unsigned) const final;
  GlobalPoint getModulePosition(const unsigned) const final;

  bool validCell(const unsigned) const final;
  bool validTriggerCell(const unsigned) const final;
  bool disconnectedModule(const unsigned) const final;
  unsigned lastTriggerLayer() const final { return last_trigger_layer_; }
  unsigned triggerLayer(const unsigned) const final;

private:
  // HSc trigger cell grouping
  unsigned hSc_triggercell_size_ = 2;
  unsigned hSc_module_size_ = 12;  // in TC units (144 TC / panel = 36 e-links)
  unsigned hSc_links_per_module_ = 1;
  unsigned hSc_wafers_per_module_ = 3;

  unsigned sector0_mask_ = 0x7f;  // 7 bits to encode module number in 60deg sector

  edm::FileInPath jsonMappingFile_;

  // rotation class
  HGCalGeomRotation geom_rotation_120_ = {HGCalGeomRotation::SectorType::Sector120Degrees};

  // module related maps
  std::unordered_map<unsigned, unsigned> links_per_module_;

  std::unordered_multimap<unsigned, unsigned> stage2_to_stage1_;
  std::unordered_multimap<unsigned, unsigned> stage1_to_stage2_;
  std::unordered_multimap<unsigned, unsigned> stage1_to_lpgbts_;
  std::unordered_map<unsigned, unsigned> lpgbt_to_stage1_;
  std::unordered_multimap<unsigned, unsigned> lpgbt_to_modules_;
  std::unordered_multimap<unsigned, unsigned> module_to_lpgbts_;

  // Disconnected modules and layers
  std::unordered_set<unsigned> disconnected_modules_;
  std::unordered_set<unsigned> disconnected_layers_;
  std::vector<unsigned> trigger_layers_;
  std::vector<unsigned> trigger_nose_layers_;
  unsigned last_trigger_layer_ = 0;

  //Scintillator layout
  unsigned hSc_num_panels_per_sector_ = 8;

  // layer offsets
  unsigned heOffset_ = 0;
  unsigned noseLayers_ = 0;
  unsigned totalLayers_ = 0;

  void fillMaps();
  bool validCellId(unsigned det, unsigned cell_id) const;
  bool validTriggerCellFromCells(const unsigned) const;

  int detIdWaferType(unsigned det, unsigned layer, short waferU, short waferV) const;
  unsigned packLayerWaferId(unsigned layer, int waferU, int waferV) const;
  HGCalGeomRotation::WaferCentring getWaferCentring(unsigned layer) const;
  void etaphiMappingFromSector0(int& ieta, int& iphi, unsigned sector) const;
  unsigned etaphiMappingToSector0(int& ieta, int& iphi) const;

  unsigned layerWithOffset(unsigned) const;
};

HGCalTriggerGeometryV9Imp3::HGCalTriggerGeometryV9Imp3(const edm::ParameterSet& conf)
    : HGCalTriggerGeometryBase(conf),
      hSc_triggercell_size_(conf.getParameter<unsigned>("ScintillatorTriggerCellSize")),
      hSc_module_size_(conf.getParameter<unsigned>("ScintillatorModuleSize")),
      hSc_links_per_module_(conf.getParameter<unsigned>("ScintillatorLinksPerModule")),
      jsonMappingFile_(conf.getParameter<edm::FileInPath>("JsonMappingFile")) {
  const unsigned ntc_per_wafer = 48;
  hSc_wafers_per_module_ = std::round(hSc_module_size_ * hSc_module_size_ / float(ntc_per_wafer));
  if (ntc_per_wafer * hSc_wafers_per_module_ < hSc_module_size_ * hSc_module_size_) {
    hSc_wafers_per_module_++;
  }
  std::vector<unsigned> tmp_vector = conf.getParameter<std::vector<unsigned>>("DisconnectedModules");
  std::move(tmp_vector.begin(), tmp_vector.end(), std::inserter(disconnected_modules_, disconnected_modules_.end()));
  tmp_vector = conf.getParameter<std::vector<unsigned>>("DisconnectedLayers");
  std::move(tmp_vector.begin(), tmp_vector.end(), std::inserter(disconnected_layers_, disconnected_layers_.end()));
}

void HGCalTriggerGeometryV9Imp3::reset() {
  stage2_to_stage1_.clear();
  stage1_to_stage2_.clear();
  stage1_to_lpgbts_.clear();
  lpgbt_to_stage1_.clear();
  lpgbt_to_modules_.clear();
  module_to_lpgbts_.clear();
}

void HGCalTriggerGeometryV9Imp3::initialize(const CaloGeometry* calo_geometry) {
  throw cms::Exception("BadGeometry")
      << "HGCalTriggerGeometryV9Imp3 geometry cannot be initialized with the V7/V8 HGCAL geometry";
}

void HGCalTriggerGeometryV9Imp3::initialize(const HGCalGeometry* hgc_ee_geometry,
                                            const HGCalGeometry* hgc_hsi_geometry,
                                            const HGCalGeometry* hgc_hsc_geometry) {
  setEEGeometry(hgc_ee_geometry);
  setHSiGeometry(hgc_hsi_geometry);
  setHScGeometry(hgc_hsc_geometry);
  heOffset_ = eeTopology().dddConstants().layers(true);
  totalLayers_ = heOffset_ + hsiTopology().dddConstants().layers(true);
  trigger_layers_.resize(totalLayers_ + 1);
  trigger_layers_[0] = 0;  // layer number 0 doesn't exist
  unsigned trigger_layer = 1;
  for (unsigned layer = 1; layer < trigger_layers_.size(); layer++) {
    if (disconnected_layers_.find(layer) == disconnected_layers_.end()) {
      // Increase trigger layer number if the layer is not disconnected
      trigger_layers_[layer] = trigger_layer;
      trigger_layer++;
    } else {
      trigger_layers_[layer] = 0;
    }
  }
  last_trigger_layer_ = trigger_layer - 1;
  fillMaps();
}

void HGCalTriggerGeometryV9Imp3::initialize(const HGCalGeometry* hgc_ee_geometry,
                                            const HGCalGeometry* hgc_hsi_geometry,
                                            const HGCalGeometry* hgc_hsc_geometry,
                                            const HGCalGeometry* hgc_nose_geometry) {
  setEEGeometry(hgc_ee_geometry);
  setHSiGeometry(hgc_hsi_geometry);
  setHScGeometry(hgc_hsc_geometry);
  setNoseGeometry(hgc_nose_geometry);

  heOffset_ = eeTopology().dddConstants().layers(true);
  totalLayers_ = heOffset_ + hsiTopology().dddConstants().layers(true);

  trigger_layers_.resize(totalLayers_ + 1);
  trigger_layers_[0] = 0;  // layer number 0 doesn't exist
  unsigned trigger_layer = 1;
  for (unsigned layer = 1; layer < trigger_layers_.size(); layer++) {
    if (disconnected_layers_.find(layer) == disconnected_layers_.end()) {
      // Increase trigger layer number if the layer is not disconnected
      trigger_layers_[layer] = trigger_layer;
      trigger_layer++;
    } else {
      trigger_layers_[layer] = 0;
    }
  }
  last_trigger_layer_ = trigger_layer - 1;
  fillMaps();

  noseLayers_ = noseTopology().dddConstants().layers(true);

  trigger_nose_layers_.resize(noseLayers_ + 1);
  trigger_nose_layers_[0] = 0;  // layer number 0 doesn't exist
  unsigned trigger_nose_layer = 1;
  for (unsigned layer = 1; layer < trigger_nose_layers_.size(); layer++) {
    trigger_nose_layers_[layer] = trigger_nose_layer;
    trigger_nose_layer++;
  }
}

unsigned HGCalTriggerGeometryV9Imp3::getTriggerCellFromCell(const unsigned cell_id) const {
  unsigned det = DetId(cell_id).det();
  unsigned trigger_cell_id = 0;
  // Scintillator
  if (det == DetId::HGCalHSc) {
    // Very rough mapping from cells to TC
    HGCScintillatorDetId cell_sc_id(cell_id);
    int ieta = ((cell_sc_id.ietaAbs() - 1) / hSc_triggercell_size_ + 1) * cell_sc_id.zside();
    int iphi = (cell_sc_id.iphi() - 1) / hSc_triggercell_size_ + 1;
    trigger_cell_id = HGCScintillatorDetId(cell_sc_id.type(), cell_sc_id.layer(), ieta, iphi);
  }
  // HFNose
  else if (det == DetId::Forward && DetId(cell_id).subdetId() == ForwardSubdetector::HFNose) {
    HFNoseDetId cell_nose_id(cell_id);
    trigger_cell_id = HFNoseTriggerDetId(HGCalTriggerSubdetector::HFNoseTrigger,
                                         cell_nose_id.zside(),
                                         cell_nose_id.type(),
                                         cell_nose_id.layer(),
                                         cell_nose_id.waferU(),
                                         cell_nose_id.waferV(),
                                         cell_nose_id.triggerCellU(),
                                         cell_nose_id.triggerCellV());
  }
  // Silicon
  else if (det == DetId::HGCalEE || det == DetId::HGCalHSi) {
    HGCSiliconDetId cell_si_id(cell_id);
    trigger_cell_id = HGCalTriggerDetId(
        det == DetId::HGCalEE ? HGCalTriggerSubdetector::HGCalEETrigger : HGCalTriggerSubdetector::HGCalHSiTrigger,
        cell_si_id.zside(),
        cell_si_id.type(),
        cell_si_id.layer(),
        cell_si_id.waferU(),
        cell_si_id.waferV(),
        cell_si_id.triggerCellU(),
        cell_si_id.triggerCellV());
  }
  return trigger_cell_id;
}

unsigned HGCalTriggerGeometryV9Imp3::getModuleFromCell(const unsigned cell_id) const {
  return getModuleFromTriggerCell(getTriggerCellFromCell(cell_id));
}

unsigned HGCalTriggerGeometryV9Imp3::getModuleFromTriggerCell(const unsigned trigger_cell_id) const {
  unsigned det = DetId(trigger_cell_id).det();
  int zside = 0;
  unsigned tc_type = 1;
  unsigned layer = 0;
  unsigned module_id = 0;

  // Scintillator
  if (det == DetId::HGCalHSc) {
    HGCScintillatorDetId trigger_cell_sc_id(trigger_cell_id);
    tc_type = trigger_cell_sc_id.type();
    layer = trigger_cell_sc_id.layer();
    zside = trigger_cell_sc_id.zside();
    int ietamin = hscTopology().dddConstants().getREtaRange(layer).first;
    int ietamin_tc = ((ietamin - 1) / hSc_triggercell_size_ + 1);
    int ieta = ((trigger_cell_sc_id.ietaAbs() - ietamin_tc) / hSc_module_size_ + 1);
    int iphi = (trigger_cell_sc_id.iphi() - 1) / hSc_module_size_ + 1;
    unsigned sector = etaphiMappingToSector0(ieta, iphi);
    module_id = HGCalModuleDetId(ForwardSubdetector::HGCHEB, zside, tc_type, layer, sector, ieta, iphi);
  }
  // HFNose
  else if (det == DetId::HGCalTrigger and
           HGCalTriggerDetId(trigger_cell_id).subdet() == HGCalTriggerSubdetector::HFNoseTrigger) {
    HFNoseTriggerDetId trigger_cell_trig_id(trigger_cell_id);
    tc_type = trigger_cell_trig_id.type();
    layer = trigger_cell_trig_id.layer();
    zside = trigger_cell_trig_id.zside();
    int waferu = trigger_cell_trig_id.waferU();
    int waferv = trigger_cell_trig_id.waferV();
    unsigned sector = geom_rotation_120_.uvMappingToSector0(getWaferCentring(layer), waferu, waferv);
    module_id = HGCalModuleDetId(ForwardSubdetector::HFNose, zside, tc_type, layer, sector, waferu, waferv);
  }
  // Silicon
  else {
    HGCalTriggerDetId trigger_cell_trig_id(trigger_cell_id);
    unsigned subdet = trigger_cell_trig_id.subdet();
    unsigned subdet_old =
        (subdet == HGCalTriggerSubdetector::HGCalEETrigger ? ForwardSubdetector::HGCEE : ForwardSubdetector::HGCHEF);
    tc_type = trigger_cell_trig_id.type();
    layer = trigger_cell_trig_id.layer();
    zside = trigger_cell_trig_id.zside();
    int waferu = trigger_cell_trig_id.waferU();
    int waferv = trigger_cell_trig_id.waferV();
    unsigned sector = geom_rotation_120_.uvMappingToSector0(getWaferCentring(layer), waferu, waferv);
    module_id = HGCalModuleDetId((ForwardSubdetector)subdet_old, zside, tc_type, layer, sector, waferu, waferv);
  }
  return module_id;
}

HGCalTriggerGeometryBase::geom_set HGCalTriggerGeometryV9Imp3::getCellsFromTriggerCell(
    const unsigned trigger_cell_id) const {
  DetId trigger_cell_det_id(trigger_cell_id);
  unsigned det = trigger_cell_det_id.det();
  geom_set cell_det_ids;
  // Scintillator
  if (det == DetId::HGCalHSc) {
    HGCScintillatorDetId trigger_cell_sc_id(trigger_cell_id);
    int ieta0 = (trigger_cell_sc_id.ietaAbs() - 1) * hSc_triggercell_size_ + 1;
    int iphi0 = (trigger_cell_sc_id.iphi() - 1) * hSc_triggercell_size_ + 1;
    for (int ietaAbs = ieta0; ietaAbs < ieta0 + (int)hSc_triggercell_size_; ietaAbs++) {
      int ieta = ietaAbs * trigger_cell_sc_id.zside();
      for (int iphi = iphi0; iphi < iphi0 + (int)hSc_triggercell_size_; iphi++) {
        unsigned cell_id = HGCScintillatorDetId(trigger_cell_sc_id.type(), trigger_cell_sc_id.layer(), ieta, iphi);
        if (validCellId(DetId::HGCalHSc, cell_id))
          cell_det_ids.emplace(cell_id);
      }
    }
  }
  // HFNose
  else if (det == DetId::HGCalTrigger and
           HGCalTriggerDetId(trigger_cell_id).subdet() == HGCalTriggerSubdetector::HFNoseTrigger) {
    HFNoseTriggerDetId trigger_cell_nose_id(trigger_cell_id);
    int layer = trigger_cell_nose_id.layer();
    int zside = trigger_cell_nose_id.zside();
    int type = trigger_cell_nose_id.type();
    int waferu = trigger_cell_nose_id.waferU();
    int waferv = trigger_cell_nose_id.waferV();
    std::vector<int> cellus = trigger_cell_nose_id.cellU();
    std::vector<int> cellvs = trigger_cell_nose_id.cellV();
    for (unsigned ic = 0; ic < cellus.size(); ic++) {
      HFNoseDetId cell_det_id(zside, type, layer, waferu, waferv, cellus[ic], cellvs[ic]);
      cell_det_ids.emplace(cell_det_id);
    }
  }
  // Silicon
  else {
    HGCalTriggerDetId trigger_cell_trig_id(trigger_cell_id);
    unsigned subdet = trigger_cell_trig_id.subdet();
    if (subdet == HGCalTriggerSubdetector::HGCalEETrigger || subdet == HGCalTriggerSubdetector::HGCalHSiTrigger) {
      DetId::Detector cell_det = (subdet == HGCalTriggerSubdetector::HGCalEETrigger ? DetId::HGCalEE : DetId::HGCalHSi);
      int layer = trigger_cell_trig_id.layer();
      int zside = trigger_cell_trig_id.zside();
      int type = trigger_cell_trig_id.type();
      int waferu = trigger_cell_trig_id.waferU();
      int waferv = trigger_cell_trig_id.waferV();
      std::vector<int> cellus = trigger_cell_trig_id.cellU();
      std::vector<int> cellvs = trigger_cell_trig_id.cellV();
      for (unsigned ic = 0; ic < cellus.size(); ic++) {
        HGCSiliconDetId cell_det_id(cell_det, zside, type, layer, waferu, waferv, cellus[ic], cellvs[ic]);
        cell_det_ids.emplace(cell_det_id);
      }
    }
  }
  return cell_det_ids;
}

HGCalTriggerGeometryBase::geom_set HGCalTriggerGeometryV9Imp3::getCellsFromModule(const unsigned module_id) const {
  geom_set cell_det_ids;
  geom_set trigger_cells = getTriggerCellsFromModule(module_id);

  for (auto trigger_cell_id : trigger_cells) {
    geom_set cells = getCellsFromTriggerCell(trigger_cell_id);
    cell_det_ids.insert(cells.begin(), cells.end());
  }
  return cell_det_ids;
}

HGCalTriggerGeometryBase::geom_ordered_set HGCalTriggerGeometryV9Imp3::getOrderedCellsFromModule(
    const unsigned module_id) const {
  geom_ordered_set cell_det_ids;
  geom_ordered_set trigger_cells = getOrderedTriggerCellsFromModule(module_id);
  for (auto trigger_cell_id : trigger_cells) {
    geom_set cells = getCellsFromTriggerCell(trigger_cell_id);
    cell_det_ids.insert(cells.begin(), cells.end());
  }
  return cell_det_ids;
}

HGCalTriggerGeometryBase::geom_set HGCalTriggerGeometryV9Imp3::getTriggerCellsFromModule(
    const unsigned module_id) const {
  DetId module_det_id(module_id);
  unsigned subdet = module_det_id.subdetId();
  geom_set trigger_cell_det_ids;

  HGCalModuleDetId hgc_module_id(module_id);

  // Scintillator
  if (subdet == ForwardSubdetector::HGCHEB) {
    int ietamin = hscTopology().dddConstants().getREtaRange(hgc_module_id.layer()).first;
    int ietamin_tc = ((ietamin - 1) / hSc_triggercell_size_ + 1);
    int ieta0 = (hgc_module_id.eta() - 1) * hSc_module_size_ + ietamin_tc;
    int iphi0 = hgc_module_id.phi();
    etaphiMappingFromSector0(ieta0, iphi0, hgc_module_id.sector());
    iphi0 = (iphi0 - 1) * hSc_module_size_ + 1;
    for (int ietaAbs = ieta0; ietaAbs < ieta0 + (int)hSc_module_size_; ietaAbs++) {
      int ieta = ietaAbs * hgc_module_id.zside();
      for (int iphi = iphi0; iphi < iphi0 + (int)hSc_module_size_; iphi++) {
        unsigned trigger_cell_id = HGCScintillatorDetId(hgc_module_id.type(), hgc_module_id.layer(), ieta, iphi);
        if (validTriggerCellFromCells(trigger_cell_id))
          trigger_cell_det_ids.emplace(trigger_cell_id);
      }
    }
  }
  // HFNose
  else if (subdet == ForwardSubdetector::HFNose) {
    HFNoseDetId module_nose_id(module_id);
    HFNoseDetIdToModule hfn;
    std::vector<HFNoseTriggerDetId> ids = hfn.getTriggerDetIds(module_nose_id);
    for (auto const& idx : ids) {
      if (validTriggerCellFromCells(idx.rawId()))
        trigger_cell_det_ids.emplace(idx);
    }
  }
  // Silicon
  else {
    HGCSiliconDetIdToROC tc2roc;
    int moduleU = hgc_module_id.moduleU();
    int moduleV = hgc_module_id.moduleV();
    unsigned layer = hgc_module_id.layer();

    //Rotate to sector
    geom_rotation_120_.uvMappingFromSector0(getWaferCentring(layer), moduleU, moduleV, hgc_module_id.sector());

    DetId::Detector det = (hgc_module_id.subdetId() == ForwardSubdetector::HGCEE ? DetId::HGCalEE : DetId::HGCalHSi);
    HGCalTriggerSubdetector subdet =
        (hgc_module_id.subdetId() == ForwardSubdetector::HGCEE ? HGCalTriggerSubdetector::HGCalEETrigger
                                                               : HGCalTriggerSubdetector::HGCalHSiTrigger);

    unsigned wafer_type = detIdWaferType(det, layer, moduleU, moduleV);
    int nroc = (wafer_type == HGCSiliconDetId::HGCalFine ? 6 : 3);
    // Loop on ROCs in wafer
    for (int roc = 1; roc <= nroc; roc++) {
      // loop on TCs in ROC
      auto tc_uvs = tc2roc.getTriggerId(roc, wafer_type);
      for (const auto& tc_uv : tc_uvs) {
        HGCalTriggerDetId trigger_cell_id(
            subdet, hgc_module_id.zside(), wafer_type, layer, moduleU, moduleV, tc_uv.first, tc_uv.second);
        if (validTriggerCellFromCells(trigger_cell_id.rawId()))
          trigger_cell_det_ids.emplace(trigger_cell_id);
      }
    }
  }

  return trigger_cell_det_ids;
}

HGCalTriggerGeometryBase::geom_ordered_set HGCalTriggerGeometryV9Imp3::getOrderedTriggerCellsFromModule(
    const unsigned module_id) const {
  DetId module_det_id(module_id);
  unsigned subdet = module_det_id.subdetId();
  geom_ordered_set trigger_cell_det_ids;

  HGCalModuleDetId hgc_module_id(module_id);

  // Scintillator
  if (subdet == ForwardSubdetector::HGCHEB) {
    int ieta0 = hgc_module_id.eta() * hSc_module_size_;
    int iphi0 = (hgc_module_id.phi() * (hgc_module_id.sector() + 1)) * hSc_module_size_;

    for (int ietaAbs = ieta0; ietaAbs < ieta0 + (int)hSc_module_size_; ietaAbs++) {
      int ieta = ietaAbs * hgc_module_id.zside();
      for (int iphi = iphi0; iphi < iphi0 + (int)hSc_module_size_; iphi++) {
        unsigned trigger_cell_id = HGCScintillatorDetId(hgc_module_id.type(), hgc_module_id.layer(), ieta, iphi);
        if (validTriggerCellFromCells(trigger_cell_id))
          trigger_cell_det_ids.emplace(trigger_cell_id);
      }
    }
  }

  // HFNose
  else if (subdet == ForwardSubdetector::HFNose) {
    HFNoseDetId module_nose_id(module_id);
    HFNoseDetIdToModule hfn;
    std::vector<HFNoseTriggerDetId> ids = hfn.getTriggerDetIds(module_nose_id);
    for (auto const& idx : ids) {
      if (validTriggerCellFromCells(idx.rawId()))
        trigger_cell_det_ids.emplace(idx);
    }
  }
  // Silicon
  else {
    HGCSiliconDetIdToROC tc2roc;
    int moduleU = hgc_module_id.moduleU();
    int moduleV = hgc_module_id.moduleU();
    unsigned layer = hgc_module_id.layer();

    //Rotate to sector
    geom_rotation_120_.uvMappingFromSector0(getWaferCentring(layer), moduleU, moduleV, hgc_module_id.sector());

    DetId::Detector det = (hgc_module_id.subdetId() == ForwardSubdetector::HGCEE ? DetId::HGCalEE : DetId::HGCalHSi);
    HGCalTriggerSubdetector subdet =
        (hgc_module_id.subdetId() == ForwardSubdetector::HGCEE ? HGCalTriggerSubdetector::HGCalEETrigger
                                                               : HGCalTriggerSubdetector::HGCalHSiTrigger);
    unsigned wafer_type = detIdWaferType(det, layer, moduleU, moduleV);
    int nroc = (wafer_type == HGCSiliconDetId::HGCalFine ? 6 : 3);
    // Loop on ROCs in wafer
    for (int roc = 1; roc <= nroc; roc++) {
      // loop on TCs in ROC
      auto tc_uvs = tc2roc.getTriggerId(roc, wafer_type);
      for (const auto& tc_uv : tc_uvs) {
        HGCalTriggerDetId trigger_cell_id(
            subdet, hgc_module_id.zside(), wafer_type, layer, moduleU, moduleV, tc_uv.first, tc_uv.second);
        if (validTriggerCellFromCells(trigger_cell_id.rawId()))
          trigger_cell_det_ids.emplace(trigger_cell_id);
      }
    }
  }

  return trigger_cell_det_ids;
}

HGCalTriggerGeometryBase::geom_set HGCalTriggerGeometryV9Imp3::getNeighborsFromTriggerCell(
    const unsigned trigger_cell_id) const {
  throw cms::Exception("FeatureNotImplemented") << "Neighbor search is not implemented in HGCalTriggerGeometryV9Imp3";
}

unsigned HGCalTriggerGeometryV9Imp3::getLinksInModule(const unsigned module_id) const {
  HGCalModuleDetId module_det_id(module_id);
  unsigned links = 0;
  // Scintillator
  if (module_det_id.subdetId() == ForwardSubdetector::HGCHEB) {
    links = hSc_links_per_module_;
  } else if (module_det_id.subdetId() == ForwardSubdetector::HFNose) {
    links = 1;
  }
  // TO ADD HFNOSE : getLinksInModule
  // Silicon
  else {
    links =
        links_per_module_.at(packLayerWaferId(module_det_id.layer(), module_det_id.moduleU(), module_det_id.moduleV()));
  }
  return links;
}

unsigned HGCalTriggerGeometryV9Imp3::getModuleSize(const unsigned module_id) const {
  unsigned nWafers = 1;
  return nWafers;
}

HGCalTriggerGeometryBase::geom_set HGCalTriggerGeometryV9Imp3::getStage1FpgasFromStage2Fpga(
    const unsigned stage2_id) const {
  geom_set stage1_ids;

  auto stage2_itrs = stage2_to_stage1_.equal_range(stage2_id);
  for (auto stage2_itr = stage2_itrs.first; stage2_itr != stage2_itrs.second; stage2_itr++) {
    stage1_ids.emplace(stage2_itr->second);
  }

  return stage1_ids;
}

HGCalTriggerGeometryBase::geom_set HGCalTriggerGeometryV9Imp3::getLbgbtsFromStage1Fpga(const unsigned stage1_id) const {
  geom_set lpgbt_ids;

  auto stage1_itrs = stage1_to_lpgbts_.equal_range(stage1_id);
  for (auto stage1_itr = stage1_itrs.first; stage1_itr != stage1_itrs.second; stage1_itr++) {
    lpgbt_ids.emplace(stage1_itr->second);
  }

  return lpgbt_ids;
}

HGCalTriggerGeometryBase::geom_set HGCalTriggerGeometryV9Imp3::getStage2FpgasFromStage1Fpga(
    const unsigned stage1_id) const {
  geom_set stage2_ids;

  auto stage1_itrs = stage1_to_stage2_.equal_range(stage1_id);
  for (auto stage1_itr = stage1_itrs.first; stage1_itr != stage1_itrs.second; stage1_itr++) {
    stage2_ids.emplace(stage1_itr->second);
  }

  return stage2_ids;
}

unsigned HGCalTriggerGeometryV9Imp3::getStage1FpgaFromLpgbt(const unsigned lpgbt_id) const {
  return lpgbt_to_stage1_.at(lpgbt_id);
}

HGCalTriggerGeometryBase::geom_set HGCalTriggerGeometryV9Imp3::getModulesFromLpgbt(const unsigned lpgbt_id) const {
  geom_set modules;

  auto lpgbt_itrs = lpgbt_to_modules_.equal_range(lpgbt_id);
  for (auto lpgbt_itr = lpgbt_itrs.first; lpgbt_itr != lpgbt_itrs.second; lpgbt_itr++) {
    modules.emplace(lpgbt_itr->second);
  }

  return modules;
}

HGCalTriggerGeometryV9Imp3::geom_set HGCalTriggerGeometryV9Imp3::getLpgbtsFromModule(const unsigned module_id) const {
  geom_set lpgbt_ids;

  auto module_itrs = module_to_lpgbts_.equal_range(module_id);
  for (auto module_itr = module_itrs.first; module_itr != module_itrs.second; module_itr++) {
    lpgbt_ids.emplace(module_itr->second);
  }

  return lpgbt_ids;
}

GlobalPoint HGCalTriggerGeometryV9Imp3::getTriggerCellPosition(const unsigned trigger_cell_det_id) const {
  unsigned det = DetId(trigger_cell_det_id).det();

  // Position: barycenter of the trigger cell.
  Basic3DVector<float> triggerCellVector(0., 0., 0.);
  const auto cell_ids = getCellsFromTriggerCell(trigger_cell_det_id);
  // Scintillator
  if (det == DetId::HGCalHSc) {
    for (const auto& cell : cell_ids) {
      triggerCellVector += hscGeometry()->getPosition(cell).basicVector();
    }
  }
  // HFNose
  else if (det == DetId::HGCalTrigger and
           HGCalTriggerDetId(trigger_cell_det_id).subdet() == HGCalTriggerSubdetector::HFNoseTrigger) {
    for (const auto& cell : cell_ids) {
      HFNoseDetId cellDetId(cell);
      triggerCellVector += noseGeometry()->getPosition(cellDetId).basicVector();
    }
  }
  // Silicon
  else {
    for (const auto& cell : cell_ids) {
      HGCSiliconDetId cellDetId(cell);
      triggerCellVector += (cellDetId.det() == DetId::HGCalEE ? eeGeometry()->getPosition(cellDetId)
                                                              : hsiGeometry()->getPosition(cellDetId))
                               .basicVector();
    }
  }
  return GlobalPoint(triggerCellVector / cell_ids.size());
}

GlobalPoint HGCalTriggerGeometryV9Imp3::getModulePosition(const unsigned module_det_id) const {
  unsigned subdet = HGCalModuleDetId(module_det_id).subdetId();
  // Position: barycenter of the module.
  Basic3DVector<float> moduleVector(0., 0., 0.);
  const auto cell_ids = getCellsFromModule(module_det_id);
  // Scintillator
  if (subdet == ForwardSubdetector::HGCHEB) {
    for (const auto& cell : cell_ids) {
      moduleVector += hscGeometry()->getPosition(cell).basicVector();
    }
  }
  // HFNose
  else if (subdet == ForwardSubdetector::HFNose) {
    for (const auto& cell : cell_ids) {
      HFNoseDetId cellDetId(cell);
      moduleVector += noseGeometry()->getPosition(cellDetId).basicVector();
    }
  }  // Silicon
  else {
    for (const auto& cell : cell_ids) {
      HGCSiliconDetId cellDetId(cell);
      moduleVector += (cellDetId.det() == DetId::HGCalEE ? eeGeometry()->getPosition(cellDetId)
                                                         : hsiGeometry()->getPosition(cellDetId))
                          .basicVector();
    }
  }

  return GlobalPoint(moduleVector / cell_ids.size());
}

void HGCalTriggerGeometryV9Imp3::fillMaps() {
  // read json mapping file
  json mapping_config;
  std::ifstream json_input_file(jsonMappingFile_.fullPath());
  if (!json_input_file.is_open()) {
    throw cms::Exception("MissingDataFile") << "Cannot open HGCalTriggerGeometry L1TMapping file\n";
  }
  json_input_file >> mapping_config;

  //Stage 1 to Stage 2 mapping
  try {
    for (unsigned stage1_id = 0; stage1_id < mapping_config.at("Stage1").size(); stage1_id++) {
      for (auto& stage2_id : mapping_config.at("Stage1").at(stage1_id).at("Stage2")) {
        stage1_to_stage2_.emplace(stage1_id, stage2_id);
      }
    }

    //Stage 1 to lpgbt mapping
    for (unsigned stage1_id = 0; stage1_id < mapping_config.at("Stage1").size(); stage1_id++) {
      for (auto& lpgbt_id : mapping_config.at("Stage1").at(stage1_id).at("lpgbts")) {
        stage1_to_lpgbts_.emplace(stage1_id, lpgbt_id);
      }
    }

  } catch (const json::exception& e) {
    edm::LogError("HGCalTriggerGeometryV9Imp3")
        << "The mapping input json file does not have the expected structure for the Stage1 block";
  }

  try {
    //Stage 2 to Stage 1 mapping
    for (unsigned stage2_id = 0; stage2_id < mapping_config.at("Stage2").size(); stage2_id++) {
      for (auto& stage1_id : mapping_config.at("Stage2").at(stage2_id).at("Stage1")) {
        stage2_to_stage1_.emplace(stage2_id, stage1_id);
      }
    }
  } catch (const json::exception& e) {
    edm::LogError("HGCalTriggerGeometryV9Imp3")
        << "The mapping input json file does not have the expected structure for the Stage2 block";
  }

  try {
    //lpgbt to Stage 1 mapping
    for (unsigned lpgbt_id = 0; lpgbt_id < mapping_config.at("lpgbt").size(); lpgbt_id++) {
      lpgbt_to_stage1_.emplace(lpgbt_id, mapping_config.at("lpgbt").at(lpgbt_id).at("Stage1"));
    }

    //lpgbt to module mapping
    for (unsigned lpgbt_id = 0; lpgbt_id < mapping_config.at("lpgbt").size(); lpgbt_id++) {
      for (auto& modules : mapping_config.at("lpgbt").at(lpgbt_id).at("Modules")) {
        lpgbt_to_modules_.emplace(lpgbt_id, packLayerWaferId(modules.at("layer"), modules.at("u"), modules.at("v")));
      }
    }

  } catch (const json::exception& e) {
    edm::LogError("HGCalTriggerGeometryV9Imp3")
        << "The mapping input json file does not have the expected structure for the lpGBT block";
  }

  try {
    //module to lpgbt mapping
    for (unsigned module = 0; module < mapping_config.at("Module").size(); module++) {
      unsigned num_elinks = 0;  //Sum number of e-links in each module over lpGBTs
      unsigned layer = mapping_config.at("Module").at(module).at("layer");
      unsigned moduleU = mapping_config.at("Module").at(module).at("u");
      unsigned moduleV = mapping_config.at("Module").at(module).at("v");

      for (auto& lpgbt : mapping_config.at("Module").at(module).at("lpgbts")) {
        module_to_lpgbts_.emplace(packLayerWaferId(layer, moduleU, moduleV), lpgbt.at("id"));
        num_elinks += unsigned(lpgbt.at("nElinks"));
      }
      if (mapping_config.at("Module").at(module).at("isSilicon")) {
        links_per_module_.emplace(packLayerWaferId(layer, moduleU, moduleV), num_elinks);
      }
    }
  } catch (const json::exception& e) {
    edm::LogError("HGCalTriggerGeometryV9Imp3")
        << "The mapping input json file does not have the expected structure for the Module block";
  }

  json_input_file.close();
}

unsigned HGCalTriggerGeometryV9Imp3::packLayerWaferId(unsigned layer, int waferU, int waferV) const {
  unsigned packed_value = 0;

  packed_value |= ((waferU & HGCalModuleDetId::kHGCalModuleUMask) << HGCalModuleDetId::kHGCalModuleUOffset);
  packed_value |= ((waferV & HGCalModuleDetId::kHGCalModuleVMask) << HGCalModuleDetId::kHGCalModuleVOffset);
  packed_value |= ((layer & HGCalModuleDetId::kHGCalLayerMask) << HGCalModuleDetId::kHGCalLayerOffset);
  return packed_value;
}

void HGCalTriggerGeometryV9Imp3::etaphiMappingFromSector0(int& ieta, int& iphi, unsigned sector) const {
  if (sector == 0) {
    return;
  }
  iphi = iphi + (sector * hSc_num_panels_per_sector_);
}

HGCalGeomRotation::WaferCentring HGCalTriggerGeometryV9Imp3::getWaferCentring(unsigned layer) const {
  if (layer <= heOffset_) {  // CE-E
    return HGCalGeomRotation::WaferCentring::WaferCentred;
  } else if ((layer % 2) == 1) {  // CE-H Odd
    return HGCalGeomRotation::WaferCentring::CornerCentredY;
  } else {  // CE-H Even
    return HGCalGeomRotation::WaferCentring::CornerCentredMercedes;
  }
}

unsigned HGCalTriggerGeometryV9Imp3::etaphiMappingToSector0(int& ieta, int& iphi) const {
  unsigned sector = 0;

  if (unsigned(std::abs(iphi)) > 2 * hSc_num_panels_per_sector_)
    sector = 2;
  else if (unsigned(std::abs(iphi)) > hSc_num_panels_per_sector_)
    sector = 1;
  else
    sector = 0;

  iphi = iphi - (sector * hSc_num_panels_per_sector_);

  return sector;
}

bool HGCalTriggerGeometryV9Imp3::validTriggerCell(const unsigned trigger_cell_id) const {
  return validTriggerCellFromCells(trigger_cell_id);
}

bool HGCalTriggerGeometryV9Imp3::disconnectedModule(const unsigned module_id) const {
  bool disconnected = false;
  if (disconnected_layers_.find(layerWithOffset(module_id)) != disconnected_layers_.end())
    disconnected = true;
  return disconnected;
}

unsigned HGCalTriggerGeometryV9Imp3::triggerLayer(const unsigned id) const {
  unsigned layer = layerWithOffset(id);

  if (DetId(id).det() == DetId::HGCalTrigger and
      HGCalTriggerDetId(id).subdet() == HGCalTriggerSubdetector::HFNoseTrigger) {
    if (layer >= trigger_nose_layers_.size())
      return 0;
    return trigger_nose_layers_[layer];
  }
  if (layer >= trigger_layers_.size())
    return 0;
  return trigger_layers_[layer];
}

bool HGCalTriggerGeometryV9Imp3::validCell(unsigned cell_id) const {
  bool is_valid = false;
  unsigned det = DetId(cell_id).det();
  switch (det) {
    case DetId::HGCalEE:
      is_valid = eeTopology().valid(cell_id);
      break;
    case DetId::HGCalHSi:
      is_valid = hsiTopology().valid(cell_id);
      break;
    case DetId::HGCalHSc:
      is_valid = hscTopology().valid(cell_id);
      break;
    case DetId::Forward:
      is_valid = noseTopology().valid(cell_id);
      break;
    default:
      is_valid = false;
      break;
  }
  return is_valid;
}

bool HGCalTriggerGeometryV9Imp3::validTriggerCellFromCells(const unsigned trigger_cell_id) const {
  // Check the validity of a trigger cell with the
  // validity of the cells. One valid cell in the
  // trigger cell is enough to make the trigger cell
  // valid.
  const geom_set cells = getCellsFromTriggerCell(trigger_cell_id);
  bool is_valid = false;
  for (const auto cell_id : cells) {
    unsigned det = DetId(cell_id).det();
    is_valid |= validCellId(det, cell_id);
    if (is_valid)
      break;
  }
  return is_valid;
}

bool HGCalTriggerGeometryV9Imp3::validCellId(unsigned subdet, unsigned cell_id) const {
  bool is_valid = false;
  switch (subdet) {
    case DetId::HGCalEE:
      is_valid = eeTopology().valid(cell_id);
      break;
    case DetId::HGCalHSi:
      is_valid = hsiTopology().valid(cell_id);
      break;
    case DetId::HGCalHSc:
      is_valid = hscTopology().valid(cell_id);
      break;
    case DetId::Forward:
      is_valid = noseTopology().valid(cell_id);
      break;
    default:
      is_valid = false;
      break;
  }
  return is_valid;
}

int HGCalTriggerGeometryV9Imp3::detIdWaferType(unsigned det, unsigned layer, short waferU, short waferV) const {
  int wafer_type = 0;
  switch (det) {
    case DetId::HGCalEE:
      wafer_type = eeTopology().dddConstants().getTypeHex(layer, waferU, waferV);
      break;
    case DetId::HGCalHSi:
      wafer_type = hsiTopology().dddConstants().getTypeHex(layer, waferU, waferV);
      break;
    default:
      break;
  };
  return wafer_type;
}

unsigned HGCalTriggerGeometryV9Imp3::layerWithOffset(unsigned id) const {
  unsigned det = DetId(id).det();
  unsigned layer = 0;

  if (det == DetId::HGCalTrigger) {
    unsigned subdet = HGCalTriggerDetId(id).subdet();
    if (subdet == HGCalTriggerSubdetector::HGCalEETrigger) {
      layer = HGCalTriggerDetId(id).layer();
    } else if (subdet == HGCalTriggerSubdetector::HGCalHSiTrigger) {
      layer = heOffset_ + HGCalTriggerDetId(id).layer();
    } else if (subdet == HGCalTriggerSubdetector::HFNoseTrigger) {
      layer = HFNoseTriggerDetId(id).layer();
    }
  } else if (det == DetId::HGCalHSc) {
    layer = heOffset_ + HGCScintillatorDetId(id).layer();
  } else if (det == DetId::Forward) {
    unsigned subdet = HGCalDetId(id).subdetId();
    if (subdet == ForwardSubdetector::HGCEE) {
      layer = HGCalDetId(id).layer();
    } else if (subdet == ForwardSubdetector::HGCHEF || subdet == ForwardSubdetector::HGCHEB) {
      layer = heOffset_ + HGCalDetId(id).layer();
    } else if (subdet == ForwardSubdetector::HFNose) {
      layer = HFNoseDetId(id).layer();
    }
  }
  return layer;
}

DEFINE_EDM_PLUGIN(HGCalTriggerGeometryFactory, HGCalTriggerGeometryV9Imp3, "HGCalTriggerGeometryV9Imp3");
