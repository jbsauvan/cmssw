#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/L1THGCal/interface/HGCalTriggerCell.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"

namespace l1t {
  class HGC3DTriggerCellGenMatchSelector : public edm::stream::EDProducer<> {
  public:
    explicit HGC3DTriggerCellGenMatchSelector(const edm::ParameterSet &);
    ~HGC3DTriggerCellGenMatchSelector() override {}

  private:
    edm::EDGetTokenT<l1t::HGCalTriggerCellBxCollection> src_;
    edm::EDGetToken genParticleSrc_;
    double dR_;
    void produce(edm::Event &, const edm::EventSetup &) override;

  };  // class
}  // namespace l1t

l1t::HGC3DTriggerCellGenMatchSelector::HGC3DTriggerCellGenMatchSelector(const edm::ParameterSet &iConfig)
    : src_(consumes<l1t::HGCalTriggerCellBxCollection>(iConfig.getParameter<edm::InputTag>("src"))),
      genParticleSrc_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genSrc"))),
      dR_(iConfig.getParameter<double>("dR")) {
  produces<l1t::HGCalTriggerCellBxCollection>();
}

void l1t::HGC3DTriggerCellGenMatchSelector::produce(edm::Event &iEvent, const edm::EventSetup &) {
  auto out = std::make_unique<l1t::HGCalTriggerCellBxCollection>();

  edm::Handle<l1t::HGCalTriggerCellBxCollection> triggercells;
  iEvent.getByToken(src_, triggercells);

  edm::Handle<reco::GenParticleCollection> genParticles;
  iEvent.getByToken(genParticleSrc_, genParticles);

  for (int bx = triggercells->getFirstBX(); bx <= triggercells->getLastBX(); ++bx) {
    for (auto it = triggercells->begin(bx), ed = triggercells->end(bx); it != ed; ++it) {
      const auto &triggercell = *it;
      for (const auto &particle : *genParticles) {
        if (particle.status() != 1)
          continue;
        if (deltaR(triggercell, particle) < dR_) {
          out->push_back(bx, triggercell);
          break;  // don't save duplicate trigger cells
        }
      }
    }
  }

  iEvent.put(std::move(out));
}
using l1t::HGC3DTriggerCellGenMatchSelector;
DEFINE_FWK_MODULE(HGC3DTriggerCellGenMatchSelector);
