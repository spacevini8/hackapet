{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_bitmap_font";
  version = "2.1.4";

  runtimeInputs = with raw-adafruit-noruntime; [adafruit-blinka];
  deferredInputs = ps: with ps.raw-adafruit-noruntime; [adafruit-blinka-displayio];

  src = {
    hash = "sha256-ZPJLghM+TdMiFDglJUPHABym6DXHD4+eOzK780SRKUI=";
  };
}
