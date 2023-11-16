.PHONY: zip
zip:
	cd functions/report_to_smartsheet/ && zip ReportToSmartsheet.zip ReportToSmartsheet.py
	cd ../../
	mkdir packages && cd packages && python3 -m venv venv && source venv/bin/activate && mkdir python && cd python && pip3 install smartsheet-python-sdk -t . && cd .. && zip -r smartsheet.zip python && mv smartsheet.zip ../functions/report_to_smartsheet/smartsheet.zip && cd .. && rm -rf packages 


.PHONY: init
init:
	terraform init

.PHONY: validate
validate: init
	terraform validate

.PHONY: fmt
fmt:
	terraform fmt

.PHONY: lint
lint:
	tflint

.PHONY: test
test: init validate fmt lint