DATA_DIR := "data"
OUT_DIR := "out"

TSVS := $(shell ls ${DATA_DIR} | grep ".tsv$$")
BUNDLES := $(\
	shell ls ${DATA_DIR} \
	| grep ".tsv$$" \
	| sed "s/\\.tsv/-bundle.html/g" \
	| sed "s/${DATA_DIR}/${OUT_DIR}/")

DEFAULT_GOAL := all
.PHONY: all
all: ${BUNDLES}

out/%-bundle.html: data/%-graph.json index.html d3/d3.v4.min.js
	./bundle.py $< index.html $@

data/%-graph.json: data/%.tsv build_graph.py
	./build_graph.py $< $@
