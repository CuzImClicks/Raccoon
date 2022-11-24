import subprocess
import time
import os
import requests
from Logger import Logger


def cmd(command):
    if type(command) is str:
        command = command.split(" ")

    return subprocess.check_output(command).decode()


def system(command):
    return os.system(str(command))


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

lg = Logger("Docker Bridge", formatter=Logger.minecraft_formatter)


lg.info("_" * 20)
lg.info(f"CuzImClicks/Raccoon Docker Bridge")
lg.info("\n")

lg.info("""\nCommands
upload <number|filepath|url id>     - copy an image to the current docker container
download <number|filepath>          - download an image from the current docker container
mv <file> <new_loc>                 - move a file
printenv                            - print all environment variables
id                                  - prints current docker id
exit                                - exits

compile                             - build the docker image
start                               - start the docker image
push                                - push the docker image to docker hub
""")

while True:
    argv = input("docker bridge >>> ")
    argv = argv.strip().split(" ")
    first = argv.pop(0)
    if first == "upload":
        if argv[0].startswith("https://") and len(argv) == 2:
            response = requests.get(argv[0])
            with open(f"image{argv[1]}.jpg", "wb") as file:
                file.write(response.content)
            docker_cp(f"image{argv[1]}.jpg", f"{container_id}:/home/models/research/input")
            lg.info(f"Docker copied image{argv[1]} to container: {container_id}")
            time.sleep(2)
            continue

        if not len(argv) == 1:
            lg.info("Usage")
            lg.info("upload <number|filepath>")
            lg.info("    number - The number of the image (image<number>.jpg)")
            lg.info("    filepath - The path to the image")
            continue

        for file in argv:
            if is_int(file):
                file = f"image{file}.jpg"
            lg.debug(file)
            if not file.endswith(".jpg"):
                continue

            docker_cp(file, f"{container_id}:/home/models/research/input")
            lg.info(f"Docker copied {file} to container: {container_id}")
            time.sleep(2)

    elif first == "download":
        if not len(argv) == 1:
            lg.info("Usage")
            lg.info("download <number|filepath>")
            lg.info("    number - The number of the image (image<number>.jpg)")
            lg.info("    filepath - The path to the image")
            continue
        for file in argv:
            if is_int(file):
                file = f"new_image{file}.jpg"
            if not file.startswith("new_"):
                file = f"new_{file}"

            docker_cp(f"{container_id}:/home/models/research/output/{file}", ".")
            lg.info(f"Docker copied {file} from container: {container_id}")
            time.sleep(2)

    elif first == "mv":
        if not len(argv) == 2:
            lg.info("mv <file> <new_loc>")
            lg.info("    file - The current location of the file")
            lg.info("    new_loc - New location of the file")
            continue

        os.replace(f"./{argv[1]}", f"./{argv[2]}")
        lg.info(f"Moved file ./{argv[1]} ./{argv[2]}")

    elif first == "env":
        lg.warning("Not working")
        continue
        #if not len(argv) == 2:
        #    print("env <name> <value>")
        #    print("    name - The name of the environment variable")
        #    print("    value - The value of the environment variable")
        #    continue

        #system(f'export {str(argv[0])}="{str(argv[1])}"')
        #print(f"Set env {str(argv[0])} = {str(argv[1])}")

    elif first == "printenv":
        if len(argv) > 0:
            environ_dict = os.environ
            arg = argv[0]
            if arg in environ_dict.keys():
                lg.info(f"{arg} = {environ_dict[arg]}")
            else:
                lg.info(f"The environment variables do not contain {arg}")

            continue
        lg.info(os.environ)

    elif first == "id":
        lg.info(container_id)

    elif first == "exit":
        exit()

    elif first == "compile":
        if not len(argv) == 1:
            system("docker build -t cuzimclicks/raccoon .")

        else:
            system(f"docker build -t {argv[0]} .")
        
    elif first == "start":
        if not len(argv) == 1:
            system("docker run --rm -i -t cuzimclicks/raccoon bash")
        
        else:
            system(f"docker run --rm -i -t {argv[0]} bash")

    elif first == "push":
        lg.warning("Warning you have to be logged in!")
        if not len(argv) == 1:
            system("docker push cuzimclicks/raccoon")

        else:
            system(f"docker push {argv[0]}")
