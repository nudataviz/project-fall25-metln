.PHONY: launch



Launch:

	@echo "Installing gender-guesser"
	npm install gender-guesser
	@echo "Launching Dashboard"
	cd Metln/src && npm run dev


