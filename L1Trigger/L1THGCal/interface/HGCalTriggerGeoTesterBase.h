#ifndef __L1Trigger_L1THGCal_HGCalTriggerGeoTesterBase_h__
#define __L1Trigger_L1THGCal_HGCalTriggerGeoTesterBase_h__

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "TTree.h"

namespace HepPDT {
  class ParticleDataTable;
}
class MagneticField;
class HGCalTriggerGeometryBase;

struct HGCalTriggerGeoTesterEventSetup {
  edm::ESHandle<HGCalTriggerGeometryBase> geometry;
};

class HGCalTriggerGeoTesterBase {
public:
  HGCalTriggerGeoTesterBase(const edm::ParameterSet& conf) : name_(conf.getParameter<std::string>("TesterName")){};
  virtual ~HGCalTriggerGeoTesterBase(){};
  const std::string& name() const { return name_; }
  virtual void initialize(TTree*, const edm::ParameterSet&) = 0;
  virtual void check(const HGCalTriggerGeoTesterEventSetup&) = 0;
  virtual void fill(const HGCalTriggerGeoTesterEventSetup&) = 0;

protected:
  virtual void clear() = 0;
  const std::string name_;
  TTree* tree_;
};

#include "FWCore/PluginManager/interface/PluginFactory.h"
typedef edmplugin::PluginFactory<HGCalTriggerGeoTesterBase*(const edm::ParameterSet&)> HGCalTriggerGeoTesterFactory;

#endif
