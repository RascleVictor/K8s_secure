# K8s_secure - Cluster Kubernetes Sécurisé

## Objectif

Ce projet vise à déployer un **cluster Kubernetes sécurisé** (hardening) avec les meilleures pratiques DevSecOps.  
L'objectif est de montrer comment sécuriser un cluster et ses workloads avec plusieurs outils et politiques de sécurité.

---

## Composants de sécurité inclus

1. **Network Policies**  
   Limitation des communications entre pods pour réduire la surface d'attaque.

2. **RBAC strict**  
   Permissions minimales pour les utilisateurs et service accounts.

3. **Pod Security Standards / Policies**  
   Restriction sur les conteneurs privilégiés, root, hostPath, etc.

4. **Liveness & Readiness Probes**  
   Assurer la résilience et la santé des applications.

5. **OPA Gatekeeper**  
   Enforcement de policies Kubernetes via ConstraintTemplates et Constraints.

6. **Kyverno**  
   Gestion de policies de sécurité, validations et mutations de ressources Kubernetes.

7. **Trivy Operator**  
   Analyse des images et des workloads pour détecter les vulnérabilités.

8. **Falco**  
   Détection d’intrusions et comportement suspect au niveau des pods/nœuds.

9. **CI/CD**  
   Déploiement automatisé dans le cluster avec pipelines sécurisés.

---

## Architecture du projet

```text
kubernetes/
  apps/
    app-web/
    app-vulnerable/
  security/
    gatekeeper/
      templates/
      constraints/
    kyverno/
    pod-security/
    trivy/
    falco/
docker/
  app-web/
    Dockerfile
  app-vulnerable/


# Créer un cluster Kind sécurisé
kind create cluster --name secure-cluster --config kind-config.yaml

# Vérifier le cluster
kubectl cluster-info
kubectl get nodes -o wide

kubectl apply -f kubernetes/namespaces/
kubectl apply -f kubernetes/apps/
kubectl get pods -A

kubectl apply -f https://openpolicyagent.org/install/gatekeeper/latest.yaml
kubectl get pods -n gatekeeper-system

kubectl apply -f kubernetes/security/gatekeeper/templates/
kubectl apply -f kubernetes/security/gatekeeper/constraints/
kubectl get allowedregistries

# Supprimer les anciennes installations si nécessaire
kubectl delete namespace kyverno || true
kubectl create namespace kyverno

# Ajouter le repo Helm de Kyverno
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

# Installer Kyverno
helm install kyverno kyverno/kyverno --namespace kyverno --create-namespace

# Vérifier les pods Kyverno
kubectl get pods -n kyverno -w

# Appliquer des policies d’exception si nécessaire
kubectl apply -f kubernetes/security/kyverno/kyverno-policy-exception.yaml

kubectl apply -f https://raw.githubusercontent.com/aquasecurity/trivy-operator/v0.15.0/deploy/static/trivy-operator.yaml
kubectl get pods -n trivy-system -w

kubectl apply -f kubernetes/security/falco/falco-policy-exception.yml
kubectl apply -f kubernetes/security/falco/manifests/falco-daemonset.yml
kubectl get pods -n falco -w
