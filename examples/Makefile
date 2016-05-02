
RUN_STDOUT = run_outputs.txt
RUN_PRODUCTS =  ${RUN_STDOUT}
YW_FACTS = yw_extract_facts.P yw_model_facts.P
YW_VIEWS = yw_views.P
RULES = ../rules/yw_rules.P ../rules/yw_nw_rules.P ../rules/yw_view_rules.P
QUERY_SCRIPT = run_queries.sh
QUERY_OUTPUTS = query_outputs.txt
NW_FACTS = nw_facts.P

WORKFLOW_GRAPH = workflow_graph
DOTS = ${WORKFLOW_GRAPH}.gv
PNGS = ${WORKFLOW_GRAPH}.png
PDFS = ${WORKFLOW_GRAPH}.pdf

YW_PROPERTIES = yw.properties

all: ${RUN_PRODUCTS} ${YW_VIEWS} ${NW_FACTS} ${QUERY_OUTPUTS} ${DOTS} ${PNGS} ${PDFS}

run: ${RUN_PRODUCTS}
yw: ${YW_VIEWS}
nw: ${NW_FACTS}
query: ${QUERY_OUTPUTS}
dots: ${DOTS}
png: ${PNGS}
pdf: ${PDFS}

${RUN_STDOUT}: ${WORKFLOW_SCRIPT}
	now run -e Tracer ${WORKFLOW_SCRIPT} &> ${RUN_STDOUT}

${YW_FACTS}: ${WORKFLOW_SCRIPT} ${YW_PROPERTIES}
	bash -lc "yw model ${WORKFLOW_SCRIPT}"

${YW_VIEWS}: ${YW_FACTS} ${RULES}
	../rules/materialize_yw_views.sh &> ${YW_VIEWS}

${WORKFLOW_GRAPH}.gv : ${WORKFLOW_SCRIPT} ${YW_PROPERTIES}
	bash -lc "yw graph ${WORKFLOW_SCRIPT} > ${WORKFLOW_GRAPH}.gv"

${NW_FACTS}: ${RUN_PRODUCTS}
	now export -m dependency | grep -v 'environment(' > ${NW_FACTS}

${QUERY_OUTPUTS}: ${QUERY_SCRIPT} ${YW_FACTS} ${NW_FACTS} ${RULES}
	./run_queries.sh &> ${QUERY_OUTPUTS}

${PNGS}: ${WORKFLOW_GRAPH}.gv
	dot -Tpng ${WORKFLOW_GRAPH}.gv -o ${WORKFLOW_GRAPH}.png

${PDFS}: ${WORKFLOW_GRAPH}.gv ${QUERY_PRODUCTS}
	dot -Tpdf ${WORKFLOW_GRAPH}.gv -o ${WORKFLOW_GRAPH}.pdf

clean:
	rm -f *.xwam *.gv *.png *.pdf *.P *.txt ../rules/*.xwam
	rm -rf .noworkflow
