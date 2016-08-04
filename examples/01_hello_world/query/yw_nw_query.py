import sqlite3

def YW_NW_q1(DataName):
    '''
        yw_nw_q1(FunctionName) :-
        nw_activation_from_yw_step(_, FunctionName, _, 'print_greeting', _).
        end_of_file.
        printall(yw_nw_q1(_)).
    '''
    query = """SELECT func_name FROM nw_activation_from_yw_step 
                WHERE step_name = :DataName;"""
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    for r in results:
        print r[0]


if __name__ == '__main__':
    DataName1 = "print_greeting"
    
    connection = sqlite3.connect('views/yw_nw_views.db')
    cursor = connection.cursor()
    cursor.execute("ATTACH 'views/nw_views.db' as nw")
    cursor.execute("ATTACH 'views/yw_views.db' as yw")

    print "\nYW_NW_q1: What functions are called from within the workflow step ",DataName1, "?"
    YW_NW_q1(DataName1)
    
    cursor.execute("DETACH database nw")
    cursor.execute("DETACH database yw")

    cursor.close()
    connection.close()

