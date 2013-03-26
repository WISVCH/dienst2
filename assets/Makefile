DATE=$(shell date +%I:%M%p)
CHECK=\033[32m✔\033[39m
HR=\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#
DIENST2=../dienst2/static
LDB=../ldb/static
KAS=../kas/static
POST=../post/static

build: bootstrap app

bootstrap:
	@recess --compile  less/bootstrap.less > $(DIENST2)/css/bootstrap.css
	@recess --compress less/bootstrap.less > $(DIENST2)/css/bootstrap.min.css
	@recess --compile  less/bootstrap-responsive.less > $(DIENST2)/css/bootstrap-responsive.css
	@recess --compress less/bootstrap-responsive.less > $(DIENST2)/css/bootstrap-responsive.min.css

	@echo "${CHECK} Compiled and Minified Boostrap LESS"

#@coffee --join js/app.js --bare --compile coffee/app.coffee coffee/services.coffee coffee/controllers.coffee coffee/filters.coffee coffee/directives.coffee
#@uglifyjs js/app.js -nc > js/app.min.js
#@coffee --compile --output js/ coffee/

app: dienst2 ldb kas post
	@echo "${CHECK} Compiled assets"

dienst2:
	@coffee --join ${DIENST2}/js/dienst2.js --compile coffee/dienst2.coffee coffee/spin.coffee
	@uglifyjs ${DIENST2}/js/dienst2.js -nc > ${DIENST2}/js/dienst2.min.js 2> /dev/null
	@echo "${CHECK} Compiled and Minified Dienst2 assets"

ldb:
	@coffee --join ${LDB}/js/ldb.js --compile coffee/ldb.coffee
	@uglifyjs ${LDB}/js/ldb.js -nc > ${LDB}/js/ldb.min.js 2> /dev/null
	@echo "${CHECK} Compiled and Minified ldb assets"

kas:
	@coffee --join ${KAS}/js/kas.js --compile coffee/kas.coffee
	@uglifyjs ${KAS}/js/kas.js -nc > ${KAS}/js/kas.min.js 2> /dev/null
	@echo "${CHECK} Compiled and Minified kas assets"

post:
	@coffee --join ${POST}/js/post.js --compile coffee/post.coffee
	@uglifyjs ${POST}/js/post.js -nc > ${POST}/js/post.min.js 2> /dev/null
	@echo "${CHECK} Compiled and Minified post assets"
