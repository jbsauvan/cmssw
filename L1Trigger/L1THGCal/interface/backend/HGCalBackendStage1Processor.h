#ifndef __L1Trigger_L1THGCal_HGCalBackendStage1Processor_h__
#define __L1Trigger_L1THGCal_HGCalBackendStage1Processor_h__

#include "L1Trigger/L1THGCal/interface/HGCalProcessorBase.h"

#include "L1Trigger/L1THGCal/interface/HGCalTriggerTools.h"
#include "DataFormats/L1THGCal/interface/HGCalTriggerCell.h"
#include "DataFormats/L1THGCal/interface/HGCalCluster.h"

#include "L1Trigger/L1THGCal/interface/backend/HGCalClusteringDummyImpl.h"

class HGCalBackendStage1Processor : public HGCalBackendLayer1ProcessorBase {
public:
  HGCalBackendStage1Processor(const edm::ParameterSet& conf);

  void run(const edm::Handle<l1t::HGCalTriggerCellBxCollection>& collHandle,
      l1t::HGCalClusterBxCollection& collCluster2D,
      const edm::EventSetup& es) override;

private:
  /* algorithms instances */
  std::unique_ptr<HGCalClusteringDummyImpl> clusteringDummy_;

};

#endif
