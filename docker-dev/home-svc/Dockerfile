# Build variable with default of 'dev'
ARG build_env="dev"
# This image is the common base image - called base (using AS keyword)
FROM python:3.12.1-alpine3.18 AS base
WORKDIR /root
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# The dev image uses base image (above) and does nothing else.
# The resulting image is called 'branch-dev'
FROM base AS branch-dev

# This builds using the 'base' and copies the app files.
# The resulting image is called 'branch-prod'
FROM base AS branch-prod
COPY ./ /root/app/
WORKDIR /root/app
CMD ["python", "home-app.py"]

# The final image is built from either branch-dev or branch-prod, depending on value of build_env
FROM branch-$build_env AS final