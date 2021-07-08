#ifndef __L1Trigger_L1THGCal_HGCalStage1TruncationImpl_h__
#define __L1Trigger_L1THGCal_HGCalStage1TruncationImpl_h__

#include <array>
#include <string>
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1THGCal/interface/HGCalTriggerCell.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "L1Trigger/L1THGCal/interface/HGCalTriggerTools.h"
#include "Geometry/HGCalCommonData/interface/HGCalGeomRotation.h"

class HGCalStage1TruncationImpl {
public:
  HGCalStage1TruncationImpl(const edm::ParameterSet& conf);

  void eventSetup(const edm::EventSetup& es) { triggerTools_.eventSetup(es); }

  void run(const std::vector<edm::Ptr<l1t::HGCalTriggerCell>>& tcs_in,
            std::vector<edm::Ptr<l1t::HGCalTriggerCell>>& tcs_out);

private:
  HGCalTriggerTools triggerTools_;
  HGCalGeomRotation geom_rotation_120_ = {HGCalGeomRotation::SectorType::Sector120Degrees};

  double roz_min_ = 0.;
  double roz_max_ = 0.;
  unsigned roz_bins_ = 42;
  std::vector<unsigned> max_tcs_per_bin_;
  std::vector<double> phi_edges_;
  double roz_bin_size_ = 0.;

  uint32_t packBin(int roverzbin, unsigned phibin) const;
  void unpackBin(unsigned packedbin, unsigned& roverzbin, unsigned& phibin) const;
  unsigned phiBin(int roverzbin, double phi) const;
  double rotatedphi(double x, double y, double z, int sector) const;


  // TODO: move it to trigger tools, or make it accessible by geometry (better?)
  unsigned sector(const l1t::HGCalTriggerCell& tc) const;
  HGCalGeomRotation::WaferCentring getWaferCentring(unsigned layer, int subdet) const;
  unsigned sectorFromEtaPhi(int ieta, int iphi) const;

};

#endif
