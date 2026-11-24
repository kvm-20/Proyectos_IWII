output "frontend_url" {
  description = "Abra esta direccion en el navegador"
  value       = "http://localhost:${var.frontend_port}"
}

output "backend_health_url" {
  value = "http://localhost:${var.backend_port}/health"
}
