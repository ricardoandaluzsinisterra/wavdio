# Filepath: setup-commands.ps1

# Define the commands to run
$commands = @(
    "kind create cluster --name wavdio --config cluster-config.yml"
    "helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard",
    "helm repo update",
    "helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard",
    "kubectl apply -f dashboard-service-account.yml",
    "kubectl apply -f role-binding.yml",
    "kubectl -n kubernetes-dashboard create token admin-user --duration 240h",
    "kubectl create -f https://download.elastic.co/downloads/eck/2.13.0/crds.yaml",
    "kubectl apply -f https://download.elastic.co/downloads/eck/2.13.0/operator.yaml",
    "kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml",
    "kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/vertical-pod-autoscaler/deploy/vpa-v1-crd-gen.yaml",
    "kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/vertical-pod-autoscaler/deploy/vpa-rbac.yaml",
    "kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/vertical-pod-autoscaler/deploy/recommender-deployment.yaml",
    "kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/vertical-pod-autoscaler/deploy/updater-deployment.yaml",
    "kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/vertical-pod-autoscaler/deploy/admission-controller-deployment.yaml",
    "kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml",
    "kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/main/config/manifests/metallb-native.yaml",
    "kubectl apply -k ./base/"
)

# Execute each command with a 3-second delay
foreach ($command in $commands) {
    Write-Host "Executing: $command"
    Invoke-Expression $command
    Start-Sleep -Seconds 25
}

Write-Host "All commands executed successfully."
