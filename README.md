# aws_instance_switch

quickly start or stop your instance

## Build your own docker image
``` bash
docker build -t <your image tag> .
```

## Run the command
``` bash
docker run -it --rm <image id> --action <start|stop|reboot|status> --access_key_id <your access key id> --access_key <your access key> --region us-east-2
```
region is optional.
`<image id>` can be the image tag you just built, or `putcn/instance_switch` to use the prebuilt one.