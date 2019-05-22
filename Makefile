LOCALES := ja ar it es de fr pt ru zh zh_Hant en ko
SRC_XML := $(LOCALES:%=vendor/cldr/common/main/%.xml)
CLDR := vendor/cldr
CITY_JSON := dist/cldr_city_names.json
CITY_TSV := dist/cldr_city_names.tsv

.PHONY: all
all: $(CITY_JSON) $(CITY_TSV)

vendor dist:
	mkdir -p $(@)

.env:
	virtualenv $(@)
	$(@)/bin/pip install -e .

$(CITY_JSON): tzcity.py | dist $(CLDR) .env
	python tzcity.py json $(SRC_XML) > $(@)

$(CITY_TSV): tzcity.py | dist $(CLDR) .env
	python tzcity.py tsv $(SRC_XML) > $(@)

$(CLDR): | vendor
	cd vendor; git clone --depth 1 https://github.com/unicode-org/cldr.git
