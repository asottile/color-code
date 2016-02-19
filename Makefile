.PHONY: all
all: ./color_code.py

venv:
	virtualenv venv -ppython2.7 && . venv/bin/activate && pip install yelp-cheetah

./%.py: %.tmpl venv
	. venv/bin/activate && cheetah-compile $^

.PHONY: clean
clean:
	rm -rf venv color_code.py *.pyc
