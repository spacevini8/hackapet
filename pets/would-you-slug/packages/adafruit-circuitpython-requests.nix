{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_requests";
  version = "4.1.9";

  runtimeInputs = with raw-adafruit-noruntime; [adafruit-circuitpython-connectionmanager];
  deferredInputs = ps: with ps.raw-adafruit-noruntime; [adafruit-blinka];

  src = {
    hash = "sha256-ue6yUrQ5RvGpDDTKiETge7HgHNIQySf1YdDhC5fF/50=";
  };
}
