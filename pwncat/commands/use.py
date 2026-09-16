import pwncat
from pwncat.commands import CommandDefinition, Complete, Parameter, get_module_choices
from pwncat.util import console


class Command(CommandDefinition):
    """
    Set the currently used module in the config handler
    """

    PROG = "use"
    ARGS = {
        "module": Parameter(
            Complete.CHOICES,
            choices=get_module_choices,
            metavar="MODULE",
            help="the module to use",
        ),
    }
    LOCAL = False

    def run(self, manager: "pwncat.manager.Manager", args):

        try:
            module = next(iter(manager.target.find_module(args.module, exact=True)))
        except IndexError:
            console.log(f"[red]error[/red]: {args.module}: no such module")
            return

        manager.target.config.use(module)
