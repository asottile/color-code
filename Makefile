.PHONY: all demo
all: color_code.py

venv:
	virtualenv venv -ppython2.7
	venv/bin/pip install yelp-cheetah

%.py: %.tmpl venv
	venv/bin/cheetah-compile $<

.PHONY: clean
clean:
	rm -rf venv color_code.py *.pyc
