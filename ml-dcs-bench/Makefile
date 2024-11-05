INPUT_DIR				= ./tmp/testcases
OUTPUT_BASE_DIR			= ./tmp/mtsa/output
LOG_BASE_DIR			= ./tmp/mtsa/log
SLEEP_TIME				= 20
MTSA_JAR_PATH			= ./tmp/mtsa/mtsa-PCS_MachineLearning_v0.2.3.jar
MEMORY_SIZE				= 20
MTSA_COMMAND			= compose
MTSA_TARGET				= TraditionalController
MTSA_RESULT_MODE		= for-machine-learning-extra
ML_DCS_BENCH_BIN_PATH	= ./tmp/ml-dcs-bench

debug:
	pipenv run python main.py run \
		--input-dir $(INPUT_DIR) \
		--output-base-dir $(OUTPUT_BASE_DIR) \
		--log-base-dir $(LOG_BASE_DIR) \
		--sleep-time $(SLEEP_TIME) \
		--mtsa-jar-path $(MTSA_JAR_PATH) \
		--memory-size $(MEMORY_SIZE) \
		--mtsa-command $(MTSA_COMMAND) \
		--mtsa-target $(MTSA_TARGET) \
		--mtsa-result-mode $(MTSA_RESULT_MODE)
run:
	$(ML_DCS_BENCH_BIN_PATH) run \
		--input-dir $(INPUT_DIR) \
		--output-base-dir $(OUTPUT_BASE_DIR) \
		--log-base-dir $(LOG_BASE_DIR) \
		--sleep-time $(SLEEP_TIME) \
		--mtsa-jar-path $(MTSA_JAR_PATH) \
		--memory-size $(MEMORY_SIZE) \
		--mtsa-command $(MTSA_COMMAND) \
		--mtsa-target $(MTSA_TARGET) \
		--mtsa-result-mode $(MTSA_RESULT_MODE)
create:
	pipenv run python main.py create_testcases -O
combine:
	pipenv run python main.py combine_results \
		--results-dir $(OUTPUT_BASE_DIR) \
		--output "./tmp/combined-result.json"
