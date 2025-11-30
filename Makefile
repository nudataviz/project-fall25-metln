.PHONY: launch



Launch:

	@echo "Installing gender-guesser"
	npm install gender-detection-from-name
	cd METLN/src && npm install
	@echo "Launching Dashboard"
	cd METLN/src && npm run dev


