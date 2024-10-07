import argparse


class BaseCommand:
    name = ""
    help = ""

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    def execute(self, args: argparse.Namespace):
        pass
