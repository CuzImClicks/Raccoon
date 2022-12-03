# Racoon

A TensorFlow based application to recognize people on video feeds.

# Docker - How to run
Build the docker image

`docker build -t my-name/my-image .`

Run the docker image

`docker run --rm -i -t my-name/my-image bash`

In the bash command line run to start the program

`python plot_object_detection_saved_model.py`

To copy something(the final images) to or from a docker container

```bash
docker ps
docker cp <file path> <container id>:<destination path>
```

## TensorFlow (no-avx, no-gpu)
https://github.com/yaroslavvb/tensorflow-community-wheels/issues/217

## TODO:
- [ ] train own dataset
- [x] dockerize for deployment
- [ ] code quality with codacy
- [x] tensorflow
- [ ] pr based contributing
- [ ] discord webhook for results

<details>
<summary>Links</summary>

### Links
<details>
<summary>usbipd</summary>

https://github.com/dorssel/usbipd-win
https://github.com/dorssel/usbipd-win/wiki/WSL-support
https://github.com/dorssel/usbipd-win/issues/264
</details>



</details>