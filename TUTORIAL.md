# Using ICON API

In this tutorial we will walk through the various elements of deploying and using the icon-api stack. You can run the stack locally or use the provided terraform module to deploy a node on AWS. From there, we will go over how to access the individual enpoints using Websockets, REST, and GraphQL. 

### Overview of ICON API 

TODO

### Pre-Requisites for Tutorial 

- curl 
- ...

For Deploying with Terraform 
- terraform 
- ansible 

### Deploying

The stack can be deployed on your own machine with docker-compose or via Terraform. To deploy with Terraform, navigate to [github.com/geometry-labs/terraform-icon-aws-api-ec2](https://github.com/geometry-labs/terraform-icon-aws-api-ec2). From there you can navigate to the examples/defaults and edit parameters based on the parameters described in the README to deploy a larger instance or customize other parameters.  You will need local ssh keys (ie ssh-keygen) and the deployment will require paths to both the public and private keys. To run the deployment, run `terraform init && terraform apply`.  You will then be asked to fill in the paths to the ssh keys which you can also hardcode into the `example/defaults/main.tf`. 

Once the node is deployed, ssh into it and start the application manually just as you would if you were running the stack locally. There is also an option to run with SSL but that is out of scope of this tutorial. 

### Registering events

There are three types of objects you can register to the ICON API:
* Transactions
* Log events
* Broadcasters

### Transactions

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

### Log Events

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

### Broadcaster

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

#### Kafka

Filtered events are produced to the output topic (default: _outputs_).
Messages are keyed with the _to_address_ associated with the event, and have any associated _broadcaster_id_ included for filtering.
Messages that are time-sensitive should be consumed directly from the output topic and sent for further processing, as there may be additional delays/connectivity issues associated with websockets.

### Unregistering Events

Events can be easily unregistered by sending a POST request to the appropriate _/unregister_ endpoint with the same object that was used to register, except now including the associated ID.
Events that were registered by a broadcaster must be removed by modifying the broadcaster event or by unregistering the broadcaster.
