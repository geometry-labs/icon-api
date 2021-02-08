# icon-api 

API microservices for the ICON Blockchain. Includes containers to run an event based architecture with websocket, REST, and GraphQl API endpoints for blocks, transactions, and event logs. Includes a REST API to register filtered events and broadcast them to a configurable set of middleware. 


### Requirements 

Minimum
- docker 
- docker-compose 

For development 
- python3
- [tackle-box]() - `pip3 install tackle-box`
- go (Only for certain services)


### Usage 

To run the entire stack, simply run. 
```shell script
docker-compose up -d
```

### Development 

This repo is actually a meta-repo consisting of many sub-repos. To pull all the source code into the project, run:
```shell script
tackle . --context-file repos.yaml
# Follow prompts to pull sub-repos 
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
