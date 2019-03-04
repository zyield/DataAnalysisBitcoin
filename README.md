# Chainspark ML API

This api labels one or more BTC addresses

## Free API
Send a wallet address or a batch of addresses and the method returns the type of the requested wallet(s) in json format. For example: Cold storage, Main exchange etc.
```
https://bitcoin-wallet-classifier.herokuapp.com/

Usage:
Input:
https://bitcoin-wallet-classifier.herokuapp.com/392LK4ZQD3gixWg5xJRTv1a24N3YDgCbwP,36ZzG7KZ91D8TZhvzxzw79vv8evzP85Fob

Output:
{"Address":{"0":"392LK4ZQD3gixWg5xJRTv1a24N3YDgCbwP","1":"36ZzG7KZ91D8TZhvzxzw79vv8evzP85Fob"},"Label":{"0":"Main Exhange","1":"intermediate address"}}
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


