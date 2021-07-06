#include "L1Trigger/L1THGCal/interface/backend/HGCalBackendStage1Processor.h"

DEFINE_EDM_PLUGIN(HGCalBackendLayer1Factory, HGCalBackendStage1Processor, "HGCalBackendStage1Processor");

HGCalBackendStage1Processor::HGCalBackendStage1Processor(const edm::ParameterSet& conf)
    : HGCalBackendLayer1ProcessorBase(conf) {
  clusteringDummy_ = std::make_unique<HGCalClusteringDummyImpl>(conf.getParameterSet("C2d_parameters"));
}

void HGCalBackendStage1Processor::run(const edm::Handle<l1t::HGCalTriggerCellBxCollection>& collHandle,
                                      l1t::HGCalClusterBxCollection& collCluster2D,
                                      const edm::EventSetup& es) {
  if (clusteringDummy_)
    clusteringDummy_->eventSetup(es);

  std::unordered_map<uint32_t, std::vector<edm::Ptr<l1t::HGCalTriggerCell>>> tcs_per_fpga;

  for (unsigned i = 0; i < collHandle->size(); ++i) {
    edm::Ptr<l1t::HGCalTriggerCell> tc_ptr(collHandle, i);
    uint32_t module = geometry_->getModuleFromTriggerCell(tc_ptr->detId());
    uint32_t fpga = geometry_->getStage1FpgaFromModule(module);
    tcs_per_fpga[fpga].push_back(tc_ptr);
  }

  for (auto& fpga_tcs : tcs_per_fpga) {
    l1t::HGCalClusterBxCollection clusters;
    std::sort(fpga_tcs.second.begin(),
              fpga_tcs.second.end(),
              [](const edm::Ptr<l1t::HGCalTriggerCell>& a, const edm::Ptr<l1t::HGCalTriggerCell>& b) -> bool {
                return a->mipPt() > b->mipPt();
              });
    clusteringDummy_->clusterizeDummy(fpga_tcs.second, clusters);
    for (unsigned i = 0; i < clusters.size(0); i++) {
      collCluster2D.push_back(0, clusters.at(0, i));
    }
  }
}
