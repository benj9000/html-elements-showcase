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
            nativeBuildInputs =
              let
                prettierPluginJinjaTemplate = pkgs.buildNpmPackage rec {
                  pname = "prettier-plugin-jinja-template";
                  version = "v2.0.0";
                  src = pkgs.fetchFromGitHub {
                    owner = "davidodenwald";
                    repo = pname;
                    rev = version;
                    hash = "sha256-5xPR305Ux0SFhoBFJ3XdlOY2PqtAqZn1PQAy38HCJss=";
                  };
                  npmDepsHash = "sha256-dlQkvji36Za86lAt5ds8nphDnu2uA28tNZqZKzt2o5A=";
                  dontNpmPrune = true;
                };

                prettierWithPlugins = pkgs.symlinkJoin {
                  name = "prettier-with-plugins";
                  paths = [ pkgs.nodePackages.prettier ];
                  buildInputs = [ pkgs.makeWrapper ];
                  postBuild = ''
                    wrapProgram "$out/bin/prettier" \
                      --add-flags "--plugin=${prettierPluginJinjaTemplate}/lib/node_modules/prettier-plugin-jinja-template/lib/index.js" \
                      --add-flags "--print-width 100"
                  '';
                };
              in
              [
                pythonPackage
                pkgs.uv
                pkgs.basedpyright
                pkgs.ruff
                prettierWithPlugins
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
