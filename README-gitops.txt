# GitOps package

Files:
- gitops/app/namespace.yaml
- gitops/app/deployment.yaml
- gitops/app/service.yaml
- gitops/argocd/application.yaml

What to change:
1. In gitops/app/deployment.yaml replace
   ghcr.io/YOUR_USERNAME/open-data-ai-analytics-web:latest
   with your real Docker image.

2. In gitops/argocd/application.yaml replace
   https://github.com/YOUR_USERNAME/open-data-ai-analytics.git
   with your real GitHub repository URL.

Expected app URL after deploy:
http://PUBLIC_IP:30080
