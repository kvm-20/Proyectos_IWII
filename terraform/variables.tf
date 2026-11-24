variable "docker_host" {
  description = "Conexion al motor de Docker. Windows: npipe:////./pipe/docker_engine | Linux/Mac: unix:///var/run/docker.sock"
  type        = string
  default     = "npipe:////./pipe/docker_engine"
}

variable "backend_image" {
  type    = string
  default = "biblioweb-backend:1.0"
}

variable "frontend_image" {
  type    = string
  default = "biblioweb-frontend:1.0"
}

variable "backend_port" {
  type    = number
  default = 5001
}

variable "frontend_port" {
  type    = number
  default = 8081
}

variable "mysql_database" {
  type    = string
  default = "biblioweb"
}

variable "mysql_user" {
  type    = string
  default = "biblioweb"
}

# Variables sensibles: se definen en terraform.tfvars (que NO se sube a GitHub)
variable "mysql_password" {
  type      = string
  sensitive = true
}

variable "mysql_root_password" {
  type      = string
  sensitive = true
}

variable "jwt_secret_key" {
  type      = string
  sensitive = true
}

variable "secret_key" {
  type      = string
  sensitive = true
}
