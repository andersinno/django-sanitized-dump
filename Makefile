test_args?=-v

test:
	python runtests.py $(test_args)

build:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

clean:
	rm -fr dist build *.egg-info .tox
