import argparse

from ml_dcs_bench.cmd.base import BaseCommand


class CreateTestCaseCommand(BaseCommand):
    name = "create_testcase"
    help = "Create a DCS test case"

    def add_arguments(self, parser):
        pass

    def execute(self, args: argparse.Namespace):
        pass
