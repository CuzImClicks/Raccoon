import time
from cmd import Cmd
import os
from Logger import Logger, Colors
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
            "compile": lambda text: ["tensorflow", "edgetpu", "compiler"],
            "start": lambda text: ["tensorflow", "edgetpu", "compiler"],
            "push": lambda text: ["tensorflow", "latest", "edgetpu"],
            "list": lambda text: ["containers", "running"],
            "upload": lambda text: os.listdir(".") if text else [
                file for file in os.listdir(".")
                if file.startswith(text)
            ],
            "exit": lambda text: [],
        }
        self.container_id = get_container_id()

    compile_presets = {
        "tensorflow": lambda
            name: f"docker build -t  {name + ':tensorflow' if not name.endswith(':tensorflow') else ''} . -f Dockerfile",
        "edgetpu": lambda
            name: f"docker build -t {name + ':tensorflow' if not name.endswith(':edgetpu') else ''} . -f Dockerfile_EdgeTPU",
        "edgetpu_compiler": lambda
            name: f"docker build -t {name + ':edgetpu_compiler' if not name.endswith(':edgetpu_compiler') else ''} . -f Dockerfile_Compiler",
        "gpu": lambda name: f"docker build -t {name + ':gpu' if not name.endswith(':gpu') else ''}"
    }

    def do_compile(self, line):
        """
        Build the docker image
        """
        flags = self.parse_flags(line)
        line = [s for s in line.split(" ") if not s == ""]
        repo = 'cuzimclicks/raccoon' if len(line) == 1 else ''.join(line[1:])
        if line[0] == "tensorflow":
            system(f"docker build -t  {repo} . -f Dockerfile")
        elif line[0] == "edgetpu":
            system(f"docker build -t {repo}:edgetpu . -f Dockerfile_EdgeTPU")
        elif line[0] == "compiler":
            system(f"docker build -t {repo}:edgetpu_compiler . -f Dockerfile_Compiler")
        else:
            system(f"docker build -t  {repo} . {'' if 'f' not in flags.keys() else '-f ' + flags['f']}")

    start_presets = {
        "tensorflow": lambda
            name: f":{name + ':tensorflow' if not name.endswith(':tensorflow') else ''} bash",
        "edgetpu": lambda
            name: f"docker run --rm -i -t --privileged -v /dev/bus/usb:/dev/bus/usb {name + ':tensorflow' if not name.endswith(':edgetpu') else ''} bash",
        "compiler": lambda
            name: f"docker run -i -t {name + ':edgetpu_compiler' if not name.endswith(':edgetpu_compiler') else ''} bash"
    }

    def do_start(self, line):
        """Starts the docker image"""
        match = re.fullmatch(r"^\s*(?P<name>\S+)(?:\s+(--?[a-zA-Z0-9]+)(?:\s+(\S+))?)*$", line)
        if not match:
            self.lg.error(f"Invalid input. Usage: start [tensorflow, edgetpu, compiler]|<name> flags")
            return
        name = match.groupdict()["name"]
        flags = {flag: value for flag, value in re.findall(r"(?P<flag>--?[a-zA-Z0-9]+)(?:\s+(?P<value>\S+))?", line)}
        # FIXME using tensorflow
        # FIXME flags
        # if name in self.completions["start"] and flags.:
        if not name:
            name = "cuzimclicks/raccoon"
        if flags.get("-p") or flags.get("--preset") or name in self.start_presets.keys():
            if name in self.start_presets.keys():
                system(self.start_presets[name](name))
            else:
                system(self.start_presets[flags["-p"] if "-p" in flags.keys() else flags["--preset"]](name))
        else:
            containers = [re.split(re.compile("\s+"), line) for line in cmd("docker container ps -a").splitlines()][1:]
            search = re.compile("".join([c for c in line.split(" ") if c != ""]))
            self.lg.info(f"Searching with regex: {search.pattern}")
            container = [con for con in containers if re.findall(search, "".join([con[-1], con[1]]))]
            selector = {index + 1: con for index, con in enumerate(container)}
            print("".join([f"{index} -> {''.join([p + '    ' for p in [con[1], con[-1]]])}\n" for index, con in
                           selector.items()]))
            inp = None if len(selector) > 1 else 1
            while inp is None:
                try:
                    inp = input('Selector >>> ')
                    if inp.lower() == "exit":
                        return
                    inp = int(inp)
                    if inp not in range(1, list(selector.keys())[-1]):
                        raise ValueError()
                except ValueError:
                    self.lg.error(
                        f"Input must be an integer in the range of ({list(selector.keys())[0]}, {list(selector.keys())[-1]})")
                    inp = None
            self.lg.info(f"Starting docker container with name {selector[inp][-1]}")
            system(f"docker start -i {selector[inp][0]} {''.join([f'{flag} {value}' for flag, value in flags])}")
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
        search = re.compile(''.join(line[1:]))
        print("".join([f"{line}\n" for line in cmd(f"docker container ps -a").splitlines() if
                       re.search(search, line) or line[0].startswith("CONTAINER ID")]))

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
        line = line.split(" ")
        command = line[0]
        if text:
            return [
                cmd for cmd in self.completions[command](text)
                if cmd.startswith(text)
            ]
        else:
            return self.completions[command](text)

    @staticmethod
    def parse_flags(string: str) -> dict:
        return {result[0]: result[1] for result in re.findall(r"(?P<flag>-+\w+) (?P<input>\w+)?", string)}


if __name__ == "__main__":
    my_cmd = DockerBridge()
    my_cmd.cmdloop()
