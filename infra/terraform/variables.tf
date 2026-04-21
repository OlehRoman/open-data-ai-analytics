variable "prefix" {
  description = "Prefix for Azure resources."
  type        = string
  default     = "devops-lab"
}

variable "resource_group_name" {
  description = "Azure Resource Group name."
  type        = string
  default     = "rg-devops-lab"
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "westeurope"
}

variable "vm_size" {
  description = "Azure VM size."
  type        = string
  default     = "Standard_B1s"
}

variable "admin_username" {
  description = "Admin username for the Linux VM."
  type        = string
  default     = "azureuser"
}

variable "admin_ssh_public_key" {
  description = "SSH public key content."
  type        = string
}

variable "repo_url" {
  description = "Git repository URL with the Docker project."
  type        = string
  default     = "https://github.com/OlehRoman/open-data-ai-analytics.git"
}

variable "compose_subdir" {
  description = "Relative path to the directory with docker-compose.yml inside the repo."
  type        = string
  default     = "docker"
}

variable "app_port" {
  description = "Public port of the web interface."
  type        = number
  default     = 8080
}