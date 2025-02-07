{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
  pillow,
  numpy,
}:
mkAdafruitLib {
  pname = "adafruit_blinka_displayio";
  version = "0.11.1";
  format = "wheel";

  runtimeInputs = with raw-adafruit-noruntime; [adafruit-blinka adafruit-circuitpython-typing adafruit-circuitpython-bitmap-font] ++ [pillow numpy];

  src = {
    format = "wheel";
    python = "py3";
    dist = "py3";
    hash = "sha256-Y+LyCMVJhk4qvxkWtgPpcSH1x7QctBwmEib/ZG1qBbk=";
  };
}
