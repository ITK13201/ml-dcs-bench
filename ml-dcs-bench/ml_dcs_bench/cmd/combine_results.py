import argparse
import glob
import json
import os
from logging import getLogger

from ml_dcs_bench.cmd.base import BaseCommand
from ml_dcs_bench.domain.result import RunResult

logger = getLogger(__name__)


class CombineResultsCommand(BaseCommand):
    name = "combine_results"
    help = "Combine results"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "-d",
            "--results-dir",
            type=str,
            required=False,
            help="Directory containing results to combine",
        )
        parser.add_argument(
            "-f",
            "--result-files",
            type=str,
            action="append",
            default=[],
            required=False,
            help="Result files to combine",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            required=True,
        )

    def __init__(self):
        super().__init__()

        # CLI arguments
        self.results_dir_path = None
        self.result_file_paths = None
        self.output_file_path = None

    def execute(self, args: argparse.Namespace):
        logger.info("CombineResultsCommand started")

        if args.result_files:
            self.result_file_paths = args.result_files
        else:
            self.results_dir_path = args.results_dir
            self.result_file_paths = glob.glob(
                os.path.join(self.results_dir_path, "*.json")
            )
        self.output_file_path = args.output

        results = []
        for result_file_path in self.result_file_paths:
            logger.info("loading results... : %s", result_file_path)
            with open(result_file_path, "r") as f:
                result_json = json.load(f)
                result = RunResult(**result_json)
                results.append(result)
            logger.info("done")

        combined_result = RunResult()
        for result in results:
            combined_result.tasks.extend(result.tasks)

        # sort tasks by timestamp
        combined_result.tasks.sort(key=lambda x: x.started_at)

        with open(self.output_file_path, mode="w", encoding="utf-8") as f:
            f.write(combined_result.model_dump_json(indent=2))

        logger.info("CombineResultsCommand finished")
