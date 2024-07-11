#include "L1Trigger/L1THGCal/interface/HGCalTriggerGeoTesterBase.h"

const std::unordered_map<HGcalTriggerGeoTesterErrors::ErrorCode, std::string> HGcalTriggerGeoTesterErrors::messages = 
{ {HGcalTriggerGeoTesterErrors::CellValidity, "Found invalid cell(s)"},
  {HGcalTriggerGeoTesterErrors::MissingCellInTC, "Found missing cell(s) in trigger cell"},
  {HGcalTriggerGeoTesterErrors::InvalidCellInTC, "Found invalid cell(s) in trigger cell"},
  {HGcalTriggerGeoTesterErrors::MissingTCInModule, "Found missing trigger cell(s) in module"},
  {HGcalTriggerGeoTesterErrors::InvalidTCInModule, "Found invalid trigger cell(s) in module"}
};

EDM_REGISTER_PLUGINFACTORY(HGCalTriggerGeoTesterFactory, "HGCalTriggerGeoTesterFactory");
