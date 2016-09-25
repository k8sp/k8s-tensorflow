# Dockerfiles

## build the containers
Just pick the dockerfile corresponding to the container you want to build, and run
```
$ docker build --pull -t $USER/tensorflow-suffix -f Dockerfile.suffix .
```

## References:
* https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/docker
