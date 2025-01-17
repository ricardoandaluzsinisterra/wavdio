# k8s-manifests/README.md

# Kubernetes Manifests

This project contains Kubernetes manifests for deploying various services and databases in a containerized environment. The manifests are organized into different directories based on their types, including deployments, stateful sets, config maps, secrets, volumes, and services.

## Directory Structure

- **deployments/**: Contains deployment manifests for each service.
  - `home-svc.yaml`: Deployment for the home service.
  - `user-svc.yaml`: Deployment for the user service.
  - `upload-svc.yaml`: Deployment for the upload service.
  - `player-svc.yaml`: Deployment for the player service.
  - `catalog-svc.yaml`: Deployment for the catalog service.
  - `nginx.yaml`: Deployment for the Nginx service.

- **statefulsets/**: Contains stateful set manifests for databases.
  - `users-db.yaml`: Stateful set for the users database.
  - `songs-db.yaml`: Stateful set for the songs database.
  - `kafka.yaml`: Stateful set for Kafka.
  - `zookeeper.yaml`: Stateful set for Zookeeper.

- **configmaps/**: Contains configuration maps for services.
  - `nginx-config.yaml`: ConfigMap for Nginx configuration.

- **secrets/**: Contains secrets for sensitive information.
  - `nginx-certs.yaml`: Secret for storing Nginx certificates.

- **volumes/**: Contains persistent volume definitions.
  - `audio-storage-pv.yaml`: PersistentVolume for audio storage.
  - `kafka-pv.yaml`: PersistentVolume for Kafka storage.
  - `zookeeper-pv.yaml`: PersistentVolume for Zookeeper storage.

- **services/**: Contains service manifests for each service.
  - `home-svc.yaml`: Service for the home service.
  - `user-svc.yaml`: Service for the user service.
  - `upload-svc.yaml`: Service for the upload service.
  - `player-svc.yaml`: Service for the player service.
  - `catalog-svc.yaml`: Service for the catalog service.
  - `nginx.yaml`: Service for Nginx.
  - `users-db.yaml`: Service for the users database.
  - `songs-db.yaml`: Service for the songs database.
  - `kafka.yaml`: Service for Kafka.
  - `zookeeper.yaml`: Service for Zookeeper.

## Usage

To apply the manifests, use the following command:

```bash
kubectl apply -f <manifest-file>
```

Replace `<manifest-file>` with the path to the desired manifest file.

Ensure that your Kubernetes cluster is up and running before applying the manifests.