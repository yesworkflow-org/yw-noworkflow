

SUBDIRS =	01_hello_world  \
		 	02_custom_hello_world \
			03_emphasized_hello_world \
			04_iterative_emphasis \
			05_emphasis_function \
			06_greeting_from_file \
			simulate_data_collection

all:
	for dir in $(SUBDIRS); do \
		echo; \
		echo "---------- Building $$dir --------------------" ;	\
		$(MAKE) -C $$dir all; \
	done

clean:
	for dir in $(SUBDIRS); do \
		echo; \
		echo "---------- Cleaning $$dir --------------------" ; \
		$(MAKE) -C $$dir clean; \
	done
