.PHONY: all
all: color_code.py

venv:
	virtualenv venv -ppython2.7 && . venv/bin/activate && pip install yelp-cheetah

color_code.py: venv color_code.tmpl
	. venv/bin/activate && cheetah-compile color_code.tmpl

.PHONY: clean
clean:
	rm -rf venv color_code.py *.pyc
