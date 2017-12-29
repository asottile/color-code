.PHONY: all demo
all: color_code.py index.py

venv:
	virtualenv venv -ppython3.6
	venv/bin/pip install yelp-cheetah

%.py: %.tmpl venv
	venv/bin/cheetah-compile $<

.PHONY: clean
clean:
	rm -rf venv color_code.py *.pyc
