# Terraform basics

1. Create Service Account

   1. IAM & Admin -> service accounts
   2. service account name
   3. description (optional)
   4. create and continue
   5. Grant this service account access to project (optional)
      1. select a role -> Cloud Storage -> storage admin
      2. select 2nd role -> BigQuery -> BigQuery admin
      3. continue
   6. IAM -> service account -> add another role -> Compute Engine -> Compute admin
   7. Service Accounts -> click -> manage keys ->add key -> create new key -> json
   8. VM -> create a dir -> cd to dir -> create dir named keys -> create a json file inside the keys dir -> paste the key

2. Create main TF file

   1. open vs code in VM -> install terraform extension

   2. create main.tf file in same dir with keys folder

   3. copy the configuration from terraform google provider website

   4. paste to main.tf file and edit

   5. use command `terraform fmt` to correct the format 

      ```tf
      terraform {
      	required_providers {
      		google {
                  source = "hashicorp/google"
                  version = "5.6.0"
              }
      	}
      }
      
      provider "google" {
      	project = "my-project-id"
      	region = "us-central1"
      }
      ```

   6. Cloud overview -> dashboard -> copy project-id

   7. export google credentials

      ```bash
      export GOOGLE_CREDENTIALS='/home/path_to_creds.json'
      ```

   8. terraform init

      ```bash
      terraform init
      ```

   9. Cloud storage -> buckets 

   10. search terraform google cloud storage bucket -> copy example usage -> paste to tf file

       ```tf
       resource "google_storage_bucket" "demo-bucket" {
       	name = "demo-bucket"
       	location = "US"
       	force_destroy = true
       	
       	lifecycle_rule {
       		condition {
       			age = 3
       		}
       		action {
       			type = "AbortIncompleteMultipartUpload"
       		}
       	}
       }
       ```

   11. terraform plan

       ```bash
       terraform plan
       ```

   12. Deploy

       ```bash
       terraform apply
       yes
       ```

   13. verify the bucket on GCP

   14. destroy

       ```bash
       terraform destroy
       confirm
       ```

   15. Use terraform git ignore all json files when pushing to github

       1. search terraform git ignore -> copy -> create .gitignore file -> paste -> add *.json 

# Terraform Variables

Creating a big query dataset

1. Search Terraform BigQuery dataset -> find required and find all required-> copy example basic dataset -> dataset_id

   ```tf
   reource "google_bigquery_dataset" "demo_dataset"{
   	dataset_id = "example_dataset"
   }
   ```

   ```bash
   terraform fmt
   terraform apply
   terraform destroy
   yes
   ```

## Using Variable

1. Create a file named `variables.tf`

   ```tf
   variable "project" {
   	description = "Project"
   	default = "terraform-demo"
   }
   
   variable "location" {
   	description = "Project Location"
   	default = "US"
   }
   
   variable "region" {
   	description = "Region"
   	default = "us-central1"
   }
   
   variable "bq_dataset_name" {
   	description = "My BigQuery Dataset Name"
   	default = "demo_dataset"
   }
   
   variable "gcs_bucket_name" {
   	description = "My Storage Bucket Name
   	default = "terraform_demo_name"
   }
   
   variable "gcs_storage_class" {
   	description = "Bucket Storage Class"
   	default = "STANDARD"
   }
   ```

2. Update the `main.tf` file with the variables created

   ```tf
   terraform {
   	required_providers {
   		google {
               source = "hashicorp/google"
               version = "5.6.0"
           }
   	}
   }
   
   provider "google" {
   	project = var.project
   	region = var.region
   }
   
   resource "google_storage_bucket" "demo-bucket" {
   	name = var.gcs_bucket_name
   	location = var.location
   	force_destroy = true
   	
   	lifecycle_rule {
   		condition {
   			age = 3
   		}
   		action {
   			type = "AbortIncompleteMultipartUpload"
   		}
   	}
   }
   
   reource "google_bigquery_dataset" "demo_dataset"{
   	dataset_id = var.bq_dataset_name
   	location = var.location
   }
   ```

3. show plan

   ```bash
   terraform plan
   ```

4. apply

   ```bash
   terraform apply
   ```

5. Unset

   ```bash
   terraform destroy
   unset GOOGLE_CREDENTIALS
   echo GOOGLE_CREDENTIALS
   terraform plan
   ```

6. Using Function file

   1. add variable credentials

   ```tf
   variable "credentials" {
   	description = "My credentials"
   	default = "./keys/my-creds.json"
   }
   ```

   2. update main tf file

   ```tf
   provider "google" {
   	credentials = file(var.credentials)
   	project = var.project
   	region = var.region
   }
   ```

   3. apply
   
      ```bash
      terraform fmt
      terraform apply
      ```
   
   4. Destroy when finished