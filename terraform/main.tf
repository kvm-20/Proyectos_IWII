# ============================================================
# Infraestructura como codigo (IaC) de BiblioWeb con Terraform.
# Usa el proveedor de Docker para crear la red, el volumen y los
# contenedores (MySQL, backend y frontend) de forma declarativa.
# ============================================================

terraform {
  required_version = ">= 1.5"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = var.docker_host
}

# ---------- Red y almacenamiento ----------
resource "docker_network" "biblioweb" {
  name = "biblioweb-tf-net"
}

resource "docker_volume" "mysql_data" {
  name = "biblioweb-tf-mysql-data"
}

# ---------- Imagenes ----------
resource "docker_image" "mysql" {
  name         = "mysql:8.4"
  keep_locally = true
}

# Imagenes propias: se construyen antes con "docker compose build"
resource "docker_image" "backend" {
  name         = var.backend_image
  keep_locally = true
}

resource "docker_image" "frontend" {
  name         = var.frontend_image
  keep_locally = true
}

# ---------- Contenedores ----------
resource "docker_container" "mysql" {
  name    = "biblioweb-tf-mysql"
  image   = docker_image.mysql.image_id
  restart = "unless-stopped"
  command = ["--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]

  env = [
    "MYSQL_DATABASE=${var.mysql_database}",
    "MYSQL_USER=${var.mysql_user}",
    "MYSQL_PASSWORD=${var.mysql_password}",
    "MYSQL_ROOT_PASSWORD=${var.mysql_root_password}",
  ]

  networks_advanced {
    name    = docker_network.biblioweb.name
    aliases = ["db"]
  }

  volumes {
    volume_name    = docker_volume.mysql_data.name
    container_path = "/var/lib/mysql"
  }
}

resource "docker_container" "backend" {
  name    = "biblioweb-tf-backend"
  image   = docker_image.backend.image_id
  restart = "unless-stopped"

  env = [
    "DATABASE_URL=mysql+pymysql://${var.mysql_user}:${var.mysql_password}@db:3306/${var.mysql_database}?charset=utf8mb4",
    "JWT_SECRET_KEY=${var.jwt_secret_key}",
    "SECRET_KEY=${var.secret_key}",
    "CORS_ORIGINS=http://localhost:${var.frontend_port}",
  ]

  networks_advanced {
    name    = docker_network.biblioweb.name
    aliases = ["backend"]
  }

  ports {
    internal = 5000
    external = var.backend_port
  }

  depends_on = [docker_container.mysql]
}

resource "docker_container" "frontend" {
  name    = "biblioweb-tf-frontend"
  image   = docker_image.frontend.image_id
  restart = "unless-stopped"

  networks_advanced {
    name = docker_network.biblioweb.name
  }

  ports {
    internal = 80
    external = var.frontend_port
  }

  depends_on = [docker_container.backend]
}
