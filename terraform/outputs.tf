output "bucket_name" {
  description = "Nom du bucket créé"
  value       = google_storage_bucket.raw_meteo_data.name
}

output "bigquery_raw_dataset_id" {
  description = "ID du dataset brut"
  value       = google_bigquery_dataset.raw_dataset.dataset_id
}

output "service_account_email" {
  description = "Email du compte de service à utiliser dans le script Python"
  value       = google_service_account.ingestion_sa.email
}