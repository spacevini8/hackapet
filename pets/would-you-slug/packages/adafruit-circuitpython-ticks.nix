{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_ticks";
  version = "1.1.2";

  runtimeInputs = with raw-adafruit-noruntime; [adafruit-blinka];

  src = {
    hash = "sha256-+eiM8m9LTJDxScq/R5jdpAR9AgoFBniI2CA6jdKHNmQ=";
  };
}
