import sqlite3

def EQ1():
    # EQ1:  What source files SF were YW annotations extracted from?

    query = "SELECT source_path FROM Extractfacts_extract_source;"
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print r[0]

def EQ2():
    # EQ2:  What are the names N of all program blocks?
    query = "SELECT value FROM extractfacts_annotation WHERE LOWER(keyword) == '@begin';"
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print r[0]

def EQ3():
    # EQ3:  What out ports are qualified with URIs?
    # :- table eq3/1.
    # eq3(PortName) :-
    # annotation(URI, _, _, 'uri', _, _),
    # annotation(OUT, _, _, 'out', _, PortName),
    # annotation_qualifies(URI, OUT).
    query = """SELECT DISTINCT b.value
               FROM extractfacts_annotation a 
               JOIN extractfacts_annotation b
               ON a.tag = 'uri' AND b.tag = 'out'
               JOIN extractfacts_annotation_qualifies aq
               ON a.annotation_id = aq.qualifying_annotation_id AND
               b.annotation_id = aq.primary_annotation_id;"""
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print r[0]

if __name__ == '__main__':

    connection = sqlite3.connect('./facts/yw_facts.db')
    cursor = connection.cursor()

    print "EQ1:  What source files SF were YW annotations extracted from?"
    EQ1()

    print "\nEQ2:  What are the names N of all program blocks?"
    EQ2()

    print "\nEQ3:  What out ports are qualified with URIs?"
    EQ3()
    cursor.close()
    connection.close()

