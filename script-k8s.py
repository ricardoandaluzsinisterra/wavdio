import subprocess

commands = {
    "start" : "minikube start",
    "stop" : "minkube stop",
    "apply" : "kubectl apply -f ./",
    "delete" : "kubectl delete -f ./",
    "pods" : "kubectl get pods"
}

decision = input("What would you like to do\n")

match decision:
    case "fr":
        subprocess.run(commands["delete"], shell=True, capture_output=True, text=True)
        subprocess.run(commands["stop"], shell=True, capture_output=True, text=True)
        subprocess.run(commands["start"], shell=True, capture_output=True, text=True)
        subprocess.run(commands["apply"], shell=True, capture_output=True, text=True)
        get_pods = subprocess.run(commands["pods"], shell=True, capture_output=True, text=True)
        print(get_pods.stdout)
        print(get_pods.stderr)
    case "r":
        subprocess.run(commands["delete"], shell=True, capture_output=True, text=True)
        subprocess.run(commands["apply"], shell=True, capture_output=True, text=True)
        get_pods = subprocess.run(commands["pods"], shell=True, capture_output=True, text=True)
        print(get_pods.stdout)
        
