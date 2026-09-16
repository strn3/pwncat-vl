from pathlib import Path

import pwncat
from pwncat.commands import CommandDefinition
from pwncat.util import console


class Command(CommandDefinition):
    """Print the local current working directory"""

    PROG = "lpwd"
    ARGS = {}

    def run(self, manager: "pwncat.manager.Manager", args):

        console.print(Path.cwd())
