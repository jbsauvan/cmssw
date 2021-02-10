#include "DataFormats/ForwardDetId/interface/HFNoseDetIdToModule.h"

HFNoseDetIdToModule::HFNoseDetIdToModule() {}

std::vector<HFNoseDetId> HFNoseDetIdToModule::getDetIds(HFNoseDetId const& id) const {
  std::vector<HFNoseDetId> ids;
  int nCells = (id.type() == 0) ? HFNoseDetId::HFNoseFineN : HFNoseDetId::HFNoseCoarseN;
  for (int u = 0; u < 2 * nCells; ++u) {
    for (int v = 0; v < 2 * nCells; ++v) {
      if (((v - u) < nCells) && (u - v) <= nCells) {
        HFNoseDetId newId(id.zside(), id.type(), id.layer(), id.waferU(), id.waferV(), u, v);
        ids.emplace_back(newId);
      }
    }
  }
  return ids;
}

std::vector<HFNoseTriggerDetId> HFNoseDetIdToModule::getTriggerDetIds(HFNoseDetId const& id) const {
  std::vector<HFNoseTriggerDetId> ids;
  int nCells = HFNoseDetId::HFNoseFineN / HFNoseDetId::HFNoseFineTrigger;
  for (int u = 0; u < 2 * nCells; ++u) {
    for (int v = 0; v < 2 * nCells; ++v) {
      if (((v - u) < nCells) && (u - v) <= nCells) {
        HFNoseTriggerDetId newId(HFNoseTrigger, id.zside(), id.type(), id.layer(), id.waferU(), id.waferV(), u, v);
        ids.emplace_back(newId);
      }
    }
  }
  return ids;
}

std::vector<HFNoseTriggerDetId> HFNoseDetIdToModule::getTriggerDetIds(HGCalModuleDetId const& id) const {
  std::vector<HFNoseTriggerDetId> ids;
  int nCells = HFNoseDetId::HFNoseFineN / HFNoseDetId::HFNoseFineTrigger;

  int moduleU = 0;
  int moduleV = 0;

  HGCalGeomRotation::WaferCentring centring;
  if (id.layer() <= 28) {  // CE-E
    centring = HGCalGeomRotation::WaferCentring::WaferCentred;
  } else if ((id.layer() % 2) == 1) {  // CE-H Odd
    centring =  HGCalGeomRotation::WaferCentring::CornerCentredY;
  } else {  // CE-H Even
    centring = HGCalGeomRotation::WaferCentring::CornerCentredMercedes;
  }

  geom_rotation_120_.uvMappingFromSector0( centring, moduleU, moduleV, id.sector() );

  for (int u = 0; u < 2 * nCells; ++u) {
    for (int v = 0; v < 2 * nCells; ++v) {
      if (((v - u) < nCells) && (u - v) <= nCells) {
        HFNoseTriggerDetId newId(HFNoseTrigger, id.zside(), id.type(), id.layer(), moduleU, moduleV, u, v);
        ids.emplace_back(newId);
      }
    }
  }
  return ids;
}

