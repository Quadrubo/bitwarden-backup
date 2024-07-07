let
  pkgs = import <nixpkgs> { };

  bitwarden-cli = pkgs.bitwarden-cli.overrideAttrs (oldAttrs: rec {
    inherit (oldAttrs) pname;
    version = "2024.6.0";

    src = pkgs.fetchFromGitHub {
      owner = "bitwarden";
      repo = "clients";
      rev = "cli-v${version}";
      hash = "sha256-qiUUrs23WHE3+KFsWDknuDSA6M3Zwjz9Jdjq6mn5XkE=";
    };

    npmDeps = pkgs.fetchNpmDeps {
      inherit src;
      name = "${pname}-${version}-npm-deps";
      hash = "sha256-Mgd15eFJtWoBqFFCsjmsnlNbcg5NDs1U7DlMkE0hIb8=";
    };
  });
in
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.python-dotenv
    ]))
    # overwrite the package version to use the old version
    bitwarden-cli
    pkgs.pipreqs
  ];
}
