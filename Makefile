DATE=$(shell date +%I:%M%p)
CHECK=\033[32m✔\033[39m
HR=\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#

build:
	@$(MAKE) -C assets
	@$(MAKE) collectstatic

app:
	@$(MAKE) -C assets app
	@$(MAKE) collectstatic

collectstatic:
	@python manage.py collectstatic --noinput > /dev/null
	@echo "${CHECK} Static files collected."
