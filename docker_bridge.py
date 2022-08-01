import subprocess
import sys
import time
import os

def cmd(command):
    if type(command) is str:
        command = command.split(" ")

    return subprocess.check_output(command).decode()

def get_container_id():
    return cmd("docker ps").split("\n")[1][:12]

container_id = get_container_id()


def docker_cp(first, second):
    cmd(f"docker cp {first} {second}")


def is_int(number):
    try:
        number = int(number)
        return True
    except:
        return False

while True:
    argv = input("docker bridge >>> ")
    argv = argv.split(" ")
    first = argv.pop(0)
    if first == "upload":
        for file in argv:
            if is_int(file):
                file = f"image{file}.jpg"
            print(file)
            if not file.endswith(".jpg"):
                continue
            
            docker_cp(file, f"{container_id}:/home/models/research/input")
            print(f"Docker copied {file} to container: {container_id}")
            time.sleep(2)

    elif first == "download":
        for file in argv:
            if is_int(file):
                file = f"new_image{file}.jpg"
            if not file.startswith("new_"):
                file = f"new_{file}"
            
            docker_cp(f"{container_id}:/home/models/research/output/{file}", ".")
            print(f"Docker copied {file} from container: {container_id}")
            time.sleep(2)

    elif first == "mv":
        os.replace(f"./{argv[1]}", f"./{argv[2]}")
        print(f"Moved file ./{argv[1]} ./{argv[2]}")

    elif first == "env":
        os.environ[str(argv[0])] = str(argv[1])
        print(f"Set env {str(argv[0])} = {str(argv[1])}")

    elif first == "printenv":
        if len(argv) > 0:
            print(os.environ[argv[0]])
        print(os.environ)

    elif first == "exit":
        exit()