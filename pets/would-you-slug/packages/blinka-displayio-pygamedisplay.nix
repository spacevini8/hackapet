{
  lib,
  buildPythonPackage,
  fetchFromGitHub,
  setuptools,
  setuptools-scm,
  wheel,
  pygame,
  adafruit-blinka-displayio,
}:
buildPythonPackage rec {
  pname = "blinka-displayio-pygamedisplay";
  version = "2.4.0";

  propagatedBuildInputs = [pygame adafruit-blinka-displayio];

  src = fetchFromGitHub {
    owner = "CyrilSLi";
    repo = "Blinka_Displayio_PyGameDisplay";
    rev = "a7262ebd1e4f103f9aa7bc4c8c26aacd4e21259f";
    hash = "sha256-ySHwYBi1ogj26P/cGenl0z8deWYmmrZ5dUYqIY54mtE=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];
}
