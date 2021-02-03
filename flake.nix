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
          buildInputs = [ pkgs.poetry ];
        };

        defaultPackage = pythonEnv;

        checks = {
          build = self.defaultPackage."${system}";

          black = pkgs.runCommand "black"
            {
              buildInputs = [ pkgs.black ];
            }
            ''
              mkdir $out
              black --check ${self}
            '';

          mypy = pkgs.runCommand "mypy"
            {
              buildInputs = [ pkgs.mypy ];
            }
            ''
              mkdir $out
              mypy ${self}/wmo
            '';

          flake8 = pkgs.runCommand "flake8"
            {
              buildInputs = [ pkgs.python3Packages.flake8 ];
            }
            ''
              mkdir $out
              flake8 ${self}/wmo
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
