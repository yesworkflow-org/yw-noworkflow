
RULES_DIR = ../../rules
GRAPH_RULES_DIR = ../../graphs
RUN_SCRIPT = run.sh
RUN_STDOUT = run_outputs.txt
RUN_PRODUCTS =  ${RUN_STDOUT}
YW_VIEWS = yw_views.P
NW_VIEWS = nw_views.P
YW_NW_VIEWS = yw_nw_views.P
RULES = ${RULES_DIR}/nw_views.P ${RULES_DIR}/yw_views.P ${RULES_DIR}/yw_nw_views.P
QUERY_SCRIPT = query.sh
QUERY_OUTPUTS = query_outputs.txt
NW_FACTS = facts/nw_facts.P

WORKFLOW_GRAPH = workflow_graph
YW_DATA_GRAPH = yw_data_graph
YW_PROCESS_GRAPH = yw_process_graph

DOTS = ${WORKFLOW_GRAPH}.gv ${YW_DATA_GRAPH}.gv {YW_PROCESS_GRAPH}.gv
PNGS = ${WORKFLOW_GRAPH}.png ${YW_DATA_GRAPH}.png ${YW_PROCESS_GRAPH}.png
PDFS = ${WORKFLOW_GRAPH}.pdf ${YW_DATA_GRAPH}.pdf ${YW_PROCESS_GRAPH}.pdf

YW_PROPERTIES = yw.properties

all: ${QUERY_OUTPUTS} ${DOTS} ${PNGS} ${PDFS}

run: ${RUN_PRODUCTS}
yw: ${YW_VIEWS}
nw: ${NW_FACTS}
ywnw: ${YW_NW_VIEWS}
query: ${QUERY_OUTPUTS}
dots: ${DOTS}
png: ${PNGS}
pdf: ${PDFS}

${RUN_PRODUCTS}: ${RUN_SCRIPT} ${WORKFLOW_SCRIPT}
	bash -l ${RUN_SCRIPT} > ${RUN_STDOUT}

${YW_VIEWS}: ${WORKFLOW_SCRIPT} ${YW_PROPERTIES}
	mkdir -p facts
	bash -lc "yw graph ${WORKFLOW_SCRIPT} > ${WORKFLOW_GRAPH}.gv"
	${RULES_DIR}/materialize_yw_views.sh > ${YW_VIEWS}

${NW_FACTS}: ${RUN_PRODUCTS}
	mkdir -p facts
	now export -t -m dependency | grep -v 'environment(' > ${NW_FACTS}
	${RULES_DIR}/materialize_nw_views.sh > ${NW_VIEWS}

${YW_NW_VIEWS}: ${YW_VIEWS} ${NW_VIEWS}
	${RULES_DIR}/materialize_yw_nw_views.sh > ${YW_NW_VIEWS}

${QUERY_OUTPUTS}: ${QUERY_SCRIPT} ${YW_VIEWS} ${NW_FACTS} ${YW_NW_VIEWS} ${RULES}
	bash -l ${QUERY_SCRIPT} > ${QUERY_OUTPUTS}

${DOTS}: ${YW_NW_VIEWS}
	bash -l ../../graphs/${YW_DATA_GRAPH}.sh > ${YW_DATA_GRAPH}.gv
	bash -l ../../graphs/${YW_PROCESS_GRAPH}.sh > ${YW_PROCESS_GRAPH}.gv

${PNGS}: ${DOTS}
	dot -Tpng ${WORKFLOW_GRAPH}.gv -o ${WORKFLOW_GRAPH}.png
	dot -Tpng ${YW_DATA_GRAPH}.gv -o ${YW_DATA_GRAPH}.png
	dot -Tpng ${YW_PROCESS_GRAPH}.gv -o ${YW_PROCESS_GRAPH}.png

${PDFS}: ${DOTS}
	dot -Tpdf ${WORKFLOW_GRAPH}.gv -o ${WORKFLOW_GRAPH}.pdf
	dot -Tpdf ${YW_DATA_GRAPH}.gv -o ${YW_DATA_GRAPH}.pdf
	dot -Tpdf ${YW_PROCESS_GRAPH}.gv -o ${YW_PROCESS_GRAPH}.pdf

clean:
	rm -f *.xwam *.gv *.png *.pdf *.P *.txt ${RULES_DIR}/*.xwam
	rm -rf facts .noworkflow
