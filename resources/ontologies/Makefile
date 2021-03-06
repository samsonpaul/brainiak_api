NEW_PYTHONPATH="`pwd`/src:$(PYTHONPATH)"

USER=dba
PWD=dba
VIRTUOSO_HOST=localhost

help:
	@echo "Usage: make <command>"
	@echo "List of commands:"
	@echo "  setup                      -- Install project dependencies"
	@echo "  deploy GRAPH=graph ENV=env -- DEPRECATED" # Deploy <graph> ontology (person, place, upper) to <env> (local, dev, qa1)
	@echo "  reset_ontologies           -- Clear all graphs and reload ontologies based on ttl definitions"
	@echo "  load_mappings              -- Execute mapping and load instances into their respective graphs"
	@echo "  reset_all                  -- Run <reset_all_ontologies> and then <deploy_instances>"

setup:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

deploy: setup
	@echo Deploying graph $(GRAPH) to enviroment $(ENV)
	@# example:
	@# make deploy GRAPH=upper ENV=local
	@# make deploy GRAPH=person ENV=dev
	export MIGRATE_DB=$(ENV);\
	export MIGRATE_GRAPH=$(GRAPH);\
	virtuoso-migrate -c config/deploy_settings.py
	@# Note: settings.py file access MIGRATE_DB and MIGRATE_GRAPH
	@# enviroment variables and define parameters needed by
	@# virtuoso-MIGRATE_DB
 
create_all:
	@echo Creating the graphs
	isql $(VIRTUOSO_HOST) $(USER) $(PWD) ./scripts/create_graphs.isql

reset_ontologies: test_env
	@echo Erasing and reloading ontologies
	python scripts/prefixes2isql.py schema > /tmp/prefixes.isql
	isql $(VIRTUOSO_HOST) $(USER) $(PWD) /tmp/prefixes.isql
	cp schema/*.ttl "$(VIRTUOSO_HOME)/dumps/"
	cp schema/*.ttl.graph "$(VIRTUOSO_HOME)/dumps/"
	isql $(VIRTUOSO_HOST) $(USER) $(PWD)  ./scripts/load_new_ontologies.isql

load_mappings: test_env
	@echo Generating and loading instance mappings
	@cd scripts; ./load_instance_mappings.sh
	isql $(VIRTUOSO_HOST) $(USER) $(PWD) ./scripts/invert_uri.isql

reset_all: reset_ontologies load_mappings

test_env:
	@if test "$VIRTUOSO_HOME" = "" ; then \
		echo "Need to set VIRTUOSO_HOME, e.g. /usr/local/virtuoso-opensource/ "; \
		exit 1; \
	fi

validate:
	@echo "\nRunning validation"
	export PYTHONPATH="`pwd`/validation:$(PYTHONPATH)"; nosetests -v -s  --tests=tests/validation --with-xunit

