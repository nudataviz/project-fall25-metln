.PHONY: launch



Launch:

	@echo "Installing gender-guesser"
	npm install gender-guesser
	@echo "Launching Dashboard"
	cd METLN/src && npm run dev


