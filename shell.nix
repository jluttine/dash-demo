let
  pkgs = import <nixpkgs> {};
in (
  pkgs.python3.withPackages (
    ps: with ps; [
      dash
      pandas
    ]
  )
).env
