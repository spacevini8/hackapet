{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
  adafruit-circuitpython-typing,
  adafruit-blinka,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_busdevice";
  version = "5.2.11";

  deferredInputs = ps: with ps.raw-adafruit-noruntime; [adafruit-blinka adafruit-circuitpython-typing];

  src = {
    hash = "sha256-qaExC+5wIXA8zCR7s/8E0Ic1c5SKbHvukBY2HNZwenE=";
  };
}
