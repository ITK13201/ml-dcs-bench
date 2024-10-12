INPUT_DIR		= ./tmp/testcases
OUTPUT_BASE_DIR	= ./tmp/mtsa/output
LOG_BASE_DIR	= ./tmp/mtsa/log
SLEEP_TIME		= 20
MTSA_JAR_PATH	= ./tmp/mtsa/mtsa-PCS_MachineLearning_v0.2.0.jar
MEMORY_SIZE		= 20
MTSA_TARGET	= TraditionalController
ML_DCS_BENCH_BIN_PATH = ./tmp/ml-dcs-bench

debug:
	pipenv run python main.py run \
		--input-dir $(INPUT_DIR) \
		--output-base-dir $(OUTPUT_BASE_DIR) \
		--log-base-dir $(LOG_BASE_DIR) \
		--sleep-time $(SLEEP_TIME) \
		--mtsa-jar-path $(MTSA_JAR_PATH) \
		--memory-size $(MEMORY_SIZE) \
		--mtsa-target $(MTSA_TARGET)
run:
	$(ML_DCS_BENCH_BIN_PATH) run \
		--input-dir $(INPUT_DIR) \
		--output-base-dir $(OUTPUT_BASE_DIR) \
		--log-base-dir $(LOG_BASE_DIR) \
		--sleep-time $(SLEEP_TIME) \
		--mtsa-jar-path $(MTSA_JAR_PATH) \
		--memory-size $(MEMORY_SIZE) \
		--mtsa-target $(MTSA_TARGET)
create:
	pipenv run python main.py create_testcases -O
