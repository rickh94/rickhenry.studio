{ pkgs, ... }:

{

  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.microserver
    pkgs.nodejs
    pkgs.nodePackages.tailwindcss
    pkgs.nodePackages.pnpm
  ];

  languages = {
    javascript = {
      enable = true;
    };
  };


  scripts.view.exec = "microserver --no-spa design";
}
