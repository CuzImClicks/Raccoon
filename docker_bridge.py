import time
from cmd import Cmd
import os
from Logger import Logger, Colors, FileHandler
import subprocess
import re


def cmd(command):
    if type(command) is str:
        command = [cmd for cmd in command.split(" ") if cmd != ""]

    return subprocess.check_output(command).decode()


def system(command):
    return os.system(str(command))


def get_container_id():
    try:
        return cmd("docker ps").split("\n")[1][:12]
    except Exception as e:
        print("Docker is not running!")
        return ""


class DockerBridge(Cmd):

    def __init__(self):
        super().__init__()
        self.prompt = 'docker bridge >>> '
        self.lg = Logger("DockerBridge", formatter=Logger.minecraft_formatter)
        self.completions = {
            "compile": ["tensorflow", "edgetpu", "compiler"],
            "start": ["tensorflow", "edgetpu", "compiler"],
            "push": ["tensorflow", "latest", "edgetpu"],
            "list": ["containers", "running"],
            "exit": [],
        }
        self.container_id = get_container_id()

    def do_compile(self, line):
        """
        Build the docker image
        """
        line = line.split(" ")
        repo = 'cuzimclicks/raccoon' if len(line) == 1 else ''.join(line[1:])
        if line[0] == "tensorflow":
            system(f"docker build -t  {repo} . -f Dockerfile")
        elif line[0] == "edgetpu":
            system(f"docker build -t {repo}:edgetpu . -f Dockerfile_EdgeTPU")
        elif line[0] == "compiler":
            system(f"docker build -t {repo}:edgetpu_compiler . -f Dockerfile_Compiler")
        else:
            system(f"docker build -t  {repo} .")

    def do_start(self, line):
        """Starts the docker image"""
        line = [s for s in line.split(" ") if not s == ""]
        repo = 'cuzimclicks/raccoon' if len(line) == 0 else ''.join(line)
        containers = [re.split(re.compile("\s+"), line) for line in cmd("docker container ps -a").splitlines()][1:]
        search = re.compile("".join(line))
        container = [con for con in containers if re.fullmatch(search, con[-1])]
        if len(container) > 0:
            first = container[0]
            self.lg.info(f"Found {len(container)}/{len(containers)} container(s)")
            self.lg.info(f"Starting '{first[-1]}' based on image '{first[1]}'")
            time.sleep(1)
            system(f"docker start -i {first[0]}")
            return
        if line[0] == "tensorflow":
            system(f"docker run --rm -i -t {repo} bash")
        elif line[0] == "edgetpu":
            self.lg.warning(
                f"Running the docker image with {Colors.BOLD.value}--privileged{Colors.RESET.value}{Colors.YELLOW.value} flag")
            system(f"docker run --rm -i -t --privileged -v /dev/bus/usb:/dev/bus/usb {repo}:edgetpu bash")
        elif line[0] == "compiler":
            system(f"docker run -i -t {repo}:edgetpu_compiler bash")
        else:
            system(f"docker run --rm -i -t {repo} bash")
        self.container_id = get_container_id()

    def do_upload(self, line):
        """TODO"""
        ...

    def do_download(self, line):
        """TODO"""
        ...

    def do_list(self, line):
        """Lists all docker containers and gives the option to filter them with regex"""
        line = [s for s in line.split(" ") if not s == ""]
        mode = '-a' if line[0] == 'containers' else ''
        if len(line) == 2:
            search = re.compile(''.join(line[1:]))
            print("".join([f"{line}\n" for line in cmd(f"docker container ps {mode}").splitlines() if
                           re.search(search, line) or line[0].startswith("CONTAINER ID")]))
        else:
            system(f"docker container ps {mode}")

    def do_id(self, line):
        """Print the current docker id"""
        if not self.container_id:
            self.container_id = get_container_id()
        self.lg.info(f"Current Docker Id is {self.container_id}")

    def do_push(self, line):
        """Push the Docker image to Docker Hub"""
        self.lg.warning("Warning you have to be logged in!")
        line = [s for s in line.split(" ") if not s == ""]
        if len(line) == 0 or line[0] == "tensorflow" or line[0] == "latest":
            system("docker push cuzimclicks/raccoon")
        elif line[0] == "edgetpu":
            self.lg.info("Pushing to Tag edgetpu")
            system("docker push cuzimclicks/raccoon:edgetpu")
        else:
            system(f"docker push {''.join(line)}")

    def do_exit(self, line):
        """Exits the CLI"""
        exit()

    def monad_print(self, *args):
        print(args)

    def preloop(self):
        for k, v in self.completions.items():
            setattr(DockerBridge, 'complete_' + k, self.complete_)

    def complete_(self, text, line, start_index, end_index):
        command = line.split(" ", maxsplit=1)[0]
        if text:
            return [
                cmd for cmd in self.completions[command]
                if cmd.startswith(text)
            ]
        else:
            return self.completions[command]

    def complete_upload(self, text, line, start_index, end_index):
        if text:
            return [
                file for file in os.listdir(".")
                if file.startswith(text)
            ]
        else:
            return os.listdir(".")


if __name__ == "__main__":
    my_cmd = DockerBridge()
    my_cmd.cmdloop()
