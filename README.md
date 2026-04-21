# Azure Lab: Terraform + Cloud Shell + cloud-init

Цей шаблон реалізує лабораторну роботу з повністю хмарним розгортанням Docker-проєкту в Microsoft Azure.

## Що створюється
Terraform створює такі ресурси Azure:

- Resource Group
- Virtual Network
- Subnet
- Public IP
- Network Security Group
- Network Interface
- Linux Virtual Machine

Під час створення VM у неї передається `cloud-init`, який:

- оновлює пакети;
- встановлює Docker;
- встановлює Docker Compose plugin;
- клонує репозиторій з GitHub;
- запускає `docker compose up -d`.

## Структура
```text
project/
├── data_load/
├── data_quality_analysis/
├── data_research/
├── visualization/
├── db/
├── web/
├── docker/
│   ├── docker-compose.yml
│   └── .env
├── infra/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── terraform.tfvars
│       └── cloud-init.yaml.tftpl
├── README.md
└── docs/
```

## Вимоги до Docker-проєкту
У репозиторії мають бути:

- база даних;
- хоча б один модуль обробки;
- веб-інтерфейс;
- файл `docker/docker-compose.yml`.

Веб-інтерфейс має бути проброшений назовні на порт `8080` або інший порт, який ти вкажеш у `terraform.tfvars`.

## Підготовка в Azure Cloud Shell

### 1. Відкрити Azure Portal
Увійди в Azure Portal і запусти **Cloud Shell**.

### 2. Створити файли
Перейди в каталог проєкту та скопіюй туди вміст папки `infra/terraform/`.

### 3. Створити SSH-ключ у Cloud Shell
```bash
ssh-keygen -t ed25519 -f ~/.ssh/azure_lab_key -N ""
cat ~/.ssh/azure_lab_key.pub
```

Скопійований публічний ключ потрібно вставити в `terraform.tfvars`.

### 4. Створити `terraform.tfvars`
Приклад:
```hcl
admin_ssh_public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... user@cloudshell"
repo_url             = "https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git"
compose_subdir       = "docker"
app_port             = 8080
```

## Послідовність команд
```bash
cd infra/terraform
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply -auto-approve
```

## Отримання URL застосунку
Після виконання:
```bash
terraform output app_url
terraform output public_ip
```

## Перевірка
Відкрити в браузері:
```text
http://PUBLIC_IP:PORT
```

Також можна перевірити з Cloud Shell:
```bash
curl $(terraform output -raw app_url)
```

## Додаткова перевірка через SSH
```bash
ssh -i ~/.ssh/azure_lab_key azureuser@$(terraform output -raw public_ip)
```

Корисні команди на VM:
```bash
sudo cloud-init status --wait
cat /var/log/deploy_app.log
docker ps
```

## Видалення ресурсів після демонстрації
```bash
terraform destroy -auto-approve
```

## Що показати на захисті
- Cloud Shell з командами `terraform init`, `plan`, `apply`;
- створену VM в Azure Portal;
- `public_ip` або `app_url` з Terraform output;
- відкриту сторінку веб-інтерфейсу;
- після демонстрації — `terraform destroy`.

## Пояснення архітектури
1. Студент запускає Cloud Shell у браузері.
2. Terraform створює мережу, NSG, NIC, Public IP та Linux VM.
3. Під час першого запуску VM отримує `cloud-init`.
4. `cloud-init` ставить Docker, клонує GitHub-репозиторій і виконує `docker compose up -d`.
5. Веб-інтерфейс стає доступним через `http://PUBLIC_IP:PORT`.