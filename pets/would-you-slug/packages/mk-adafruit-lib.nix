{
  lib,
  buildPythonPackage,
  pythonRuntimeDepsCheckHook,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
  makeSetupHook,
  writeScript,
} @ pkgs: let
  cleanAttrs = lib.flip removeAttrs ["checkRuntimeDeps" "deferredInputs"];

  exportWheelHook =
    makeSetupHook
    {
      name = "exportWheelsHook";
    }
    (writeScript
      "export-wheels-hook.sh.sh"
      ''
        exportWheelsHook() {
          mkdir -p $out/dist

          for wheel in dist/*.whl; do
            cp $wheel $out/dist/
          done
        }

        echo "Using exportWheelsHook"
        appendToVar preInstallPhases exportWheelsHook
      '');
in
  {
    pname,
    version,
    runtimeInputs ? [],
    deferredInputs ? ps: [],
    checkRuntimeDeps ? false,
    src ? {},
    ...
  } @ attrs: let
    rawPackage = buildPythonPackage ((cleanAttrs attrs)
      // {
        inherit pname version;

        nativeBuildInputs = [exportWheelHook];
        propagatedBuildInputs = runtimeInputs;

        src = fetchPypi (src
          // {
            inherit pname version;
          });

        pyproject =
          if attrs ? format
          then null
          else true;
        build-system = [
          setuptools-scm
          setuptools
          wheel
        ];

        dontCheckRuntimeDeps = !checkRuntimeDeps;
      });

    finalPackage = buildPythonPackage {
      inherit pname version;

      nativeBuildInputs = [pythonRuntimeDepsCheckHook];
      propagatedBuildInputs = [rawPackage] ++ deferredInputs pkgs;

      unpackPhase = ''
        runHook preUnpack

        mkdir -p dist
        cp ${rawPackage}/dist/*.whl dist
      '';

      format = "other";
    };
  in {
    rawPackage = rawPackage;
    package = finalPackage;
  }
