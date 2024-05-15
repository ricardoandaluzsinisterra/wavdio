import subprocess

def docker_build(service_path, repo, service, build_env="dev"):
    global hub_repo
    hub_repo = f"ricardoandaluz/{repo}"

    build_command = f"docker build --build-arg build_env={build_env} -t {hub_repo}:{service} {service_path}"

    result = subprocess.run(build_command, shell=True, capture_output=True, text=True)

    print(result.stderr)

repo = 'wavdio'   
build_env = 'prod'  # or 'dev' depending on your needs

docker_build("./catalog-svc", repo, "catalog", build_env)
docker_build("./home-svc", repo, "home", build_env)
docker_build("./player-svc", repo, "player", build_env)
docker_build("./upload-svc", repo, "upload", build_env)
docker_build("./user-svc", repo, "user", build_env)

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
    print(result.stdout)