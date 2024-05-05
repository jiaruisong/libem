.PHONY: dist install
dist:
	python setup.py sdist bdist_wheel && twine upload --skip-existing dist/*
	rm -rf build dist *.egg-info
install:
	pip install -e . && rm -rf *.egg-info
	mkdir -p ~/.libem && touch ~/.libem/config.yaml


# examples
.PHONY: run match browse chat all
run: | match
match:
	python examples/match.py
browse:
	python examples/browse.py
chat:
	python examples/chat.py
all: | run browse chat

# benchmarks
.PHONY: product benchmark
product:
	python benchmark/product.py


# test
.PHONY: test
test: | all