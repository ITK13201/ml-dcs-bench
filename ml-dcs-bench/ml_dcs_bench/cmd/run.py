import argparse
import datetime
import glob
import os.path
import subprocess
import time
from logging import getLogger

from ml_dcs_bench.cmd.base import BaseCommand
from ml_dcs_bench.domain.result import RunResult, RunResultTask

logger = getLogger(__name__)

# LTS_NAMES = [
#     "ArtGallery（N, 2 room）",
#     "ArtGallery（N, 3 room）",
#     "ArtGallery（N, 4 room）",
#     "ArtGallery（N, 5 room）",
#     "ArtGallery（N, 6 room）",
#     "ArtGallery（N, 7 room）",
#     "ArtGallery（N, 8 room）",
#     "ArtGallery（N, 9 room）",
#     "ArtGallery（N, 10 room）",
#     "ArtGallery（S, 5 people）",
#     "ArtGallery（S, 6 people）",
#     "ArtGallery（S, 7 people）",
#     "ArtGallery（S, 8 people）",
#     "ArtGallery（S, 9 people）",
#     "ArtGallery（S, 10 people）",
#     "AT（2, 2）",
#     "AT（2, 3）",
#     "AT（2, 4）",
#     "AT（2, 5）",
#     "AT（3, 3）",
#     "AT（3, 4）",
#     "AT（3, 5）",
#     "AT（4, 4）",
#     "AT（4, 5）",
#     "AT（5, 5）",
#     "AT（5, 10）",
#     "BW（2, 2）",
#     "BW（2, 3）",
#     "BW（2, 4）",
#     "BW（2, 5）",
#     "BW（3, 2）",
#     "BW（3, 3）",
#     "BW（3, 4）",
#     "BW（3, 5）",
#     "BW（4, 2）",
#     "BW（4, 3）",
#     "BW（4, 4）",
#     "BW（4, 5）",
#     "BW（5, 2）",
#     "BW（5, 3）",
#     "BW（5, 4）",
#     "BW（5, 5）",
#     "CM（2, 2）",
#     "CM（2, 3）",
#     "CM（2, 4）",
#     "CM（2, 5）",
#     "CM（3, 2）",
#     "CM（3, 3）",
#     "CM（3, 4）",
#     "CM（3, 5）",
#     "CM（4, 2）",
#     "CM（4, 3）",
#     "CM（4, 4）",
#     "CM（4, 5）",
#     "CM（5, 2）",
#     "CM（5, 3）",
#     "CM（5, 4）",
#     "CM（5, 5）",
#     "KIVA_system（N, 2 robot）",
#     "KIVA_system（N, 3 robot）",
#     "KIVA_system（N, 4 robot）",
#     "KIVA_system（S, 5 pod）",
#     "KIVA_system（S, 10 pod）",
#     "KIVA_system（S, 20 pod）",
#     "KIVA_system（S, 30 pod）",
# ]

# sorted by execute duration
LTS_NAMES = [
    # AT (all)
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
    # BW (all)
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
    # CM
    "CM（2, 2）",
    "CM（2, 3）",
    "CM（2, 4）",
    "CM（2, 5）",
    "CM（3, 2）",
    "CM（3, 3）",
    # ArtGallery
    "ArtGallery（N, 2 room）",
    "ArtGallery（N, 3 room）",
    "ArtGallery（N, 4 room）",
    "ArtGallery（S, 5 people）",
    "ArtGallery（S, 6 people）",
    # KiVA_system
    "KIVA_system（N, 2 robot）",
    "KIVA_system（N, 3 robot）",
    "KIVA_system（N, 4 robot）",
    "KIVA_system（S, 5 pod）",
    "KIVA_system（S, 10 pod）",
    # Succeeded but log duration
    "CM（3, 4）",
    "ArtGallery（N, 5 room）",
    "KIVA_system（S, 20 pod）",
    # Failed
    "CM（3, 5）",
    "CM（4, 2）",
    "CM（4, 3）",
    "CM（4, 4）",
    "CM（4, 5）",
    "CM（5, 2）",
    "CM（5, 3）",
    "CM（5, 4）",
    "CM（5, 5）",
    "ArtGallery（N, 6 room）",
    "ArtGallery（N, 7 room）",
    "ArtGallery（N, 8 room）",
    "ArtGallery（N, 9 room）",
    "ArtGallery（N, 10 room）",
    "ArtGallery（S, 7 people）",
    "ArtGallery（S, 8 people）",
    "ArtGallery（S, 9 people）",
    "ArtGallery（S, 10 people）",
    "KIVA_system（S, 30 pod）",
]


