{
  description = "Website Monitor";

  inputs.utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem
    (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = (pkgs.poetry2nix.mkPoetryEnv {
          projectDir = self;
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

        defaultPackage = (pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;

          propagatedBuildInputs = [ pkgs.postgresql ];
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
              #isort --check ${self}
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
