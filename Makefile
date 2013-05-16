DATE=$(shell date +%I:%M%p)
#CHECK=\033[32m✔\033[39m
CHECK=✔
HR=\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#
PATH:=.Dienstensysteem/bin:/usr/local/bin:/usr/local/share/npm/bin:$(PATH)

build:
	@$(MAKE) -C assets app
	@$(MAKE) collectstatic

all:
	@$(MAKE) -C assets
	@$(MAKE) collectstatic

collectstatic:
	@./manage.py collectstatic --noinput > /dev/null
	@echo "${CHECK} Static files collected."
