{ pkgs, config, ... }:

{

  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.microserver
    pkgs.nodejs
    pkgs.nodePackages.tailwindcss
    pkgs.nodePackages.pnpm
    pkgs.php82
    pkgs.wp-cli
    pkgs.wordpress
  ];

  languages = {
    javascript = {
      enable = true;
      package = pkgs.nodejs;
    };
    php = {
      enable = true;
      fpm.pools.web = {
        settings = {
          "clear_env" = "no";
          "pm" = "dynamic";
          "pm.max_children" = 10;
          "pm.start_servers" = 2;
          "pm.min_spare_servers" = 1;
          "pm.max_spare_servers" = 3;
        };
        phpOptions = ''
          upload_max_filesize = 32M
          post_max_size = 64M
          memory_limit = 128M
        '';
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
        root * public
        php_fastcgi unix/${config.languages.php.fpm.pools.web.socket} 
        file_server
      '';
    };
  };

  services.mysql = {
    enable = true;
    initialDatabases = [{ name = "studio"; }];
    ensureUsers = [{
      name = "studio";
      password = "studio";
      ensurePermissions = { "studio.*" = "ALL PRIVILEGES"; };
    }];
  };

  env.DB_NAME = "studio";
  env.DB_USER = "studio";
  env.DB_PASSWORD = "studio";


}
