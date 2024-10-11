import argparse
import os.path
from itertools import chain, combinations
from logging import getLogger
from typing import Iterable, Iterator, List

import yaml

from ml_dcs_bench.cmd.base import BaseCommand
from ml_dcs_bench.domain.lts import ControllerSpec

logger = getLogger(__name__)

LTS_COMPONENTS_BASE_DIR = os.path.join("assets", "lts-components")
DEFAULT_LTS_COMPONENTS = [
    "AT（2, 2）",
    "AT（2, 3）",
    "AT（2, 4）",
    # "AT（2, 5）",
    # "AT（3, 3）",
    # "AT（3, 4）",
    # "AT（3, 5）",
    # "AT（4, 4）",
    # "AT（4, 5）",
    # "AT（5, 5）",
    # "AT（5, 10）",
]
DEFAULT_OUTPUT_DIR = os.path.join("tmp", "output")


class CreateTestCasesCommand(BaseCommand):
    name = "create_testcases"
    help = "Create test cases"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "-l",
            "--lts-components",
            nargs="*",
            help="List of lts component",
            default=DEFAULT_LTS_COMPONENTS,
        )
        parser.add_argument(
            "-o",
            "--output-dir",
            type=str,
            required=False,
            help="Output directory",
            default=DEFAULT_OUTPUT_DIR,
        )

    def __init__(self):
        super().__init__()
        self.lts_component_names: List[str] = []
        self.output_dir: str = ""

    def execute(self, args: argparse.Namespace):
        logger.info("CreateTestCasesCommand started")

        self.lts_component_names = args.lts_components
        self.output_dir = args.output_dir

        for lts_component_name in self.lts_component_names:
            logger.info("creating test cases... : {}".format(lts_component_name))

            # load
            models_string = self._load_models_string(lts_component_name)
            controller_spec = self._load_controller_spec(lts_component_name)
            targets_string = self._load_targets_string(lts_component_name)

            # build
            for index, new_controller_spec in enumerate(
                self._build_controller_spec_safety_powerset(controller_spec)
            ):
                controller_spec_string = self._build_controller_spec_string(
                    new_controller_spec
                )

                # dump
                output_file_name = "{}_{}.lts".format(
                    lts_component_name, str(index).zfill(6)
                )
                self._dump_lts(
                    models_string,
                    controller_spec_string,
                    targets_string,
                    output_file_name,
                )

            logger.info(
                "successfully created test cases: {}".format(lts_component_name)
            )

        logger.info("CreateTestCasesCommand finished")

    def _load_models_string(self, lts_component_name: str):
        file_path = os.path.join(
            LTS_COMPONENTS_BASE_DIR, lts_component_name, "models.lts"
        )
        with open(file_path, mode="r") as f:
            models_string = f.read()
        return models_string

    def _load_controller_spec(self, lts_component_name: str) -> ControllerSpec:
        file_path = os.path.join(
            LTS_COMPONENTS_BASE_DIR, lts_component_name, "cspec.yaml"
        )
        with open(file_path, mode="r", encoding="utf-8") as f:
            controller_spec = yaml.safe_load(f)
        return ControllerSpec(**controller_spec)

    def _load_targets_string(self, lts_component_name: str):
        file_path = os.path.join(
            LTS_COMPONENTS_BASE_DIR, lts_component_name, "targets.lts"
        )
        with open(file_path, mode="r") as f:
            targets_string = f.read()
        return targets_string

    def _powerset(self, iterable: Iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    def _build_controller_spec_safety_powerset(
        self, controller_spec: ControllerSpec
    ) -> Iterator[ControllerSpec]:
        safety_properties = controller_spec.safety
        safety_properties_powerset = self._powerset(safety_properties)
        for safety_properties_set in safety_properties_powerset:
            new_controller_spec = controller_spec.model_copy(deep=True)
            new_controller_spec.safety = safety_properties_set
            yield new_controller_spec

    def _build_controller_spec_string(self, controller_spec: ControllerSpec) -> str:
        result = []
        indent = 0

        # controllerSpec bgn
        result.append("controllerSpec {} = {{".format(controller_spec.name))
        indent += 1

        # safety
        result.append("{}safety = {{".format("\t" * indent))
        indent += 1
        for safety_property in controller_spec.safety:
            result.append("{}{},".format("\t" * indent, safety_property))
        indent -= 1
        result.append("{}}}".format("\t" * indent))

        # controllable
        result.append("{}controllable = {{".format("\t" * indent))
        indent += 1
        for controllable_action in controller_spec.controllable:
            result.append("{}{},".format("\t" * indent, controllable_action))
        indent -= 1
        result.append("{}}}".format("\t" * indent))

        # marking
        if controller_spec.marking:
            result.append("{}marking = {{".format("\t" * indent))
            indent += 1
            for controllable_action in controller_spec.controllable:
                result.append("{}{},".format("\t" * indent, controllable_action))
            indent -= 1
            result.append("{}}}".format("\t" * indent))

        # nonblocking
        if controller_spec.nonblocking:
            result.append("{}nonblocking".format("\t" * indent))

        # controllerSpec end
        indent -= 1
        result.append("}\n")

        return "\n".join(result)

    def _dump_lts(
        self,
        models_string: str,
        controller_spec_string: str,
        targets_string: str,
        output_file_name: str,
    ):
        context = "\n".join([models_string, controller_spec_string, targets_string])
        output_path = os.path.join(self.output_dir, output_file_name)
        with open(output_path, mode="w", encoding="utf-8") as f:
            f.write(context)
