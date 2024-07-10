#include "L1Trigger/L1THGCal/interface/HGCalTriggerGeoTesterBase.h"

const std::unordered_map<HGcalTriggerGeoTesterErrors::ErrorCode, std::string> HGcalTriggerGeoTesterErrors::messages = 
{ {HGcalTriggerGeoTesterErrors::CellValidity, "Found invalid cell(s)"},
  {HGcalTriggerGeoTesterErrors::MissingCellInTC, "Found missing cell(s) in trigger cell"},
  {HGcalTriggerGeoTesterErrors::InvalidCellInTC, "Found invalid cell(s) in trigger cell"},
  {HGcalTriggerGeoTesterErrors::ModuleMapping, "Found inconsistencies in trigger module mapping"}
};

EDM_REGISTER_PLUGINFACTORY(HGCalTriggerGeoTesterFactory, "HGCalTriggerGeoTesterFactory");
