# aws_instance_switch

quickly start or stop your instance

## Build with docker
``` bash
docker build -t <your image tag> .
```

## Run the command
``` bash
docker run -it --rm <your image id> --action <start|stop|reboot|status> --access_key_id <your access key id> --access_key <your access key> --region us-east-2
```
region is optional