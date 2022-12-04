from cmd import Cmd
import os
from Logger import Logger, Colors, FileHandler
import subprocess


def cmd(command):
    if type(command) is str:
        command = command.split(" ")

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
            "start": ["tensorflow", "edgetpu"],
            "push": ["tensorflow", "latest", "edgetpu"],
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
            system(f"docker build -t {repo}:edgetpu . -f Dockerfile_EdgeTPU)")
        elif line[0] == "compiler":
            system(f"docker build -t {repo}:edgetpu_compiler . -f Dockerfile_Compiler)")
        else:
            system(f"docker build -t  {repo} .")

    def do_start(self, line):
        """Starts the docker image"""
        line = [s for s in line.split(" ") if not s == ""]
        repo = 'cuzimclicks/raccoon' if len(line) == 1 else ''.join(line[1:])
        if line[0] == "tensorflow":
            system(f"docker run --rm -i -t {repo} bash")
        elif line[0] == "edgetpu":
            self.lg.warning(f"Running the docker image with {Colors.BOLD.value}--privileged{Colors.RESET.value}{Colors.YELLOW.value} flag")
            system(f"docker run --rm -i -t --privileged -v /dev/bus/usb:/dev/bus/usb {repo}:edgetpu bash")
        elif line[0] == "compiler":
            system(f"docker run --rm -i -t {repo}:edgetpu_compiler bash")
        else:
            system(f"docker run --rm -i -t {repo} bash")
        self.container_id = get_container_id()

    def do_upload(self, line):
        """TODO"""
        ...

    def do_download(self, line):
        """TODO"""
        ...

    def do_id(self, line):
        """Print the current docker id"""
        if not self.container_id:
            self.container_id = get_container_id()
        self.lg.info(f"Current Docker Id is {self.container_id}")

    def do_push(self, line):
        """Push the Docker image to Docker Hub"""
        self.lg.warning("Warning you have to be logged in!")
        line = [s for s in line.split(" ") if not s == ""]
        print(line)
        if len(line) == 0 or line[0] == "tensorflow" or line[0] == "latest":
            print("docker push cuzimclicks/raccoon")
            system("docker push cuzimclicks/raccoon")
        elif line[0] == "edgetpu":
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


my_cmd = DockerBridge()
my_cmd.cmdloop()
