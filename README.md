# Open Data AI Analytics in Azure

## 1. Розгортання в Azure

### Підготовка
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
ssh-keygen -t rsa -b 4096 -f ~/.ssh/azure_lab_rsa -N ""
cat ~/.ssh/azure_lab_rsa.pub
```

### `infra/terraform/terraform.tfvars`
```hcl
admin_ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQ..."
repo_url             = "https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git"
compose_subdir       = "."
app_port             = 5000
location             = "francecentral"
vm_size              = "Standard_A1_v2"
```

### Terraform
```bash
cd infra/terraform
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply -auto-approve
terraform output public_ip
terraform output app_url
```

### Перевірка
```bash
curl $(terraform output -raw app_url)
```

### SSH до VM
```bash
ssh -i ~/.ssh/azure_lab_rsa azureuser@$(terraform output -raw public_ip)
```

### Корисні команди на VM
```bash
sudo cloud-init status --wait
cat /var/log/deploy_app.log
sudo docker ps
```

---

## 2. Моніторинг

### Запуск monitoring
```bash
cd /opt/app/monitoring
sudo docker compose -f docker-compose.monitoring.yml up -d
sudo docker ps
```

### URL
- Grafana: `http://PUBLIC_IP:3000`
- Prometheus: `http://PUBLIC_IP:9090`
- cAdvisor: `http://PUBLIC_IP:8080`

### Grafana
- login: `admin`
- password: `admin`

---

## 3. GitOps

### Встановлення k3s
```bash
curl -sfL https://get.k3s.io | sh -
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
export KUBECONFIG=~/.kube/config
kubectl get nodes
```

### Встановлення Argo CD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get pods -n argocd
```

### Пароль Argo CD
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```

### Port-forward
```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443 --address 0.0.0.0
```

### Argo CD URL
- `https://PUBLIC_IP:8081`
- login: `admin`

### Підключення Application
```bash
cd /opt/app
kubectl apply -f gitops/argocd/application.yaml
kubectl get applications -n argocd
kubectl get pods -n app-gitops
kubectl get svc -n app-gitops
```

### URL GitOps-застосунку
- `http://PUBLIC_IP:30080`

---

## 4. Auto update

Змінити в `gitops/app/deployment.yaml`:
```yaml
replicas: 1
```
на
```yaml
replicas: 2
```

Потім:
```bash
git add gitops/app/deployment.yaml
git commit -m "Scale web-app from 1 to 2 replicas"
git push
kubectl get pods -n app-gitops
```

---

## 5. Rollback

```bash
git revert HEAD
git push
kubectl get pods -n app-gitops
```

---

## 6. Що показати

### Azure
```bash
terraform output public_ip
terraform output app_url
```

### Kubernetes
```bash
kubectl get nodes
kubectl get pods -n argocd
kubectl get applications -n argocd
kubectl get pods -n app-gitops
kubectl get svc -n app-gitops
```

### Моніторинг
- Prometheus Targets
- Grafana Dashboard

### GitOps
- Argo CD UI
- застосунок на `30080`
- commit з оновленням
- rollback

---

## 7. Завершення

### Вийти з VM
```bash
exit
```

### Видалити Azure-ресурси
```bash
cd ~/YOUR_REPOSITORY/infra/terraform
terraform destroy -auto-approve
terraform state list
```
