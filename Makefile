.PHONY: zip
zip:
	cd functions/report_to_smartsheet/
	zip ReportToSmartsheet.zip ReportToSmartsheet.py
	mkdir functions/report_to_smartsheet/smartsheet
	pip3 install smartsheet-python-sdk -t functions/report_to_smartsheet/smartsheet
	zip -r smartsheet.zip /smartsheet
	cd ../../
	rm -rf functions/report_to_smartsheet/smartsheet
	rmdir functions/report_to_smartsheet/smartsheet

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