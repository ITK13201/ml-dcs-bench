import argparse
from typing import Type

from ml_dcs_bench.cmd.base import BaseCommand
from ml_dcs_bench.cmd.create_testcase import CreateTestCaseCommand


class RootCommand:
    description = "Script for benchmark testing."
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest="command")

    def add_command(self, command_class: Type[BaseCommand]):
        command = command_class()
        subparser = self.subparsers.add_parser(command.name, help=command.help)
        command.add_arguments(subparser)
        subparser.set_defaults(handler=command.execute)

    def __init__(self):
        self.add_command(CreateTestCaseCommand)

    def execute(self):
        args = self.parser.parse_args()
        if hasattr(args, "handler"):
            args.handler(args)
        else:
            self.parser.print_help()