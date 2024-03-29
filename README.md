# fast-food-application

[![CI-CD](https://github.com/sammiee5311/fast-food-application/actions/workflows/CI-CD.yml/badge.svg?branch=main)](https://github.com/sammiee5311/fast-food-application/actions/workflows/CI-CD.yml)

## expected BPMN

![](./images/order-bpmn.png)


## system design

![](./images/system-design.jpg)

## tech stacks
<details>
<summary>See</summary>

### Back-end
 - flask
 - django
 - fast-api
 - node.js

### Front-end
 - react

### Database
 - postgres
 - sqlite
 - mongodb
 - redis 

### Message
 - kafka 

### Log
 - elasticsearch
 - logstash
 - kibana 

### Machine Learning
 - mlflow 

### Languages
 - python
 - javascript
 - typescript   

### Build 
 - docker

### Proxy
 - nginx
 
### Trace
 - Opentelemetry
 - Jaeger

### CI / CD
 - gitHub actions  
 - heroku 
 
</details> 

## servers

- [django](https://github.com/sammiee5311/fast-food-application/tree/main/django)
- [react](https://github.com/sammiee5311/fast-food-application/tree/main/react)
- [kafka](https://github.com/sammiee5311/fast-food-application/tree/main/kafka)
- [log](https://github.com/sammiee5311/fast-food-application/tree/main/log)
- [order-delivery-time-handler](https://github.com/sammiee5311/fast-food-application/tree/main/order-delivery-time-handler)
- [machine-learning](https://github.com/sammiee5311/fast-food-application/tree/main/machine-learning-api)
- [tracking & restaurant](https://github.com/sammiee5311/fast-food-application/tree/main/tracking)
- [id-generator](https://github.com/sammiee5311/fast-food-application/tree/main/id-generator)
- [otel-collector](https://github.com/sammiee5311/fast-food-application/tree/main/otel-collector)

## ports

- logstash: `5501`
- elasticsearch: `9200`
- kibana: `5601`
- zookeeper: `2181`
- kafka: `9092`
- kafka-manager: `9000`
- django: `8000`
- order-delivery-time-handler: `8080`
- tracking: `3001`
- react: `3000`
- mlflow: `1234`
- postgres: `5432`
- otel-collector: `4317`
- jaeger: `14268`

## reference

- [docker-elk](https://github.com/deviantony/docker-elk)
