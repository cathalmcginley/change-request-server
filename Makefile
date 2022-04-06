.PHONY: clean build

clean:
	find -name '*~' -delete
	find src -name __pycache__ -exec rm -rf '{}' '+'
	rm -rf src/witaker_clipboard_server.egg-info
	rm -rf dist

build:
	python3 -m build
