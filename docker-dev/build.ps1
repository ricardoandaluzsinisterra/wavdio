

# Tear down the existing Docker containers
docker-compose down

# Build a new image without using cache
docker-compose build --no-cache

# Start the containers
docker-compose up -d