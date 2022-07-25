# Racoon

A TensorFlow based application to recognize people on video feeds.

# Docker
Build the docker image

`docker build -t my-name/my-image .`

Run the docker image

`docker run --rm -i -t my-name/my-image bash`

To copy something to or from a docker container

```bash
docker ps
docker cp <file path> <container id>:<destination path>
```

## TODO:
- [ ] train own dataset
- [ ] dockerize for deployment
- [ ] code quality with codacy
- [x] tensorflow
- [ ] pr based contributing
- [ ] discord webhook for results