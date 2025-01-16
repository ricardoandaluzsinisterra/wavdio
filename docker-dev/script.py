import subprocess

def docker_build(service_path, repo, service, build_env="dev"):
    hub_repo = f"ricardoandaluz/{repo}"  # Remove global, make it local
    build_command = f"docker build --build-arg build_env={build_env} -t {hub_repo}:{service} {service_path}"
    
    result = subprocess.run(build_command, shell=True, capture_output=True, text=True)
    print(result.stderr)
    
    # Return the full image name for pushing later
    return f"{hub_repo}:{service}"

# Define repos for each service
repos = {
    "catalog": "repo1",
    "home": "repo2",
    "player": "repo3",
    "upload": "repo4",
    "user": "repo5"
}

build_env = 'prod'  # or 'dev' depending on your needs

# Build and collect image names
images = {
    "catalog": docker_build("./catalog-svc", repos["catalog"], "catalog", build_env),
    "home": docker_build("./home-svc", repos["home"], "home", build_env),
    "player": docker_build("./player-svc", repos["player"], "player", build_env),
    "upload": docker_build("./upload-svc", repos["upload"], "upload", build_env),
    "user": docker_build("./user-svc", repos["user"], "user", build_env)
}

# Push each image
for service, image in images.items():
    push_command = f"docker push {image}"
    result = subprocess.run(push_command, shell=True, capture_output=True, text=True)
    print(f"Pushing {service}:")
    print(result.stderr)
    print(result.stdout)