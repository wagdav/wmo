{
  description = "Website Monitor";

  inputs.utils.url = "github:numtide/flake-utils";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.09";

  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem
    (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = (pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
        });

      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.poetry
            pkgs.postgresql
          ];
        };

        apps = {
          check = {
            type = "app";
            program = "${self.defaultPackage."${system}"}/bin/check";
          };

          write = {
            type = "app";
            program = "${self.defaultPackage."${system}"}/bin/write";
          };
        };

        defaultPackage = (pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;

          propagatedBuildInputs = [ pkgs.postgresql ];

          checkPhase = "python -m unittest discover";
        });

        checks = {
          build = self.defaultPackage."${system}";

          black = pkgs.runCommand "black"
            {
              buildInputs = [ pythonEnv ];
            }
            ''
              mkdir $out
              black --check ${self}
            '';

          mypy = pkgs.runCommand "mypy"
            {
              buildInputs = [ pythonEnv ];
            }
            ''
              mkdir $out
              mypy ${self}/wmo
            '';

          flake8 = pkgs.runCommand "flake8"
            {
              buildInputs = [ pythonEnv ];
            }
            ''
              mkdir $out
              flake8 --config ${self}/setup.cfg ${self}
            '';

          isort = pkgs.runCommand "isort"
            {
              buildInputs = [ pythonEnv ];
            }
            ''
              mkdir $out
              cd ${self} && isort --check wmo tests
            '';

          yamllint = pkgs.runCommand "yamllint"
            {
              buildInputs = with pkgs; [ yamllint ];
            }
            ''
              mkdir $out
              yamllint --strict ${./.github/workflows}
            '';

          markdownlint = pkgs.runCommand "mdl"
            {
              buildInputs = [ pkgs.mdl ];
            }
            ''
              mkdir $out
              mdl ${./README.md}
            '';
        };
      }
    );
}
