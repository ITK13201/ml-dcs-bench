import argparse
import os.path
import random
import shutil
from itertools import chain, combinations
from logging import getLogger
from typing import Iterable, Iterator, List

import yaml

from ml_dcs_bench.cmd.base import BaseCommand
from ml_dcs_bench.domain.lts import ControllerSpec

logger = getLogger(__name__)

LTS_COMPONENTS_BASE_DIR = os.path.join("assets", "lts-components")
DEFAULT_LTS_COMPONENTS = [
    "ArtGallery（N, 2 room）",
    "ArtGallery（N, 3 room）",
    "ArtGallery（N, 4 room）",
    "ArtGallery（N, 5 room）",
    "ArtGallery（N, 6 room）",
    "ArtGallery（N, 7 room）",
    "ArtGallery（N, 8 room）",
    "ArtGallery（N, 9 room）",
    "ArtGallery（N, 10 room）",
    "ArtGallery（S, 5 people）",
    "ArtGallery（S, 6 people）",
    "ArtGallery（S, 7 people）",
    "ArtGallery（S, 8 people）",
    "ArtGallery（S, 9 people）",
    "ArtGallery（S, 10 people）",
    "AT（2, 2）",
    "AT（2, 3）",
    "AT（2, 4）",
    "AT（2, 5）",
    "AT（3, 3）",
    "AT（3, 4）",
    "AT（3, 5）",
    "AT（4, 4）",
    "AT（4, 5）",
    "AT（5, 5）",
    "AT（5, 10）",
    "BW（2, 2）",
    "BW（2, 3）",
    "BW（2, 4）",
    "BW（2, 5）",
    "BW（3, 2）",
    "BW（3, 3）",
    "BW（3, 4）",
    "BW（3, 5）",
    "BW（4, 2）",
    "BW（4, 3）",
    "BW（4, 4）",
    "BW（4, 5）",
    "BW（5, 2）",
    "BW（5, 3）",
    "BW（5, 4）",
    "BW（5, 5）",
    "CM（2, 2）",
    "CM（2, 3）",
    "CM（2, 4）",
    "CM（2, 5）",
    "CM（3, 2）",
    "CM（3, 3）",
    "CM（3, 4）",
    "CM（3, 5）",
    "CM（4, 2）",
    "CM（4, 3）",
    "CM（4, 4）",
    "CM（4, 5）",
    "CM（5, 2）",
    "CM（5, 3）",
    "CM（5, 4）",
    "CM（5, 5）",
    "KIVA_system（N, 2 robot）",
    "KIVA_system（N, 3 robot）",
    "KIVA_system（N, 4 robot）",
    "KIVA_system（S, 5 pod）",
    "KIVA_system（S, 10 pod）",
    "KIVA_system（S, 20 pod）",
    "KIVA_system（S, 30 pod）",
]
DEFAULT_OUTPUT_DIR = os.path.join("tmp", "testcases")
NUMBER_OF_ITEMS_TO_BE_RANDOMLY_SELECTED = 200


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
        parser.add_argument(
            "-O",
            "--overwrite",
            action="store_true",
            help="Overwrite existing output directory",
            default=False,
        )

    def __init__(self):
        super().__init__()
        self.lts_component_names: List[str] = []
        self.output_dir: str = ""
        self.is_allowed_override = False

    def execute(self, args: argparse.Namespace):
        logger.info("CreateTestCasesCommand started")

        self.lts_component_names = args.lts_components
        self.output_dir = args.output_dir
        self.is_allowed_override = args.overwrite

        if self.is_allowed_override:
            # recreate output dir
            logger.info("recreating output directory...")
            shutil.rmtree(DEFAULT_OUTPUT_DIR)
            os.mkdir(DEFAULT_OUTPUT_DIR)
            logger.info("successfully recreated output directory")

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

    def _powerset_without_empty(self, iterable: Iterable) -> List[List[str]]:
        s = list(iterable)
        # powerset = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
        powerset_without_empty = chain.from_iterable(
            combinations(s, r) for r in range(1, len(s) + 1)
        )
        return list(powerset_without_empty)

    def _choice_combinations_randomly(self, iterable: Iterable) -> List[List[str]]:
        s = list(iterable)
        length = len(s)
        if 2**length - 1 < NUMBER_OF_ITEMS_TO_BE_RANDOMLY_SELECTED:
            raise RuntimeError("Not enough items selected")

        selected_numbers = set()
        selected_combinations = []
        for _ in range(NUMBER_OF_ITEMS_TO_BE_RANDOMLY_SELECTED):
            while True:
                random_number = random.randint(1, 2**length - 1)
                if random_number not in selected_numbers:
                    selected_numbers.add(random_number)
                    break
            random_binary_number = format(random_number, "0{}b".format(length))
            random_binary_number_list = list(random_binary_number)

            combination = []
            for index, bit in enumerate(random_binary_number_list):
                if bit == "0":
                    continue
                elif bit == "1":
                    combination.append(s[index])
            selected_combinations.append(combination)
        return selected_combinations

    def _build_controller_spec_safety_powerset(
        self, controller_spec: ControllerSpec
    ) -> Iterator[ControllerSpec]:
        safety_properties = controller_spec.safety
        if 2 ** len(safety_properties) - 1 < NUMBER_OF_ITEMS_TO_BE_RANDOMLY_SELECTED:
            safety_properties_combinations = self._powerset_without_empty(
                safety_properties
            )
        else:
            safety_properties_combinations = self._choice_combinations_randomly(
                safety_properties
            )
        for safety_properties_set in safety_properties_combinations:
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
        for index, safety_property in enumerate(controller_spec.safety):
            if index != len(controller_spec.safety) - 1:
                result.append("{}{},".format("\t" * indent, safety_property))
            else:
                result.append("{}{}".format("\t" * indent, safety_property))
        indent -= 1
        result.append("{}}}".format("\t" * indent))

        # controllable
        result.append("{}controllable = {{".format("\t" * indent))
        indent += 1
        for index, controllable_action in enumerate(controller_spec.controllable):
            if index != len(controller_spec.controllable) - 1:
                result.append("{}{},".format("\t" * indent, controllable_action))
            else:
                result.append("{}{}".format("\t" * indent, controllable_action))
        indent -= 1
        result.append("{}}}".format("\t" * indent))

        # marking
        if controller_spec.marking:
            result.append("{}marking = {{".format("\t" * indent))
            indent += 1
            for index, marking_action in enumerate(controller_spec.marking):
                if index != len(controller_spec.marking) - 1:
                    result.append("{}{},".format("\t" * indent, marking_action))
                else:
                    result.append("{}{}".format("\t" * indent, marking_action))
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
