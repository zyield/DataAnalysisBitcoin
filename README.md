# Chainspark ML API

This api labels one or more BTC addresses

## Free API
```
https://bitcoin-wallet-classifier.herokuapp.com/
```

## Building the Docker container 

```
docker build -t chainspark_ml .
```

This command builds a container called chainspark_ml according to the Dockerfile

## Running the container locally

```
docker run -d -p 5000:5000 chainspark_ml
```

This runs a detached container exposing port 5000. You can access the api at http://0.0.0.0:5000

To stop the container:

```
docker ps
```

```
docker stop <CONTAINER_ID>
```


