let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.python-dotenv
    ]))
    pkgs.bitwarden-cli
    pkgs.pipreqs
  ];
}
