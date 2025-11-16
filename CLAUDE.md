# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ML-DCS-BENCH is a benchmark toolkit for [ML-DCS](https://github.com/ITK13201/ml-dcs/tree/master) (Machine Learning-based Discrete Controller Synthesis). The project:
- Generates test cases from LTS (Labeled Transition System) components using evaluation scenarios
- Runs controller synthesis benchmarks using MTSA (Modal Transition System Analyzer)
- Combines and analyzes benchmark results with timing and memory metrics
- Compiles to standalone executables for Windows, macOS, and Linux using Nuitka

## Development Setup

The main Python application is located in `ml-dcs-bench/` subdirectory.

**Install dependencies:**
```bash
cd ml-dcs-bench
pip install pipenv
pipenv install --dev
```

**Activate virtual environment:**
```bash
cd ml-dcs-bench
pipenv shell
```

## Commands

All commands are run from the `ml-dcs-bench/` directory.

**Run the application (via Python):**
```bash
pipenv run python main.py <command>
```

**Available commands:**
- `create_testcases` - Generate test cases from LTS components
- `run` - Execute MTSA benchmarks
- `combine_results` - Combine multiple result files

**Code formatting:**
```bash
pipenv run black .
pipenv run isort .
```

**Using Makefile shortcuts:**
```bash
# Create testcases (overwrites existing)
make create

# Run benchmarks in debug mode (via Python)
make debug

# Run benchmarks via compiled binary
make run

# Combine results
make combine
```

Note: The Makefile assumes certain paths exist (like `./tmp/testcases`, `./tmp/mtsa/mtsa-PCS_MachineLearning_v0.2.3.jar`). Review `ml-dcs-bench/Makefile` for configuration variables.

## Architecture

**Command Pattern:** The CLI uses a command pattern with subcommands:
- `RootCommand` (ml_dcs_bench/cmd/root.py) - Main CLI entry point, registers subcommands
- `BaseCommand` (ml_dcs_bench/cmd/base.py) - Abstract base for commands
- `CreateTestCasesCommand` (ml_dcs_bench/cmd/create_testcases.py) - Generates test cases
- `RunCommand` (ml_dcs_bench/cmd/run.py) - Executes MTSA benchmarks
- `CombineResultsCommand` (ml_dcs_bench/cmd/combine_results.py) - Merges result files

**Domain Models:**
- `ControllerSpec` (ml_dcs_bench/domain/lts.py) - Models controller specifications (safety properties, controllable actions, marking, nonblocking)
- `RunResult` and `RunResultTask` (ml_dcs_bench/domain/result.py) - Models benchmark execution results with timing and memory metrics

**Test Case Generation:**
The `create_testcases` command generates benchmark test cases by:
1. Loading LTS components from `ml-dcs-bench/assets/lts-components/<component-name>/`:
   - `models.lts` - LTS model definitions (environment models)
   - `cspec.yaml` - Controller specification (safety properties/monitoring models, controllable actions, etc.)
   - `targets.lts` - Target specifications
2. Creating powerset combinations of safety properties (or random sampling if >200 combinations)
3. Outputting `.lts` files combining models + modified controller spec + targets

**Evaluation Scenarios:**
Five benchmark scenarios are used, each with parameters N (number of environment models) and K (states per model):
- **ArtGallery (Headcount Control)**: Room access control based on occupancy
- **AT (Air Traffic)**: Aircraft landing coordination without collisions
- **BW (Bidding Workflow)**: Application approval system with審査teams
- **CM (Cat and Mouse)**: Capture robot system in restricted area
- **KIVA_system**: Warehouse robot system (Amazon Robotics-based)

**Benchmark Execution:**
The `run` command:
1. Processes each LTS file through MTSA via Java subprocess
2. Monitors memory usage during execution (tracks OS memory delta)
3. Captures stdout/stderr to log files
4. Records timing, success/failure, and memory metrics
5. Outputs individual result JSON files with task details
6. Supports resuming from a specific test case via `--skip-to`

**Result Aggregation:**
The `combine_results` command merges multiple result JSON files, sorting tasks by start time.

## Build and Release

**Build process:** Configured via `.github/workflows/release.yaml`
- Triggered on version tags (v*)
- Uses Nuitka to compile Python to native executables
- Builds for Windows, macOS, and Linux
- Creates GitHub releases with compressed binaries

**Python version:** 3.12

**Key dependencies:**
- pyyaml - LTS component parsing
- pydantic - Data validation and serialization
- psutil - Memory monitoring

## Code Style

- Python code follows Black formatting (line length: 88)
- Import sorting via isort (Black-compatible profile)
- No trailing newlines are missing in files
