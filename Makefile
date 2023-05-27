install:
	pip3 install .

install-dev:
	pip3 install --editable .

uninstall:
	pip3 uninstall --yes 70mai-m300-toolbox

unit-test:
	python3 -W error -X dev -X tracemalloc -m unittest discover

clean:
	rm -rf *.egg-info build

docker-image:
	docker build --pull --no-cache --tag 70mai-m300-toolbox .
