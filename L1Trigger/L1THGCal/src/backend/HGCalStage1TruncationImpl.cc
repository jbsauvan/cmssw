#include "L1Trigger/L1THGCal/interface/backend/HGCalStage1TruncationImpl.h"
#include <cmath>

#include "DataFormats/ForwardDetId/interface/HFNoseTriggerDetId.h"
#include "DataFormats/ForwardDetId/interface/HGCScintillatorDetId.h"
#include "DataFormats/ForwardDetId/interface/HGCalTriggerDetId.h"



HGCalStage1TruncationImpl::HGCalStage1TruncationImpl(const edm::ParameterSet& conf)
    : roz_min_(conf.getParameter<double>("rozMin")),
      roz_max_(conf.getParameter<double>("rozMax")),
      roz_bins_(conf.getParameter<unsigned>("rozBins")),
      max_tcs_per_bin_(conf.getParameter<std::vector<unsigned>>("maxTcsPerBin")),
      phi_edges_(conf.getParameter<std::vector<double>>("phiSectorEdges")) {

  constexpr double margin = 1.001;
  roz_bin_size_ = (roz_max_ - roz_min_)*margin/double(roz_bins_);
}

void HGCalStage1TruncationImpl::run(const std::vector<edm::Ptr<l1t::HGCalTriggerCell>>& tcs_in,
    std::vector<edm::Ptr<l1t::HGCalTriggerCell>>& tcs_out) {

  std::unordered_map<unsigned, std::vector<edm::Ptr<l1t::HGCalTriggerCell>>> tcs_per_bin;

  for (const auto& tc : tcs_in) {
    const GlobalPoint& position = tc->position();
    double x = position.x();
    double y = position.y();
    double z = position.z();
    double roverz = std::sqrt(x*x + y*y)/std::abs(z);
    roverz = (roverz < roz_min_ ? roz_min_ : roverz);
    roverz = (roverz > roz_max_ ? roz_max_ : roverz);
    int roverzbin = int((roverz-roz_min_)/roz_bin_size_);
    unsigned sector120 = sector(*tc);
    double phi = rotatedphi(x, y, z, sector120);
    unsigned phibin = phiBin(roverzbin, phi);
    unsigned packed_bin = packBin(roverzbin, phibin);

    tcs_per_bin[packed_bin].push_back(tc);
  }
  for (auto& bin_tcs : tcs_per_bin) {
    std::sort(bin_tcs.second.begin(),
              bin_tcs.second.end(),
              [](const edm::Ptr<l1t::HGCalTriggerCell>& a, const edm::Ptr<l1t::HGCalTriggerCell>& b) -> bool {
                return a->mipPt() > b->mipPt();
              });

    unsigned roverzbin = 0;
    unsigned phibin = 0;
    unpackBin(bin_tcs.first, roverzbin, phibin);
    unsigned max_tc = max_tcs_per_bin_[roverzbin];
    // keep only N trigger cells
    if (bin_tcs.second.size() > max_tc) {
      bin_tcs.second.resize(max_tc);
    }
    for(const auto& tc : bin_tcs.second) {
      tcs_out.push_back(tc);
    }
  }
}

unsigned HGCalStage1TruncationImpl::packBin(int roverzbin, unsigned phibin) const {
  // TODO: make these class members
  unsigned offset_roz = 1;
  unsigned mask_roz = 6; // max 64 bins
  unsigned mask_phi = 1;
  unsigned packed_bin = 0;
  packed_bin |= ((roverzbin & mask_roz) << offset_roz );
  packed_bin |= (phibin & mask_phi);
  return packed_bin;
}


void HGCalStage1TruncationImpl::unpackBin(unsigned packedbin, unsigned& roverzbin, unsigned& phibin) const {
  // TODO: make these class members
  unsigned offset_roz = 1;
  unsigned mask_roz = 6; // max 64 bins
  unsigned mask_phi = 1;
  roverzbin = (packedbin >> offset_roz) & mask_roz;
  phibin = packedbin & mask_phi;
}


