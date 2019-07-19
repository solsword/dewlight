DATA_DIR := "data"
OUT_DIR := "out"

TSVS := $(shell find ${DATA_DIR} -name "*.tsv")
BUNDLES := $(shell \
	find ${DATA_DIR} -name "*.tsv" \
	| sed -e "s/\\.tsv/-bundle.html/g" \
	| sed -e "s/${DATA_DIR}/${OUT_DIR}/")

.PHONY: show
show:
	echo ${TSVS}
	echo ${BUNDLES}

.DEFAULT_GOAL := all
.PHONY: all
all: ${BUNDLES}

out/%-bundle.html: data/%-graph.json index.html help.html d3/d3.v4.min.js bundle.py
	./bundle.py $< index.html help.html $@

.PRECIOUS: data/%-graph.json
data/%-graph.json: data/%.tsv build_graph.py
	./build_graph.py $< $@

help.html: help.md
	pandoc -f markdown+smart $< --output=$@
