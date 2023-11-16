.PHONY: zip
zip:
	cd functions/report_to_smartsheet && zip ReportToSmartsheet.zip ReportToSmartsheet.py

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