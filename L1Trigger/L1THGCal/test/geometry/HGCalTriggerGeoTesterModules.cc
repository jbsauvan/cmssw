
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "DataFormats/ForwardDetId/interface/HGCalTriggerModuleDetId.h"
#include "L1Trigger/L1THGCal/interface/HGCalTriggerGeometryBase.h"
#include "L1Trigger/L1THGCal/interface/HGCalTriggerGeoTesterBase.h"
#include "L1Trigger/L1THGCal/interface/HGCalTriggerTools.h"

class HGCalTriggerGeoTesterModules : public HGCalTriggerGeoTesterBase {
public:
  HGCalTriggerGeoTesterModules(const edm::ParameterSet& conf);
  ~HGCalTriggerGeoTesterModules() override{};
  void initialize(TTree*, const edm::ParameterSet&) final;
  void check(const HGCalTriggerGeoTesterEventSetup& es) final;
  void fill(const HGCalTriggerGeoTesterEventSetup& es) final;

private:
  void clear() final;

  HGCalTriggerTools triggerTools_;

  unsigned id_ = 0;
  int disconnected_ = 0;
  int zside_ = 0;
  int subdet_ = 0;
  int sector_ = 0;
  int layer_ = 0;
  int u_ = 0;
  int v_ = 0;
  int ieta_ = 0;
  int iphi_ = 0;
  int type_ = 0;
  float x_ = 0.;
  float y_ = 0.;
  float z_ = 0.;
  float eta_ = 0.;
  float phi_ = 0.;
  int cells_n_ = 0;
  int triggercells_n_ = 0;
  std::vector<uint32_t> cells_;
  std::vector<uint32_t> triggercells_;

};

DEFINE_EDM_PLUGIN(HGCalTriggerGeoTesterFactory, HGCalTriggerGeoTesterModules, "HGCalTriggerGeoTesterModules");

HGCalTriggerGeoTesterModules::HGCalTriggerGeoTesterModules(const edm::ParameterSet& conf)
    : HGCalTriggerGeoTesterBase(conf) {
}

void HGCalTriggerGeoTesterModules::initialize(TTree* tree,
                                            const edm::ParameterSet& conf) {

  tree_ = tree;

  tree_->Branch("disconnected", &disconnected_, "disconnected/I");
  tree_->Branch("id", &id_, "id/i");
  tree_->Branch("zside", &zside_, "zside/I");
  tree_->Branch("subdet", &subdet_, "subdet/I");
  tree_->Branch("sector", &sector_, "sector/I");
  tree_->Branch("layer", &layer_, "layer/I");
  tree_->Branch("u", &u_, "u/I");
  tree_->Branch("v", &v_, "v/I");
  tree_->Branch("ieta", &ieta_, "ieta/I");
  tree_->Branch("iphi", &iphi_, "iphi/I");
  tree_->Branch("type", &type_, "type/i");
  tree_->Branch("x", &x_, "x/F");
  tree_->Branch("y", &y_, "y/F");
  tree_->Branch("z", &z_, "z/F");
  tree_->Branch("eta", &eta_, "eta/F");
  tree_->Branch("phi", &phi_, "phi/F");
  tree_->Branch("cells_n", &cells_n_, "cells_n/I");
  tree_->Branch("triggercells_n", &triggercells_n_, "triggercells_n/I");
  tree_->Branch("cells", &cells_);
  tree_->Branch("triggercells", &triggercells_);
}


void HGCalTriggerGeoTesterModules::fill(const HGCalTriggerGeoTesterEventSetup& es) {
  clear();
  edm::LogPrint("TreeFilling") << "Filling modules tree";
  // Create list of modules from valid cells
  std::unordered_set<uint32_t> modules;
  for (const auto& id : es.geometry->eeGeometry()->getValidDetIds()) {
    modules.insert(es.geometry->getModuleFromCell(id));
  }
  for (const auto& id : es.geometry->hsiGeometry()->getValidDetIds()) {
    modules.insert(es.geometry->getModuleFromCell(id));
  }
  for (const auto& id : es.geometry->hscGeometry()->getValidDetIds()) {
    modules.insert(es.geometry->getModuleFromCell(id));
  }
  for (const auto& id : modules) {
    HGCalTriggerModuleDetId detid(id);
    disconnected_ = es.geometry->disconnectedModule(id);
    id_ = id;
    zside_ = detid.zside();
    subdet_ = detid.subdetId();
    type_ = detid.type();
    layer_ = triggerTools_.layerWithOffset(id);
    if (triggerTools_.isSilicon(id)) {
      u_ = detid.moduleU();
      v_ = detid.moduleV();
      ieta_ = -999;
      iphi_ = -999;
    } else if (triggerTools_.isScintillator(id)) {
      u_ = -999;
      v_ = -999;
      ieta_ = detid.eta();
      iphi_ = detid.phi();
    } else {
      throw cms::Exception("InvalidHGCalTriggerDetid")
          << "Found unexpected module detid to be filled in HGCal trigger module ntuple.";
    }
    auto cells = es.geometry->getCellsFromModule(id);
    cells_n_ = cells.size();
    cells_.resize(cells.size());
    std::copy(cells.begin(), cells.end(), cells_.begin());
    auto tcs = es.geometry->getTriggerCellsFromModule(id);
    triggercells_n_ = tcs.size();
    triggercells_.resize(tcs.size());
    std::copy(tcs.begin(), tcs.end(), triggercells_.begin());
    //
    GlobalPoint center = es.geometry->getModulePosition(id);
    x_ = center.x();
    y_ = center.y();
    z_ = center.z();
    eta_ = center.eta();
    phi_ = center.phi();

    tree_->Fill();
    clear();
  }
}

void HGCalTriggerGeoTesterModules::check(const HGCalTriggerGeoTesterEventSetup& es) {
}


void HGCalTriggerGeoTesterModules::clear() {
  id_ = 0;
  disconnected_ = 0;
  zside_ = 0;
  subdet_ = 0;
  layer_ = 0;
  u_ = 0;
  v_ = 0;
  ieta_ = 0;
  iphi_ = 0;
  type_ = 0;
  x_ = 0.;
  y_ = 0.;
  z_ = 0.;
  eta_ = 0.;
  phi_ = 0.;
  cells_n_ = 0;
  triggercells_n_ = 0;
  cells_.clear();
  triggercells_.clear();
}
