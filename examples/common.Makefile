
RULES_DIR = ../../rules
GRAPH_RULES_DIR = ../../graphs

YW_EXTRACT_FACTS = facts/yw_extract_facts.P
YW_MODEL_FACTS = facts/yw_model_facts.P
YW_FACTS = ${YW_EXTRACT_FACTS} ${YW_MODEL_FACTS}
YW_VIEWS = yw_views.P
YW_MODEL_OPTIONS = -c extract.language=python \
                   -c extract.factsfile=${YW_EXTRACT_FACTS} \
                   -c model.factsfile=${YW_MODEL_FACTS} \
                   -c query.engine=xsb

NW_FACTS = facts/nw_facts.P
NW_VIEWS = nw_views.P

YW_NW_VIEWS = yw_nw_views.P

RUN_SCRIPT = run.sh
RUN_STDOUT = run_outputs.txt
RUN_OUTPUTS = ${RUN_STDOUT}

RULES = ${RULES_DIR}/nw_views.P ${RULES_DIR}/yw_views.P ${RULES_DIR}/yw_nw_views.P
QUERY_SCRIPT = query.sh
QUERY_OUTPUTS = query_outputs.txt

YW_DATA_GRAPH = yw_data_graph
YW_PROCESS_GRAPH = yw_process_graph
YW_COMBINED_GRAPH = yw_combined_graph
YW_PROSPECTIVE_LINEAGE_GRAPH = yw_prospective_lineage
YW_NW_RETROSPECTIVE_LINEAGE_GRAPH = yw_nw_retrospective_lineage

YW_GRAPHS = ${YW_DATA_GRAPH}.gv \
            ${YW_PROCESS_GRAPH}.gv \
	        ${YW_COMBINED_GRAPH}.gv \
	        ${YW_PROSPECTIVE_LINEAGE_GRAPH}.gv

YW_NW_GRAPHS = ${YW_NW_RETROSPECTIVE_LINEAGE_GRAPH}.gv

GRAPHS = ${YW_GRAPHS} ${YW_NW_GRAPHS}
PNGS = ${GRAPHS:.gv=.png}
PDFS = ${GRAPHS:.gv=.pdf}

all: ${QUERY_OUTPUTS} ${GRAPHS} ${PNGS} ${PDFS}
run: ${RUN_OUTPUTS}
yw: ${YW_FACTS} ${YW_VIEWS} ${YW_GRAPHS}
nw: ${NW_FACTS} ${NW_VIEWS} ${NW_GRAPHS}
ywnw: ${YW_NW_VIEWS} ${YW_NW_GRAPHS}
query: ${QUERY_OUTPUTS}
graph: ${GRAPHS}
png: ${PNGS}
pdf: ${PDFS}

.SUFFIXES:
.SUFFIXES: .gv .pdf .png

.gv.pdf:
	dot -Tpdf $*.gv -o $*.pdf

.gv.png:
	dot -Tpng $*.gv -o $*.png

ifdef DATA
RETROSPECTIVE_LINEAGE_DATA = $(DATA)
PROSPECTIVE_LINEAGE_DATA = $(DATA)
.PHONY: ${YW_NW_RETROSPECTIVE_LINEAGE_GRAPH}.gv \
        ${YW_PROSPECTIVE_LINEAGE_GRAPH}.gv
endif

ifdef VALUE
RETROSPECTIVE_LINEAGE_VALUE= "$(VALUE)"
.PHONY: ${YW_NW_RETROSPECTIVE_LINEAGE_GRAPH}.gv
endif

${YW_FACTS}: ${WORKFLOW_SCRIPT}
ifdef YW_JAR
	mkdir -p facts
	java -jar ${YW_JAR} model ${WORKFLOW_SCRIPT} ${YW_MODEL_OPTIONS}
else
	$(error Must set YW_JAR environment variable to path to YesWorkflow jar)
endif

${YW_VIEWS}: ${YW_FACTS}
	bash ${RULES_DIR}/materialize_yw_views.sh > ${YW_VIEWS}

${RUN_OUTPUTS}: ${RUN_SCRIPT} ${WORKFLOW_SCRIPT}
	bash ${RUN_SCRIPT} > ${RUN_STDOUT}

${NW_FACTS}: ${RUN_OUTPUTS}
	mkdir -p facts
	now export -t -m dependency | grep -v 'environment(' > ${NW_FACTS}

${NW_VIEWS}: ${NW_FACTS}
	bash ${RULES_DIR}/materialize_nw_views.sh > ${NW_VIEWS}

${YW_NW_VIEWS}: ${YW_VIEWS} ${NW_VIEWS}
	bash ${RULES_DIR}/materialize_yw_nw_views.sh > ${YW_NW_VIEWS}

${YW_DATA_GRAPH}.gv: ${YW_VIEWS}
	bash ../../graphs/${YW_DATA_GRAPH}.sh > ${YW_DATA_GRAPH}.gv

${YW_PROCESS_GRAPH}.gv: ${YW_VIEWS}
	bash ../../graphs/${YW_PROCESS_GRAPH}.sh > ${YW_PROCESS_GRAPH}.gv

${YW_COMBINED_GRAPH}.gv: ${YW_VIEWS}
	bash ../../graphs/${YW_COMBINED_GRAPH}.sh > ${YW_COMBINED_GRAPH}.gv

${YW_PROSPECTIVE_LINEAGE_GRAPH}.gv: ${YW_VIEWS}
	bash ../../graphs/${YW_PROSPECTIVE_LINEAGE_GRAPH}.sh \
		${PROSPECTIVE_LINEAGE_DATA} \
		> ${YW_PROSPECTIVE_LINEAGE_GRAPH}.gv

${YW_NW_RETROSPECTIVE_LINEAGE_GRAPH}.gv : ${YW_NW_VIEWS}
	bash ../../graphs/${YW_NW_RETROSPECTIVE_LINEAGE_GRAPH}.sh \
		${RETROSPECTIVE_LINEAGE_DATA} ${RETROSPECTIVE_LINEAGE_VALUE} \
		> ${YW_NW_RETROSPECTIVE_LINEAGE_GRAPH}.gv

${QUERY_OUTPUTS}: ${QUERY_SCRIPT} ${YW_VIEWS} ${NW_VIEWS} ${YW_NW_VIEWS} ${RULES}
	bash ${QUERY_SCRIPT} > ${QUERY_OUTPUTS}

clean:
	rm -rf facts .noworkflow *.xwam *.gv *.png *.pdf *.P *.txt ${RULES_DIR}/*.xwam

repl: ${YW_NW_VIEWS}
	expect ../../rules/start_xsb.exp
