{ pkgs, ... }: {
  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.microserver
    pkgs.nodejs
    pkgs.nodePackages.tailwindcss
    pkgs.nodePackages.pnpm
    pkgs.litestream
    pkgs.python311
    pkgs.poetry
    pkgs.litefs
    pkgs.rustywind
  ];

  languages = {
    javascript = {
      enable = true;
    };
    python = {
      package = pkgs.python311;
      enable = true;
      poetry = {
        enable = true;
        activate.enable = true;
        install.enable = true;
        install.allExtras = true;
      };
    };
  };

  certificates = [
    "studio.localhost"
  ];

  services.caddy = {
    enable = true;
    virtualHosts."studio.localhost" = {
      extraConfig = ''
        reverse_proxy :8000
      '';
    };
  };

  scripts.tw.exec = "bun x tailwindcss -i ./static-src/main.css -o ./static/main.css --watch";
  scripts.automigrate.exec = "python studioblog/manage.py makemigrations && python studioblog/manage.py migrate";

  processes = {
    litestream.exec = "${pkgs.litestream}/bin/litestream replicate -config ${./litestream.dev.yml}";
    dev.exec = "cd studioblog && ${pkgs.poetry}/bin/poetry run python manage.py runserver 0.0.0.0:8000";
  };

  scripts.view.exec = "microserver --no-spa design";
}
