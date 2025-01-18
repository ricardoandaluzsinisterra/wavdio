import subprocess
import json
from pathlib import Path

def get_latest_version(service):
    version_file = Path("versions.json")
    if version_file.exists():
        with open(version_file) as f:
            versions = json.load(f)
            return versions.get(service, 0)
    return 0

def update_version(service, version):
    version_file = Path("versions.json")
    versions = {}
    if version_file.exists():
        with open(version_file) as f:
            versions = json.load(f)
    versions[service] = version
    with open(version_file, "w") as f:
        json.dump(versions, f)

def docker_build(service_path, service, build_env="dev"):
    current_version = get_latest_version(service) + 1
    hub_repo = f"ricardoandaluz/{service}"
    tag = f"v{current_version}"
    
    build_command = f"docker build --build-arg build_env={build_env} -t {hub_repo}:{tag} {service_path}"
    
    result = subprocess.run(build_command, shell=True, capture_output=True, text=True, errors='replace')
    print(result.stderr)
    
    update_version(service, current_version)
    return f"{hub_repo}:{tag}"

services = ["catalog", "home", "player", "upload", "user"]
build_env = 'prod'

images = {
    service: docker_build(f"./{service}-svc", service, build_env)
    for service in services
}

for service, image in images.items():
    push_command = f"docker push {image}"
    result = subprocess.run(push_command, shell=True, capture_output=True, text=True, errors='replace')
    print(f"Pushing {service}:")
    print(result.stderr)
    print(result.stdout)