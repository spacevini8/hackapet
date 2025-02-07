{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    pyproject-nix,
  } @ inputs:
    flake-utils.lib.eachDefaultSystem
    (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        lib = pkgs.lib;

        pyproject = pyproject-nix.lib.project.loadPyproject {projectRoot = ./.;};

        callAdafruitPackages = names: pypkgs: let
          packagesList =
            lib.map (name: let
              library = pypkgs.callPackage ./packages/${name}.nix {};
            in {
              raw-adafruit-noruntime.${name} = library.rawPackage;
              ${name} = library.package;
            })
            names;
          packages = lib.foldl (a: b: lib.recursiveUpdate a b) {} packagesList;
        in
          packages;

        python = pkgs.python3.override {
          packageOverrides = pyfinal: pyprev:
            {
              mkAdafruitLib = pyfinal.callPackage ./packages/mk-adafruit-lib.nix {};
              blinka-displayio-pygamedisplay = pyfinal.callPackage ./packages/blinka-displayio-pygamedisplay.nix {};
            }
            // callAdafruitPackages [
              "adafruit-blinka-displayio"
              "adafruit-blinka"
              "adafruit-circuitpython-bitmap-font"
              "adafruit-circuitpython-busdevice"
              "adafruit-circuitpython-connectionmanager"
              "adafruit-circuitpython-display-text"
              "adafruit-circuitpython-requests"
              "adafruit-circuitpython-ticks"
              "adafruit-circuitpython-typing"
            ]
            pyfinal;
        };

        projectPackages = pyproject.renderers.withPackages {inherit python;};

        pythonEnv = python.withPackages projectPackages;
      in {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [alejandra pythonEnv aseprite fontforge-gtk];
        };
      }
    );
}
