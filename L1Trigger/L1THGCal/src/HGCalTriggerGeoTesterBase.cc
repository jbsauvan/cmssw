#include "L1Trigger/L1THGCal/interface/HGCalTriggerGeoTesterBase.h"

const std::unordered_map<HGcalTriggerGeoTesterErrors::ErrorCode, std::string> HGcalTriggerGeoTesterErrors::messages = 
{ {HGcalTriggerGeoTesterErrors::CellValidity, "Found invalid cell(s)"},
  {HGcalTriggerGeoTesterErrors::MissingCellInTC, "Found missing cell(s) in trigger cell"},
  {HGcalTriggerGeoTesterErrors::InvalidCellInTC, "Found invalid cell(s) in trigger cell"},
  {HGcalTriggerGeoTesterErrors::MissingTCInModule, "Found missing trigger cell(s) in module"},
  {HGcalTriggerGeoTesterErrors::InvalidTCInModule, "Found invalid trigger cell(s) in module"},
  {HGcalTriggerGeoTesterErrors::ModuleSplitInStage1, "Found module with lpGBTs connected to several Stage 1 FPGAs"},
  {HGcalTriggerGeoTesterErrors::MissingModuleInStage1FPGA, "Found missing module(s) in Stage 1 FPGA"},
  {HGcalTriggerGeoTesterErrors::InvalidModuleInStage1FPGA, "Found invalid module(s) in Stage 1 FPGA"}
};

EDM_REGISTER_PLUGINFACTORY(HGCalTriggerGeoTesterFactory, "HGCalTriggerGeoTesterFactory");
