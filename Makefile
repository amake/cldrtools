LOCALES := ja ar it es de fr pt ru zh zh_Hant en ko
SRC_XML := $(LOCALES:%=vendor/cldr/common/main/%.xml)
CLDR := vendor/cldr
DIST_JSON := dist/cldr_city_names.json
DIST_TSV := dist/cldr_city_names.tsv

.PHONY: all
all: $(DIST_JSON) $(DIST_TSV)

vendor dist:
	mkdir -p $(@)

$(DIST_JSON): tzcity.py | dist $(CLDR)
	python tzcity.py json $(SRC_XML) > $(@)

$(DIST_TSV): tzcity.py | dist $(CLDR)
	python tzcity.py tsv $(SRC_XML) > $(@)

$(CLDR): | vendor
	cd vendor; git clone --depth 1 https://github.com/unicode-org/cldr.git
