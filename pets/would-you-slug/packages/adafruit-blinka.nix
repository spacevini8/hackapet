{
  lib,
  mkAdafruitLib,
  raw-adafruit-noruntime,
  adafruit-platformdetect,
  adafruit-pureio,
  binho-host-adapter,
  pyftdi,
  sysv-ipc,
}:
mkAdafruitLib {
  pname = "adafruit_blinka";
  version = "8.51.0";

  runtimeInputs = with raw-adafruit-noruntime; [adafruit-circuitpython-typing] ++ [adafruit-platformdetect adafruit-pureio binho-host-adapter pyftdi sysv-ipc];

  src = {
    hash = "sha256-hE8Vvnde5cQYRGlppCfFo4R5KOZE8rGjVUKs/1sgjzo=";
  };
}