unsigned HGCalStage1TruncationImpl::phiBin(int roverzbin, double phi) const {
  unsigned phi_bin = 0;
  double phi_edge = phi_edges_[roverzbin];
  if (phi>phi_edge)
    phi_bin = 1;
  return phi_bin;
}


double HGCalStage1TruncationImpl::rotatedphi(double x, double y, double z, int sector) const {
  if (z > 0)
    x = -x;
  double phi = std::atan2(y, x);

  if (sector == 1) {
    if ( phi < M_PI and phi > 0)
      phi = phi-(2.*M_PI/3.);
    else
      phi = phi+(4.*M_PI/3.);
  }
  else if (sector == 2) {
    phi = phi+(2.*M_PI/3.);
  }
  return phi;
}

// TODO: move it to trigger tools
HGCalGeomRotation::WaferCentring HGCalStage1TruncationImpl::getWaferCentring(unsigned layer, int subdet) const {
  if (subdet == HGCalTriggerSubdetector::HGCalEETrigger) {  // CE-E
    return HGCalGeomRotation::WaferCentring::WaferCentred;
  } else if (subdet == HGCalTriggerSubdetector::HGCalHSiTrigger) {
    if ((layer % 2) == 1) {  // CE-H Odd
      return HGCalGeomRotation::WaferCentring::CornerCentredY;
    } else {  // CE-H Even
      return HGCalGeomRotation::WaferCentring::CornerCentredMercedes;
    }
  } else if (subdet == HGCalTriggerSubdetector::HFNoseTrigger) {  //HFNose
    return HGCalGeomRotation::WaferCentring::WaferCentred;
  } else {
    edm::LogError("HGCalStage1TruncationImpl")
        << "HGCalTriggerGeometryV9Imp3: trigger sub-detector expected to be silicon";
    return HGCalGeomRotation::WaferCentring::WaferCentred;
  }
}

// TODO: move it to trigger tools, or make it available from geometry (better)
unsigned HGCalStage1TruncationImpl::sectorFromEtaPhi(int ieta, int iphi) const {
  unsigned sector = 0;
  unsigned hSc_num_panels_per_sector = 8;

  if (unsigned(std::abs(iphi)) > 2 * hSc_num_panels_per_sector)
    sector = 2;
  else if (unsigned(std::abs(iphi)) > hSc_num_panels_per_sector)
    sector = 1;
  else
    sector = 0;

  iphi = iphi - (sector * hSc_num_panels_per_sector);

  return sector;
}


  // TODO: move it to trigger tools, or make it accessible by geometry (better?)
unsigned HGCalStage1TruncationImpl::sector(const l1t::HGCalTriggerCell& tc) const {
  unsigned det = DetId(tc.detId()).det();
  unsigned sector = 0;

  if (det == DetId::HGCalHSc) {
    HGCScintillatorDetId detid(tc.detId());
    sector = sectorFromEtaPhi(detid.ietaAbs(), detid.iphi());
  }
  else if (det == DetId::HGCalTrigger and
           HGCalTriggerDetId(tc.detId()).subdet() == HGCalTriggerSubdetector::HFNoseTrigger) {
    HFNoseTriggerDetId detid(tc.detId());
    int layer = detid.layer();
    int waferu = detid.waferU();
    int waferv = detid.waferV();
    sector = geom_rotation_120_.uvMappingToSector0(
        getWaferCentring(layer, HGCalTriggerSubdetector::HFNoseTrigger), waferu, waferv);
  }
  else {
    HGCalTriggerDetId detid(tc.detId());
    unsigned subdet = detid.subdet();
    int layer = detid.layer();
    int waferu = detid.waferU();
    int waferv = detid.waferV();
    sector = geom_rotation_120_.uvMappingToSector0(getWaferCentring(layer, subdet), waferu, waferv);
  }
  return sector;
}
