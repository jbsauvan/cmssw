#ifndef L1Trigger_L1THGCal_HGCalModuleDetId_H
#define L1Trigger_L1THGCal_HGCalModuleDetId_H 1

#include <iosfwd>
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/ForwardDetId/interface/ForwardSubdetector.h"

/* \brief description of the bit assigment
   [0:3]  u-coordinate of the silicon module (u-axis points along -x axis)
          or eta-coordinate of the scintillator module
   [4:7]  v-coordinate of the silicon module (v-axis points 60-degree wrt x-axis)
          or phi-coordinate of the scintillator module
   [8:9] sector (0,1,2 counter-clockwise from u-axis)

   [10:16] reserved for future use

   [17:21] layer number 
   [22:23] Type (0 fine divisions of wafer with 120 mum thick silicon
                 1 coarse divisions of wafer with 200 mum thick silicon
                 2 coarse divisions of wafer with 300 mum thick silicon
                 0 fine divisions of scintillators
                 1 coarse divisions of scintillators)

   [24:24] z-side (0 for +z; 1 for -z)
   [25:27] Subdetector Type (HGCEE/HGCHEF/HGCHEB/HFNose)
   [28:31] Detector type (Forward)
*/

class HGCalModuleDetId : public DetId {
public:
  /** Create a null cellid*/
  HGCalModuleDetId();
  /** Create cellid from raw id (0=invalid tower id) */
  HGCalModuleDetId(uint32_t rawid);
  /** Constructor from subdetector, zplus, type, layer, sector, module numbers */
  HGCalModuleDetId(ForwardSubdetector subdet, int zp, int type, int layer, int sector, int moduleU, int moduleV);
  /** Constructor from a generic cell id */
  HGCalModuleDetId(const DetId& id);
  /** Assignment from a generic cell id */
  HGCalModuleDetId& operator=(const DetId& id);

  /// get the type
  int type() const { return (id_ >> kHGCalTypeOffset) & kHGCalTypeMask; }

  /// get the z-side of the cell (1/-1)
  int zside() const { return ((id_ >> kHGCalZsideOffset) & kHGCalZsideMask ? -1 : 1); }

  /// get the layer #
  int layer() const { return (id_ >> kHGCalLayerOffset) & kHGCalLayerMask; }

  /// get the sector #
  int sector() const { return (id_ >> kHGCalSectorOffset) & kHGCalSectorMask; }

  /// get the module U
  int moduleU() const { return (id_ >> kHGCalModuleUOffset) & kHGCalModuleUMask; }

  /// get the module V
  int moduleV() const { return (id_ >> kHGCalModuleVOffset) & kHGCalModuleVMask; }

  /// get the scintillator panel eta
  int eta() const { return moduleU(); }

  /// get the scintillator panel phi
  int phi() const { return moduleV(); }

  /// consistency check : no bits left => no overhead
  bool isHFNose() const { return (subdetId() == HFNose); }
  bool isEE() const { return (subdetId() == HGCEE); }
  bool isHSilicon() const { return (subdetId() == HGCHEF); }
  bool isHScintillator() const { return (subdetId() == HGCHEB); }
  bool isForward() const { return true; }

  static const HGCalModuleDetId Undefined;

  static const int kHGCalModuleUOffset = 0;
  static const int kHGCalModuleUMask = 0xF;
  static const int kHGCalModuleVOffset = 4;
  static const int kHGCalModuleVMask = 0xF;
  static const int kHGCalSectorOffset = 8;
  static const int kHGCalSectorMask = 0x3;
  static const int kHGCalLayerOffset = 17;
  static const int kHGCalLayerMask = 0x1F;
  static const int kHGCalTypeOffset = 22;
  static const int kHGCalTypeMask = 0x3;
  static const int kHGCalZsideOffset = 24;
  static const int kHGCalZsideMask = 0x1;
};

std::ostream& operator<<(std::ostream&, const HGCalModuleDetId& id);

#endif
