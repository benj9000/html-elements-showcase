{
  description = "HTML elements showcase";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonVersions = {
          default = pkgs.python314;
          python312 = pkgs.python312;
          python313 = pkgs.python313;
          python314 = pkgs.python314;
        };
        mkPythonShell = devShellName: pythonPackage:
          let venvDirectory = "venv"; in
          pkgs.mkShell {
            name = "python-uv-development-environment";
            nativeBuildInputs = [
              pythonPackage
              pkgs.uv
              pkgs.basedpyright
              pkgs.ruff
              pkgs.nodePackages.prettier
            ];
            UV_PROJECT_ENVIRONMENT = venvDirectory;
            UV_PYTHON_DOWNLOADS = "never";
            shellHook = ''
              echo "Start Python development environment with uv"
              uv sync --python ${pythonPackage}/bin/python
              if [ -d ${venvDirectory} ]; then
                  source ${venvDirectory}/bin/activate
              fi
            '';
          };
      in
      {
        devShells = builtins.mapAttrs mkPythonShell pythonVersions;
      }
    );
}
