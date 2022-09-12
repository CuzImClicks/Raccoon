import subprocess
import sys
import time
import os

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

print("_"*20)
print(f"CuzImClicks/Raccoon Docker Bridge")
print("\n")

print("""Commands
upload <number|filepath>
download <number|filepath>
mv <file> <new_loc>
printenv
id
exit
""")

while True:
    argv = input("docker bridge >>> ")
    argv = argv.split(" ")
    first = argv.pop(0)
    if first == "upload":
        if not len(argv) == 1:
            print("Usage")
            print("upload <number|filepath>")
            print("    number - The number of the image (image<number>.jpg)")
            print("    filepath - The path to the image")
            continue
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
        if not len(argv) == 1:
            print("Usage")
            print("download <number|filepath>")
            print("    number - The number of the image (image<number>.jpg)")
            print("    filepath - The path to the image")
            continue
        for file in argv:
            if is_int(file):
                file = f"new_image{file}.jpg"
            if not file.startswith("new_"):
                file = f"new_{file}"
            
            docker_cp(f"{container_id}:/home/models/research/output/{file}", ".")
            print(f"Docker copied {file} from container: {container_id}")
            time.sleep(2)

    elif first == "mv":
        if not len(argv) == 2:
            print("mv <file> <new_loc>")
            print("    file - The current location of the file")
            print("    new_loc - New location of the file")
            continue

        os.replace(f"./{argv[1]}", f"./{argv[2]}")
        print(f"Moved file ./{argv[1]} ./{argv[2]}")

    elif first == "env":
        print("Not working")
        continue
        if not len(argv) == 2:
            print("env <name> <value>")
            print("    name - The name of the environment variable")
            print("    value - The value of the environment variable")
            continue

        system(f'export {str(argv[0])}="{str(argv[1])}"')
        print(f"Set env {str(argv[0])} = {str(argv[1])}")

    elif first == "printenv":
        if len(argv) > 0:
            environ_dict = os.environ
            arg = argv[0]
            if arg in environ_dict.keys():
                print(f"{arg} = {environ_dict[arg]}")
            else:
                print(f"The environment variables do not contain {arg}")
                
            continue
        print(os.environ)

    elif first == "id":
        print(container_id)

    elif first == "exit":
        exit()