# stroke-prediction-webapp

## ...

## ...

## Docker Integration
Navigate to the directory where the Dockerfile is located and run the commands in the following order.

1. Build image from Dockerfile.
    > docker build -t stroke-prediction-webapp .
2. Starts a container with the previously built image. With port mapping from 5000 to 8080.
    > docker run -d -p 8080:5000 stroke-prediction-webapp