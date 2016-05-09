
RULES_DIR = ../../rules
RUN_STDOUT = run_outputs.txt
RUN_PRODUCTS =  ${RUN_STDOUT}
YW_VIEWS = yw_views.P
NW_VIEWS = nw_views.P
RULES = ${RULES_DIR}/yw_rules.P ${RULES_DIR}/yw_nw_rules.P ${RULES_DIR}/yw_view_rules.P
QUERY_SCRIPT = run_queries.sh
QUERY_OUTPUTS = query_outputs.txt
NW_FACTS = nw_facts.P

WORKFLOW_GRAPH = workflow_graph
DOTS = ${WORKFLOW_GRAPH}.gv
PNGS = ${WORKFLOW_GRAPH}.png
PDFS = ${WORKFLOW_GRAPH}.pdf

YW_PROPERTIES = yw.properties

all: ${QUERY_OUTPUTS} ${DOTS} ${PNGS} ${PDFS}

run: ${RUN_PRODUCTS}
yw: ${YW_VIEWS}
nw: ${NW_FACTS}
query: ${QUERY_OUTPUTS}
dots: ${DOTS}
png: ${PNGS}
pdf: ${PDFS}

${RUN_PRODUCTS}: ${WORKFLOW_SCRIPT}
	now run -e Tracer ${WORKFLOW_SCRIPT} > ${RUN_STDOUT}

${YW_VIEWS}: ${WORKFLOW_SCRIPT} ${YW_PROPERTIES}
	bash -lc "yw graph ${WORKFLOW_SCRIPT} > ${WORKFLOW_GRAPH}.gv"
	${RULES_DIR}/materialize_yw_views.sh > ${YW_VIEWS}
	rm -f yw_extract_facts.* yw_model_facts.*

${NW_FACTS}: ${RUN_PRODUCTS}
	now export -t -m dependency | grep -v 'environment(' > ${NW_FACTS}
	${RULES_DIR}/materialize_nw_views.sh &> ${NW_VIEWS}

${QUERY_OUTPUTS}: ${QUERY_SCRIPT} ${YW_VIEWS} ${NW_FACTS} ${RULES}
	./run_queries.sh &> ${QUERY_OUTPUTS}

${PNGS}: ${WORKFLOW_GRAPH}.gv
	dot -Tpng ${WORKFLOW_GRAPH}.gv -o ${WORKFLOW_GRAPH}.png

${PDFS}: ${WORKFLOW_GRAPH}.gv
	dot -Tpdf ${WORKFLOW_GRAPH}.gv -o ${WORKFLOW_GRAPH}.pdf

clean:
	rm -f *.xwam *.gv *.png *.pdf *.P *.txt ${RULES_DIR}/*.xwam
	rm -rf .noworkflow