class RunCommand(BaseCommand):
    name = "run"
    help = "run DCS with MTSA"

    def add_arguments(self, parser: argparse.ArgumentParser):
        # arguments for its own
        parser.add_argument(
            "-i",
            "--input-dir",
            type=str,
            required=True,
            help="Input directory",
        )
        parser.add_argument(
            "-o",
            "--output-base-dir",
            type=str,
            required=True,
            help="Output base directory",
        )
        parser.add_argument(
            "-l",
            "--log-base-dir",
            type=str,
            required=True,
            help="Log base directory",
        )
        parser.add_argument(
            "-s",
            "--sleep-time",
            type=int,
            required=False,
            help="Sleep time in seconds",
            default=10,
        )

        # Java arguments
        parser.add_argument(
            "-j",
            "--mtsa-jar-path",
            type=str,
            required=True,
            help="MTSA jar path",
        )
        parser.add_argument(
            "-m",
            "--memory-size",
            type=int,
            required=False,
            help="Memory size (GB)",
            default=225,
        )

        # MTSA arguments
        parser.add_argument(
            "-t",
            "--mtsa-target",
            type=str,
            required=False,
            help="MTSA Target name",
            default="TraditionalController",
        )

    def __init__(self):
        super().__init__()

        # CLI arguments
        self.input_dir = ""
        self.output_base_dir: str = ""
        self.log_base_dir: str = ""
        self.sleep_time: int = -1
        self.mtsa_jar_path: str = ""
        self.memory_size: int = -1
        self.mtsa_target: str = ""

        # others
        self.output_dir = ""
        self.log_dir = ""
        self.result = RunResult()

    def execute(self, args: argparse.Namespace):
        logger.info("RunCommand started")

        self.input_dir = args.input_dir
        self.output_base_dir = args.output_base_dir
        self.log_base_dir = args.log_base_dir
        self.sleep_time = args.sleep_time
        self.mtsa_jar_path = args.mtsa_jar_path
        self.memory_size = args.memory_size
        self.mtsa_target = args.mtsa_target

        now = datetime.datetime.now()
        self.output_dir = os.path.join(
            self.output_base_dir, now.strftime("%Y%m%d-%H%M%S")
        )
        self.log_dir = os.path.join(self.log_base_dir, now.strftime("%Y%m%d-%H%M%S"))

        # create dirs
        os.mkdir(self.output_dir)
        os.mkdir(self.log_dir)

        self.result.started_at = now

        for lts_name in LTS_NAMES:
            lts_file_paths = glob.glob(
                os.path.join(self.input_dir, "{}*.lts".format(lts_name)), recursive=True
            )

            for lts_file_path in lts_file_paths:
                logger.info("Started to execute: {}".format(lts_file_path))

                lts_file_basename = os.path.splitext(os.path.basename(lts_file_path))[0]

                now = datetime.datetime.now()
                task_result = RunResultTask(name=lts_file_basename, started_at=now)

                log_file_path = os.path.join(
                    self.log_dir,
                    lts_file_basename + ".log",
                )
                with open(log_file_path, "w") as log_file:
                    process = subprocess.run(
                        [
                            "java",
                            "-Xmx{}G".format(args.memory_size),
                            "-jar",
                            args.mtsa_jar_path,
                            "-f",
                            lts_file_path,
                            "-t",
                            args.mtsa_target,
                            "-o",
                            self.output_dir,
                        ],
                        stdout=log_file,
                        stderr=log_file,
                    )

                now = datetime.datetime.now()
                task_result.finished_at = now

                if process.returncode == 0:
                    task_result.success = True
                    logger.info("Finished to execute: {}".format(lts_file_path))
                else:
                    task_result.success = False
                    logger.error("Failed to execute: {}".format(lts_file_path))

                self.result.tasks.append(task_result)

                # sleep
                time.sleep(self.sleep_time)

        now = datetime.datetime.now()
        self.result.finished_at = now

        result_json = self.result.model_dump_json(indent=2)
        with open(
            os.path.join(
                self.output_base_dir,
                "result_{}.json".format(
                    self.result.started_at.strftime("%Y%m%d-%H%M%S")
                ),
            ),
            "w",
        ) as f:
            f.write(result_json)

        logger.info("RunCommand finished")
