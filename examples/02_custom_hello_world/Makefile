WORKFLOW_SCRIPT = custom_hello_world.py
RUN_OUTPUTS = run_outputs.txt
YW_FACTS = yw_extract_facts.P yw_model_facts.P
WORKFLOW_GRAPH = workflow_graph
DOTS = ${WORKFLOW_GRAPH}.gv
PNGS = ${WORKFLOW_GRAPH}.png
PDFS = ${WORKFLOW_GRAPH}.pdf
NW_FACTS = nw_facts.P
QUERY_OUTPUTS = query_outputs.txt
YW_PROPERTIES = yw.properties
QUERIES = run_queries.sh
RULES = ../rules/yw_rules.P ../rules/yw_nw_rules.P

FACTS = ${YW_FACTS} ${NW_FACTS}
ALL_OUTPUTS = ${RUN_OUTPUTS} ${FACTS} ${QUERY_OUTPUTS} ${DOTS} ${PNGS} ${PDFS}

all: ${ALL_OUTPUTS}
run: ${RUN_OUTPUTS}
yw: ${YW_FACTS}
nw: ${NW_FACTS}
png: ${PNGS}
pdf: ${PDFS}
query: ${QUERY_OUTPUTS}

${YW_FACTS}: ${WORKFLOW_SCRIPT} ${YW_PROPERTIES}
	bash -lc "yw graph ${WORKFLOW_SCRIPT} > ${WORKFLOW_GRAPH}.gv"

${RUN_OUTPUTS}: ${WORKFLOW_SCRIPT}
	now run -e Tracer ${WORKFLOW_SCRIPT} &> ${RUN_OUTPUTS}

${NW_FACTS}: ${RUN_OUTPUTS}
	now export -m dependency | grep -v 'environment(' > ${NW_FACTS}

${QUERY_OUTPUTS}: ${QUERIES} ${YW_FACTS} ${NW_FACTS} ${RULES}
	./run_queries.sh &> ${QUERY_OUTPUTS}

${PNGS}: ${QUERY_OUTPUTS}
	dot -Tpng ${WORKFLOW_GRAPH}.gv -o ${WORKFLOW_GRAPH}.png

${PDFS}: ${QUERY_OUTPUTS}
		dot -Tpdf ${WORKFLOW_GRAPH}.gv -o ${WORKFLOW_GRAPH}.pdf

clean:
	rm -f *.xwam ${ALL_OUTPUTS}
	rm -rf .noworkflow
