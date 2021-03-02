# Using ICON API

In this tutorial we will walk through the various elements of deploying and using the icon-api stack. You can run the stack locally or use the provided terraform module to deploy a node on AWS. From there, we will go over how to access the individual enpoints using Websockets, REST, and GraphQL. 

### Pre-Requisites for Tutorial 

- curl 
- ...

For Deploying with Terraform 
- terraform 
- ansible 

### Deploying

The stack can be deployed on your own machine with docker-compose or via Terraform on AWS. It can be run to sync up the backend from any given blockheight which, if you are running from genesis, will require up to 300 GB of disk space.  If running from the current blockheight (icon-etl flag `--start-at-head", "${START_AT_HEAD:-true}` per the docker-compose.yml), then you you will need to allocate about 2 GB per week that you intend on running the node. 

To deploy with Terraform, navigate to [github.com/geometry-labs/terraform-icon-aws-api-ec2](https://github.com/geometry-labs/terraform-icon-aws-api-ec2). From there you can navigate to the examples/defaults and edit parameters based on the README values. Some values like key locations can be persisted in a `terraform.tfvars` per it's [example](https://github.com/geometry-labs/terraform-icon-aws-api-ec2/blob/main/examples/defaults/terraform.tfvars.example).  You will need local ssh keys (ie ssh-keygen) and the deployment will require paths to both the public and private keys. To run the deployment, run `terraform init && terraform apply`.  You will then be asked to fill in the paths to the ssh keys unless you setup the terraform.tfvars file. 

Once the node is deployed, ssh into it and start the application manually just as you would if you were running the stack locally. There is also an option to run with SSL but that is out of scope of this tutorial. 

### Registering events

There are three types of objects you can register to the ICON API:
* Transactions
* Log events
* Broadcasters

#### Transactions

Transactions can be filtered based on the to or from addresses.
To register a new transaction event, make a POST request to the _/transaction/register_ endpoint.
The payload should be in the form of:

```json
{
    "to_address": "cx0000000000000000000000000000000000000000",
    "from_address": "cx0000000000000000000000000000000000000001"
}
```

Individual registrations must be sent separately.
If you want to register multiple related objects, submit them as a broadcaster object.

Filtered transactions will be output directly to the output topic for further consumption.

#### Log Events

Log events are combinations of contract addresses, log output keywords, and log output positions.
To register a new log event, make a POST request to the _/logevent/register_ endpoint.
The payload should be in the form of:

```json
{
    "address": "cx0000000000000000000000000000000000000001",
    "keyword": "LogKeyword",
    "position": 1
}
```

Log events are extracted from the block log and are reformatted and output to the output topic for further consumption.

#### Broadcaster

Broadcasters are sets of associated transaction and log events.
Normally these do not need to be manually registered, as the websocket server will take care of this step.

To register a broadcaster, make a POST request to the _/broadcaster/register_ endpoint.
The payload should be in the form of:

```json
{
    "connection_type": "ws",
    "endpoint": "wss://test",
    "event_ids": [
      "1234-1234-1234"
    ],
    "transaction_events": [
        {
            "to_address": "cx0000000000000000000000000000000000000000",
            "from_address": "cx0000000000000000000000000000000000000001"
        }
    ],
    "log_events": [
        {
            "address": "cx0000000000000000000000000000000000000001",
            "keyword": "LogKeyword",
            "position": 1
        }
    ]
}
```

All associated events, once registered, will output to the output topic and will have the broadcaster_id associated with the message key for output filtering.

### Receiving events
#### Websockets

In order to recieve filtered transactions and log events through a websocket, open a websocket connection on _/ws/admin_.
Once successfully connected, send your filter settings through the same websocket connection.
The payload should ne in the form of:

```json
{
    "connection_type": "ws",
    "endpoint": "wss://test",
    "event_ids": [
      "1234-1234-1234"
    ],
    "transaction_events": [
        {
            "to_address": "cx0000000000000000000000000000000000000000",
            "from_address": "cx0000000000000000000000000000000000000001"
        }
    ],
    "log_events": [
        {
            "address": "cx0000000000000000000000000000000000000001",
            "keyword": "LogKeyword",
            "position": 1
        }
    ]
}
```

If the filter registration was successful, the server will respond on the same websocket with your broadcaster_id.
The websocket will start streaming the filtered transactions and log events.

```json
{
  "broadcaster_id": "2b90ec6e-716f-4cae-a7b6-6800424607da"
}
```

If the filter registration was unsuccessful, the server will respond on the same websocket with an error.

```json
{
  "error": "failed to register"
}
```

```json
{
  "broadcaster_id": "2b90ec6e-716f-4cae-a7b6-6800424607da"
}
```

If the filter registration was unsuccessful, the server will respond on the same websocket with an error.

```json
{
  "error": "failed to register"
}
```

#### Kafka

Filtered events are produced to the output topic (default: _outputs_).
Messages are keyed with the _to_address_ associated with the event, and have any associated _broadcaster_id_ included for filtering.
Messages that are time-sensitive should be consumed directly from the output topic and sent for further processing, as there may be additional delays/connectivity issues associated with websockets.

#### Unregistering Events

Events can be easily unregistered by sending a POST request to the appropriate _/unregister_ endpoint with the same object that was used to register, except now including the associated ID.
Events that were registered by a broadcaster must be removed by modifying the broadcaster event or by unregistering the broadcaster.

### Historical Data

Accessing historical icon blockchain data is made easy through the REST GraphQL APIs.

#### REST API

The REST API can be accessed through curl commands (or any other http client)

```bash
curl -X GET "http://localhost/api/v1/blocks/?skip=0&limit=1" -H  "accept: application/json"
```

> All endpoints that return arrays have a `skip` and `limit` parameter

| Path | Description | Response Type |
|------|-------------|---------------|
| /api/v1/blocks | `GET` latest blocks | array |
| /api/v1/blocks/height/{height} | `GET` block by height | object |
| /api/v1/blocks/hash/{hash} | `GET` block by hash | object |
| /api/v1/tx/hash/{hash} | `GET` transaction by hash | object |
| /api/v1/tx/address/{address} | `GET` transaction by from address | array |
| /api/v1/tx/block | `GET` transactions in the latest blocks | array |
| /api/v1/tx/block/{height} | `GET` transactions by block height | array |
| /api/v1/events/tx/{hash} | `GET` event logs by from_address | array |
| /api/v1/events/block | `GET` event logs in the latest blocks | array |
| /api/v1/events/block/{height} | `GET` event logs by block height | array |

The github repository for the REST API can be found [here](https://github.com/geometry-labs/icon-rest-api).

#### Graphql API

The Graphql API can be accessed through the Graphql Playground located at `/graph/` (or any other graphql client)

Example Graphql query made to `/graph/query`:
```
query Block {
  block(hash: "202d264fb85603ab19f747a60c0cf1aac53b6a15d9567ce7c8bd5e015c023296") {
    hash,
    number,
    transaction_count,
    peer_id
  }
}
```

The github repository for the Graphql API can be found [here](https://github.com/geometry-labs/icon-graphql-api).

##### Schemas

Blocks:
| Field | Type | Parameter |
|------|-------------|---------|
| hash | String | True |
| number | Int | False |
| signature | String | False |
| item_id | String | False |
| transaction_count | Int | False |
| type | String | False |
| version | String | False |
| peer_id | String | False |
| merkle_root_hash | String | False |
| item_timestamp | String | False |
| parent_hash | String | False |
| timestamp | Int | False |

Transactions:
| Field | Type | Filterable |
|------|-------------|---------|
| hash | String | True |
| signature | String | False |
| fee | Int | False |
| block_number | Int | False |
| transaction_index | Int | False |
| type | String | False |
| receipt_step_price | Int | False |
| from_address | String | False |
| value | Int | False |
| timestamp | String | False |
| receipt_status | Int | False |
| item_id | String | False |
| receipt_logs | String | False |
| block_hash | String | False |
| to_address | String | False |
| version | String | False |
| nonce | Int | False |
| receipt_cumulative_step_used | Int | False |
| receipt_score_address | String | False |
| data_type | String | False |
| item_timestamp | String | False |

Logs:
| Field | Type | Filterable |
|------|-------------|---------|
| transaction_hash| String | True |
| address| String | False |
| data| [String] | False |
| indexed| [String] | False |
| item_id| String | False |
| block_timestamp| Int | False |
| block_number| Int | False |
| block_hash| String | False |
| transaction_index| Int | False |
| type| String | False |
| item_timestamp| String | False |

### Websocket Data Streaming

Blockchain data can be streamed via a websocket connection. Just open up a websocket connection to one of three endpoints to start streaming

The github repository for the Websocket API can be found [here](https://github.com/geometry-labs/kafka-websocket-server).

/ws/blocks
```json
{
  "type": "block",
  "number": 31248024,
  "hash": "8abec43285d347c943ef287ab1677338e058b7b6f31eb6039464d94a51a584ed",
  "parent_hash": "7233045d2e84ea1a1694dd9a22ba34508ec1ca6c9fc8569f3c6570794c2ae0dd",
  "merkle_root_hash": "a4484c1a6a3d06a2eaf9abfeaeb8f5e39dba1f8d9ff3ed82790f4a885da5c043",
  "timestamp": 1614666626727336,
  "version": "0.5",
  "transaction_count": 2,
  "peer_id": "hx81719dcfe8f58ca07044b7bede49cecd61f9bd3f",
  "signature": "FHrmre9ijL7H+/N9F/cf4buxZHVgoH7e32iVzvxL7Lc8Ps8NWBiEAjnt2+n+FyHZJ9Ub7b+tZwCU10EHauuFBgE=",
  "next_leader": "hx81719dcfe8f58ca07044b7bede49cecd61f9bd3f",
  "item_id": "block_8abec43285d347c943ef287ab1677338e058b7b6f31eb6039464d94a51a584ed",
  "item_timestamp": "2021-03-02T06:30:26Z"
}
```

/ws/transactions
```json
{
  "type": "transaction",
  "version": "0x3",
  "from_address": null,
  "to_address": null,
  "value": 0,
  "step_limit": null,
  "timestamp": "0x5bc87e2eb1bbf",
  "block_timestamp": 1614666697219007,
  "nid": null,
  "nonce": null,
  "hash": "0xf93fff92e4ed528cf47d54e570e196ac0baf93700ed4ab8d4f270759946304b6",
  "transaction_index": 0,
  "block_hash": "e7d7343a5eb509e8513308ec1c384f054ebb6071292f8af182bf17b03a559b4d",
  "block_number": 31248059,
  "fee": null,
  "signature": null,
  "data_type": "base",
  "data": {
    "prep": {
      "irep": "0x21e19e0c9bab2400000",
      "rrep": "0x181",
      "totalDelegation": "0x1214a2763e44ace3832b64a",
      "value": "0x2a93c85453d83fb3"
    },
    "result": {
      "coveredByFee": "0x0",
      "coveredByOverIssuedICX": "0x0",
      "issue": "0x2a93c85453d83fb3"
    }
  },
  "receipt_cumulative_step_used": 0,
  "receipt_step_used": 0,
  "receipt_step_price": 0,
  "receipt_score_address": null,
  "receipt_logs": null,
  "receipt_status": 1,
  "item_id": "transaction_0xf93fff92e4ed528cf47d54e570e196ac0baf93700ed4ab8d4f270759946304b6",
  "item_timestamp": "2021-03-02T06:31:37Z"
}
```

/ws/logs
```json
{
  "type": "log",
  "log_index": 0,
  "transaction_hash": "0x6426cb215a5125cdeebe80a0922d4fd51b906d543133f6d66f8c7530c83c63c8",
  "transaction_index": 0,
  "address": "cx0000000000000000000000000000000000000000",
  "data": [
    "0x21e19e0c9bab2400000",
    "0x181",
    "0x1214a2763e44ace3832b64a",
    "0x2a93c85453d83fb3"
  ],
  "indexed": [
    "PRepIssued(int,int,int,int)"
  ],
  "block_number": 31248075,
  "block_timestamp": 1614666729418470,
  "block_hash": "2337742853924bbbe6e53210d1186d380ad2db2b71e77108481aa82135762963",
  "item_id": "log_0x6426cb215a5125cdeebe80a0922d4fd51b906d543133f6d66f8c7530c83c63c8_0",
  "item_timestamp": "2021-03-02T06:32:09Z"
}
```

