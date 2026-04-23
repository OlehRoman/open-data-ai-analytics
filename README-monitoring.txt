# Monitoring package

Files:
- monitoring/docker-compose.monitoring.yml
- monitoring/prometheus/prometheus.yml
- monitoring/grafana/provisioning/datasources/prometheus.yml
- monitoring/grafana/provisioning/dashboards/dashboard.yml
- monitoring/grafana/dashboards/azure-app-monitoring.json

Run on VM:
cd /opt/app
sudo docker compose -f monitoring/docker-compose.monitoring.yml up -d

URLs:
- Grafana: http://PUBLIC_IP:3000
- Prometheus: http://PUBLIC_IP:9090
- cAdvisor: http://PUBLIC_IP:8080

Grafana login:
- user: admin
- password: admin
