{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
}:
mkAdafruitLib {
  pname = "adafruit_circuitpython_typing";
  version = "1.11.2";

  runtimeInputs = with raw-adafruit-noruntime; [adafruit-circuitpython-busdevice adafruit-circuitpython-requests];
  deferredInputs = ps: with ps.raw-adafruit-noruntime; [adafruit-blinka];

  src = {
    hash = "sha256-x6yFMqmtfkpl1ViHZLdIPAtpZ9MFw3+uvMDFNW1nfjM=";
  };
}
