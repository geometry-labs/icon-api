<p align="center">
  <h3 align="center">ICON API</h3>

  <p align="center">
    API microservice stack for the ICON Blockchain.
    <br />
</p>

Includes containers to run an event based architecture on Kafka with websockets, REST, and GraphQl API endpoints for blocks, transactions, and event logs.
Includes a REST API to register filtered events and broadcast them to a configurable set of middleware similar to [eventeum](https://github.com/eventeum/eventeum). 

The stack is modular and can be adopted in whole or in part by disabling various services in the stack.
Each process relies on [icon-etl](https://github.com/blockchain-etl/icon-etl) to stream data into Kafka from which APIs are built on top of.
For historical queries, data is moved by means of Kafka Connect into MongoDB from which REST and GraphQL endpoints are exposed.
For websockets, data is streamed directly from kafka. 
The services are packaged with docker-compose with a [Traefik](https://doc.traefik.io/traefik/) reverse proxy.  

<!---
### Endpoints 
| Name | Endpoint Prefix |  Docs | 
| :--- | :--- | :--- |  
| REST API | /api/v1/ | /api/v1/docs | 
--->

### Containers

| Name | Description |
| :--- | :---------- |
| [etl](https://github.com/geometry-labs/icon-etl) | Icon etl to scan the blockchain and pipe data to kafka brokers |
| [registration](https://github.com/geometry-labs/icon-filter-registration) | Rest api to register contracts and transactions to track |
| [filter-worker-contract](https://github.com/geometry-labs/icon-kafka-worker) | Filter worker for contracts |
| [filter-worker-transaction](https://github.com/geometry-labs/icon-kafka-worker) | Filter worker for transactions | 
| [rest-api](https://github.com/geometry-labs/icon-rest-api) | Rest api to retrieve historical icon blockchain data |
| [kafka-websocket-server](https://github.com/geometry-labs/kafka-websocket-server) | Websocket server to stream live data for blocks, transactions, and contract logs |
| [kafka-topic-init](https://github.com/geometry-labs/kafka-topics-init) | Kafka topic initialization container, exit 0 after completion |
| [kafka-connect-init](https://github.com/geometry-labs/kafka-connect-init) | Kafka contract initialization container, exit 0 after completion |


### Requirements 

Minimum:
- docker 
- docker-compose 

For development :
- python3
- [tackle-box](https://github.com/geometry-labs/tackle-box) - `pip3 install tackle-box`
- Go (Only for certain services)

### Usage 

To run the entire stack, simply run. 
```shell script
docker-compose up -d
```

### Development 

This repo is actually a meta-repo consisting of many sub-repos. To pull all the source code into the project, run:
```shell script
pip3 install tackle-box 
tackle . --context-file repos.yaml --no-input 
```

To run the development version, run the docker-compose with the `docker-compose.dev.yml` to override the images with local builds of the containers like so. 

```shell script
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d 
```

Each service has unit tests embedded into their build pipelines with integration tests run from this repo in the `tests` directory. To run integration tests, run the stack and then run the tests separately. 

```shell script
pip install -r requirements_dev.txt 
python -m pytest tests
```
