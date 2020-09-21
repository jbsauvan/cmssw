#include "L1Trigger/L1THGCal/interface/veryfrontend/HGCalVFELinearizationImpl.h"
#include "SimCalorimetry/HGCalSimAlgos/interface/HGCalSiNoiseMap.h"

#include <cmath>

HGCalVFELinearizationImpl::HGCalVFELinearizationImpl(const edm::ParameterSet& conf)
    : linLSB_(conf.getParameter<double>("linLSB")),
      adcsaturation_(conf.getParameter<double>("adcsaturation")),
      tdcnBits_(conf.getParameter<uint32_t>("tdcnBits")),
      tdcOnset_(conf.getParameter<double>("tdcOnset")),
      adcnBits_(conf.getParameter<uint32_t>("adcnBits")),
      tdcsaturation_(conf.getParameter<double>("tdcsaturation")),
      linnBits_(conf.getParameter<uint32_t>("linnBits")),
      oot_coefficients_(conf.getParameter<std::vector<double>>("oot_coefficients")),
      new_digi_(conf.getParameter<bool>("newDigi")) {
  constexpr int kOot_order = 2;
  if (oot_coefficients_.size() != kOot_order) {
    throw cms::Exception("BadConfiguration") << "OOT subtraction needs " << kOot_order << " coefficients";
  }
  adcLSB_ = std::ldexp(adcsaturation_, -adcnBits_);
  tdcLSB_ = std::ldexp(tdcsaturation_, -tdcnBits_);
  linMax_ = (0x1 << linnBits_) - 1;

}


void HGCalVFELinearizationImpl::linearize(const std::vector<HGCalDataFrame>& dataframes,
                                          std::vector<std::pair<DetId, uint32_t>>& linearized_dataframes) {
  constexpr int kIntimeSample = 2;
  constexpr int kOuttime1Sample = 1;  // in time - 1;
  constexpr int kOuttime2Sample = 0;  // in time - 2;

  for (const auto& frame : dataframes) {  //loop on DIGI
    bool isTDC( frame[kIntimeSample].mode() );
    double rawData( double(frame[kIntimeSample].data()) );
    bool isBusy( isTDC && rawData==0 );


    double adcLSB = adcLSB_;
    if(new_digi_) {
      auto gain = static_cast<HGCalSiNoiseMap::GainRange_t>(frame[kIntimeSample].gain());
      if(gain==HGCalSiNoiseMap::q80fC) adcLSB=1./80.;
      else if(gain==HGCalSiNoiseMap::q160fC) adcLSB=1./160.;
      else if(gain==HGCalSiNoiseMap::q320fC) adcLSB=1./320.;
    }

    double amplitude = 0.;
    if(isBusy) {
      continue;
    }
    if (isTDC) {  
      amplitude = (std::floor(tdcOnset_ / adcLSB) + 1.0) * adcLSB + rawData * tdcLSB_;
    } else {  //ADC mode
      double data = rawData;
      // applies OOT PU subtraction only in the ADC mode
      if (!frame[kOuttime1Sample].mode()) {
        data += oot_coefficients_[kOuttime1Sample] * frame[kOuttime1Sample].data();
        if (!frame[kOuttime2Sample].mode()) {
          data += oot_coefficients_[kOuttime2Sample] * frame[kOuttime2Sample].data();
        }
      }
      amplitude = std::max(0., data) * adcLSB;
    }
    uint32_t amplitude_int = uint32_t(std::floor(amplitude / linLSB_ + 0.5));
    if (amplitude_int == 0)
      continue;
    if (amplitude_int > linMax_)
      amplitude_int = linMax_;

    linearized_dataframes.emplace_back(frame.id(), amplitude_int);
  }
}
