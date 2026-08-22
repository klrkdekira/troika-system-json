.PHONY: help bundle llms llms-full search-index collection-index sitemap publish test validate check

UV ?= uv
UV_CACHE_DIR ?= /tmp/troika-system-json-uv-cache
PYTHON = UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) run python

help:
	@echo "Available targets:"
	@echo "  bundle           Build the single-file corpus and sync context.jsonld"
	@echo "  llms             Regenerate llms.txt"
	@echo "  llms-full        Regenerate llms-full.txt"
	@echo "  search-index     Regenerate objects/search-index.json"
	@echo "  collection-index Regenerate objects/collection-index.json"
	@echo "  sitemap          Regenerate sitemap.xml"
	@echo "  publish          Build every publishing artifact"
	@echo "  test             Run the unit test suite"
	@echo "  validate         Validate objects and references"
	@echo "  check            Build publishing artifacts, validate, and test"

bundle:
	$(PYTHON) scripts/generate_indexes.py

llms:
	$(PYTHON) scripts/build_llms.py --root .

llms-full:
	$(PYTHON) scripts/build_llms_full.py --root .

search-index:
	$(PYTHON) scripts/build_search_index.py --root .

collection-index:
	$(PYTHON) scripts/build_collection_index.py --root .

sitemap:
	$(PYTHON) scripts/build_sitemap.py --root .

publish: bundle llms llms-full search-index collection-index sitemap

test:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) main.py
	$(PYTHON) main.py objects --check-references

check: publish validate test
