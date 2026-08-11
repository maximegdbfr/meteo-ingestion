variable "project_id" {
  description = "L'ID de ton projet Google Cloud"
  type        = string
}

variable "region" {
  description = "La région où déployer les ressources"
  type        = string
  default     = "europe-west1" # Belgique (proche et moins cher)
}

variable "bucket_name" {
  description = "Le nom du bucket Cloud Storage (attention, il doit être unique au monde)"
  type        = string
}