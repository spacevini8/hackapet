{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_display_text";
  version = "3.2.2";

  runtimeInputs = with raw-adafruit-noruntime; [adafruit-blinka-displayio adafruit-blinka adafruit-circuitpython-bitmap-font adafruit-circuitpython-ticks];

  src = {
    hash = "sha256-4TKrQidduvg6Z8Lo2pmNyQEE6GXurcChbg+5f702luU=";
  };
}
