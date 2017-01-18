import sqlite3

def YW_NW_q1(DataName, BlockName):
    '''
        What Python variables carries values of DataName into the BlockName workflow step?
        :- table yw_nw_q1/3.
        yw_nw_q1(VariableId, VariableName, VariableValue) :-
        yw_flow(_, _, _, _, _, 'emphasized_greeting', PortId, _, _, 'print_greeting'),
        nw_variable_for_yw_in_port(VariableId, VariableName, VariableValue, _, _, _, PortId, _, _, _).'''
    query = """SELECT variable_id,variable_name,variable_value
        FROM yw.yw_flow yf, nw_variable_for_yw_in_port_10 vip
        WHERE yf.data_name = :DataName AND yf.sink_program_name = :BlockName 
        AND yf.sink_port_id = vip.port_id;"""
    cursor.execute(query, {"DataName": DataName, "BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print 'Variable ID: {}. Variable Name: {}, Variable Value {} '.format(r[0], r[1], r[2])

def YW_NW_q2(DataName, BlockName):
    '''
        What values are emitted by the DataName output of the BlockName step?
        :- table yw_nw_q1/3.
        yw_nw_q2(VariableValue) :-
            yw_step_output(_, 'transform_images', _, PortId, _, _, 'corrected_image'),
            nw_variable_for_yw_out_port(VariableId, VariableName, VariableValue, _, _, PortId, _, _, _).
    '''
    query = """SELECT variable_id, variable_name,variable_value 
        FROM yw.yw_step_output yo, nw_variable_for_yw_out_port vop 
        WHERE vop.port_id = yo.port_id 
        AND yo.program_name = :BlockName AND yo.data_name = :DataName;"""
    cursor.execute(query, {"DataName": DataName, "BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print 'Variable ID: {}. Variable Name: {}, Variable Value {} '.format(r[0], r[1], r[2])

if __name__ == '__main__':
    DataName1 = "sample_name"
    BlockName1 = "calculate_strategy"
    DataName2 = "corrected_image"
    BlockName2 = "transform_images"
    connection = sqlite3.connect('views/yw_nw_views.db')
    cursor = connection.cursor()
    cursor.execute("ATTACH 'views/nw_views.db' as nw")
    cursor.execute("ATTACH 'views/yw_views.db' as yw")

    print "\nYW_NW_q1: What Python variables carries values of ",DataName1, " into the ",BlockName1, " step?"
    YW_NW_q1(DataName1, BlockName1)
    
    print "\nYW_NW_q2: What values are emitted by the ",DataName2," output of the ",BlockName2," step?"
    YW_NW_q2(DataName2, BlockName2)
    
    cursor.execute("DETACH database nw")
    cursor.execute("DETACH database yw")

    cursor.close()
    connection.close()

