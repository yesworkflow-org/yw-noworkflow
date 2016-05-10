

SUBDIRS =	01_hello_world  \
		 	02_custom_hello_world \
			03_emphasized_hello_world \
			04_iterative_emphasis \
			simulate_data_collection

all:
	for dir in $(SUBDIRS); do \
		echo; \
		echo "---------- Building $$dir --------------------" ;	\
		make -C $$dir all; \
	done

clean:
	for dir in $(SUBDIRS); do \
		echo; \
		echo "---------- Cleaning $$dir --------------------" ; \
		make -C $$dir clean; \
	done
