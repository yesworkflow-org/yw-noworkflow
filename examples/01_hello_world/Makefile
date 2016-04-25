

FACTS = yw_extract_facts.P yw_model_facts.P nw_facts.P

all: query.txt

yw_extract_facts.P yw_model_facts.P nw.P run.txt: *.py
	./run.sh &> run.txt

query.txt: ${FACTS}
	./query.sh &> query.txt

clean:
	rm -f *.xwam *.txt *.gv ${FACTS}
	rm -rf .noworkflow
