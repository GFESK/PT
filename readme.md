# README

This document provides instructions for deploying a web application service using docker.

## Setup

To deploy the service, use the following command:

```shell
docker-compose up
```

The service pulls the base image from Docker Hub, which contains the necessary libraries and a pre-trained model.

Base image link: [Docker Hub Image](https://hub.docker.com/r/gfesk/pt_test_base_img/tags)

By default, the web application starts up on `0.0.0.0:8080`. You can change this in the config file. Don't forget to adjust corresponding settings in compose and Docker.

## API Usage

Below is an example of how to use the provided API:

```python
import requests
import json

data = ([{"data": "{\"CLIENT_IP\": \"188.138.92.55\", \"CLIENT_USERAGENT\": NaN, \"REQUEST_SIZE\": 166, \"RESPONSE_CODE\": 404, \"MATCHED_VARIABLE_SRC\": \"REQUEST_URI\", \"MATCHED_VARIABLE_NAME\": NaN, \"MATCHED_VARIABLE_VALUE\": \"//tmp/20160925122692indo.php.vob\", \"EVENT_ID\": \"AVdhXFgVq1Ppo9zF5Fxu\"}"},
       {"data": "{\"CLIENT_IP\": \"93.158.215.131\", \"CLIENT_USERAGENT\": \"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0\", \"REQUEST_SIZE\": 431, \"RESPONSE_CODE\": 302, \"MATCHED_VARIABLE_SRC\": \"REQUEST_GET_ARGS\", \"MATCHED_VARIABLE_NAME\": \"url\", \"MATCHED_VARIABLE_VALUE\": \"http://www.galitsios.gr/?option=com_k2\", \"EVENT_ID\": \"AVdcJmIIq1Ppo9zF2YIp\"}"}])

r = requests.post('http://127.0.0.1:8080/predict', json=data)

print(r.json())
```

This request will return a JSON array of predictions, like this:

```json
[
    {
        "EVENT_ID": "AVdhXFgVq1Ppo9zF5Fxu",
        "LABEL_PRED": "1",
        "Elapsed time": "8.30082392692566"
    },
    {
        "EVENT_ID": "AVdcJmIIq1Ppo9zF2YIp",
        "LABEL_PRED": "1",
        "Elapsed time": "2.6966137886047363"
    }
]
```