{
  description = "HTML elements showcase";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, pyproject-nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        src = ./.;
        pyproject = pyproject-nix.lib.project.loadUVPyproject { projectRoot = src; };
        projectName = pyproject.pyproject.project.name;

        pkgs = nixpkgs.legacyPackages.${system};
        defaultPythonPackage = pkgs.python314;
        pythonPackages = {
          default = defaultPythonPackage;
          "${projectName}" = defaultPythonPackage;
          "${projectName}-py312" = pkgs.python312;
          "${projectName}-py313" = pkgs.python313;
          "${projectName}-py314" = pkgs.python314;
        };

        mkPythonShell = devShellName: pythonPackage:
          let
            pyprojectToml = "./pyproject.toml";
            venvDirectory = "./venv";
            directoryToLiveServe = "./dist/html-elements-showcase";
          in
          pkgs.mkShell {
            name = "${projectName}-development-environment";
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

                liveServerScripts = pkgs.symlinkJoin {
                  name = "live-server-scripts-${projectName}";
                  paths =
                    let
                      liveServerTmuxSessionName = "live server (${projectName})";
                      startLiveServerScript = pkgs.writeShellScriptBin "start-live-server" ''
                        if [ ! -d ${directoryToLiveServe} ]; then
                            echo "Could not detect the directory to serve."
                            echo "Make sure to call this command from within the project's root directory."
                            exit 1
                        fi
                        ${pkgs.tmux}/bin/tmux new-session -s "${liveServerTmuxSessionName}" -d \
                            "${pkgs.nodePackages.live-server}/bin/live-server ${directoryToLiveServe}"
                      '';
                      stopLiveServerScript = pkgs.writeShellScriptBin "stop-live-server" ''
                        ${pkgs.tmux}/bin/tmux kill-session -t "${liveServerTmuxSessionName}"
                      '';
                      showLiveServerScript = pkgs.writeShellScriptBin "show-live-server" ''
                        ${pkgs.tmux}/bin/tmux attach-session -t "${liveServerTmuxSessionName}"
                      '';
                    in
                    [ startLiveServerScript stopLiveServerScript showLiveServerScript ];
                };
              in
              [
                pythonPackage
                pkgs.uv
                pkgs.basedpyright
                pkgs.ruff
                prettierWithPlugins
                liveServerScripts
              ];

            env = {
              UV_PROJECT_ENVIRONMENT = venvDirectory;
              UV_PYTHON = pythonPackage.interpreter;
              UV_PYTHON_DOWNLOADS = "never";
            };

            shellHook = ''
              unset PYTHONPATH
              [ -f "${pyprojectToml}" ] && uv sync
              [ -d "${venvDirectory}" ] && source "${venvDirectory}/bin/activate"
            '';
          };
      in
      {
        devShells = builtins.mapAttrs mkPythonShell pythonPackages;
      }
    );
}
