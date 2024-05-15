import subprocess

def docker_build(service_path, repo, service):
    global hub_repo
    hub_repo = f"ricardoandaluz/{repo}"

    build_command = f"docker build -t {hub_repo}:{service} {service_path}"

    # Use subprocess.run instead of os.system to capture the output
    result = subprocess.run(build_command, shell=True, capture_output=True, text=True)

    print(result.stderr)
    
repo = 'wavdio'   
# Use the function
docker_build("./catalog-svc", repo, "catalog")
docker_build("./home-svc", repo, "home" )
docker_build("./player-svc", repo, "player")
docker_build("./upload-svc", repo, "upload")
docker_build("./user-svc", repo, "user")

pushes = {
"catalog_push" : f"docker push {hub_repo}:catalog",
"home_push" : f"docker push {hub_repo}:home",
"upload_push" : f"docker push {hub_repo}:upload",
"player_push" : f"docker push {hub_repo}:player",
"user_push" : f"docker push {hub_repo}:user",
}

for push in pushes:
    result = subprocess.run(pushes[push], shell=True, capture_output=True, text=True)
    print(result.stderr)