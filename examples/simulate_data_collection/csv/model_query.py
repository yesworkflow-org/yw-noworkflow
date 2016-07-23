import sqlite3

def MQ1(BlockName):
    '''% MQ1:  Where is the definition of block BLOCKNAME?
        :- table mq1/3.
        mq1(SourceFile, StartLine, EndLine) :-
        program_source(BLOCKNAME, SourceFile, StartLine, EndLine).'''
    query = "SELECT source_path, begin_line, end_line FROM program_source WHERE qualified_program_name = :BlockName;"
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print 'Source file: {}. Start Line: {}, End Line: {} '.format(r[0], r[1], r[2])

def MQ2():
    ''' MQ2:  What is the name and description of the top-level workflow?
        :- table mq2/2.
        mq2(WorkflowName,Description) :-
        top_workflow(W),
        program(W, _, WorkflowName, _, _),
        program_description(W, Description).'''
    query = """SELECT p.qualified_program_name, d.value
        FROM modelfacts_program p
        JOIN top_workflow t
        ON p.program_id = t.program_id
        JOIN program_description d
        ON p.program_id = d.program_id;
        """
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print 'WorkflowName: {}. Description: {}'.format(r[0], r[1])

def MQ3():
    '''% MQ3:  What are the names of any top-level functions?
    :- table mq3/1.
    mq3(FunctionName) :-
        function(F),
            not subprogram(F),
                program(F, _, FunctionName, _, _).
    '''
    query = """SELECT p.qualified_program_name FROM modelfacts_function f, subprogram sp, modelfacts_program p WHERE f.program_id = p.program_id AND f.program_id != sp.subprogram_id;"""
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print 'Top-level Function Name: {}'.format(r[0])

def MQ4():
    '''\
        % MQ4:  What are the names of the programs comprising the top-level workflow?
        :- table mq4/1.
        mq4(ProgramName) :-
        top_workflow(W),
        has_subprogram(W, P),
        program(P, ProgramName, _, _, _).'''
    query = """SELECT p.program_name
        FROM top_workflow t
        JOIN modelfacts_has_subprogram hs
        ON t.program_id = hs.program_id
        JOIN modelfacts_program p
        ON p.program_id = hs.subprogram_id;"""
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print 'SubProgram Name: {}'.format(r[0])


def MQ5():
    '''\
        % MQ5:  What are the names and descriptions of the inputs to the top-level workflow?
        :- table mq5/2.
        mq5(InputPortName,Description) :-
        top_workflow(W),
        has_in_port(W, P),
        port(P, _, InputPortName, _, _, _),
        port_description(P, Description).
        '''
    query = """SELECT p.port_name, pd.value
        FROM top_workflow t
        JOIN modelfacts_has_in_port hip
        ON t.program_id = hip.block_id
        JOIN modelfacts_port p
        ON hip.port_id = p.port_id
        JOIN port_description pd
        ON p.port_id = pd.port_id;"""
    cursor.execute(query)
    results = cursor.fetchall()
    for r in results:
        print 'InputPortName: {}. Description: {}'.format(r[0], r[1])

def MQ6(BlockName):
    '''% MQ6:  What data is output by program block BlockName?
        :- table mq6/2.
        mq6(DataName,Description) :-
        program(P, _,BlockName, _, _),
        has_out_port(P, OUT),
        port_data(OUT, DataName, _),
        port_description(OUT,Description).'''
    query = """SELECT DISTINCT pdata.data_name, pdes.value
        FROM modelfacts_program p
        JOIN modelfacts_has_out_port hop
        ON p.program_id = hop.block_id
        JOIN port_data pdata
        ON hop.port_id = pdata.port_id
        JOIN port_description pdes
        ON hop.port_id = pdes.port_id
        WHERE p.qualified_program_name = :BlockName;"""
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print 'Data Name: {}. Description: {}'.format(r[0], r[1])

def MQ7(BlockName):
    '''% MQ7: What program blocks provide input directly to BLOCKNAME?
        :- table mq7/1.
        mq7(ProgramName) :-
        program(P1, _, BlockName, _, _),
        has_in_port(P1, IN),
        port_data(IN, _, D),
        port_data(OUT, _, D),
        has_out_port(P2, OUT),
        program(P2, _, ProgramName, _, _).'''
    query = """SELECT DISTINCT p2.qualified_program_name
        FROM modelfacts_program p1
        JOIN modelfacts_has_in_port hip
        ON p1.program_id = hip.block_id
        JOIN port_data pd1 ON hip.port_id = pd1.port_id
        JOIN port_data pd2
        ON pd1.qualified_data_name = pd2.qualified_data_name
        JOIN modelfacts_has_out_port hop
        ON hop.port_id = pd2.port_id
        JOIN modelfacts_program p2
        ON hop.block_id = p2.program_id
        WHERE p1.qualified_program_name = :BlockName;"""
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ8(DataName):
    '''% MQ8: What programs have input ports that receive data data_name?
        :- table mq8/1.
        mq8(ProgramName) :-
        data(D, _, data_name),
        channel(C, D),
        port_connects_to_channel(IN, C),
        has_in_port(P, IN),
        program(P, _, ProgramName, _, _).'''
    query = """SELECT p.qualified_program_name
        FROM modelfacts_data d
        JOIN modelfacts_channel c
        ON d.data_id = c.data_id
        JOIN modelfacts_port_connects_to_channel pc
        ON c.channel_id = pc.channel_id
        JOIN modelfacts_has_in_port hip
        ON pc.port_id = hip.port_id
        JOIN modelfacts_program p
        ON hip.block_id = p.program_id
        WHERE d.qualified_data_name = :DataName;
        """
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ9(DataName):
    '''% MQ9: How many ports read data DataName?
        :- table mq9/1.
        mq9(PortCount) :-
        data(D, _, DataName),
        count(data_in_port(_, D), PortCount).'''
    query = """SELECT COUNT(*)
        FROM modelfacts_data d
        JOIN data_in_port dip
        ON dip.data_id = d.data_id
        WHERE d.qualified_data_name = :DataName;
        """
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    print '{} ports read data {}'.format(results[0][0], DataName)

def MQ10():
    '''% MQ10: How many data are read by more than 1 port in workflow?
        :- table mq10/1.
        mq10(DataCount) :-
        program(W, 'simulate_data_collection', _, _, _),
        count(data_in_workflow_read_by_multiple_ports(_, W), DataCount).'''
    query = """SELECT COUNT(*)
        FROM modelfacts_program p
        JOIN data_in_workflow_read_by_multiple_ports dmp
        ON p.program_id = dmp. program_id
        WHERE p.program_name = 'simulate_data_collection';
        """
    cursor.execute(query)
    results = cursor.fetchall()
    print '{} data are read by more than port in workflow'.format(results[0][0])

def MQ11(BlockName):
    '''% MQ11: What program blocks are immediately downstream of BlockName?
        :- table mq11/1.
        mq11(DownstreamProgramName) :-
        program(P1, DownstreamProgramName, _, _, _),
        program(P2, _, BlockName, _, _),
        program_immediately_downstream(P1, P2).'''
    query = """SELECT DISTINCT p1.program_name
        FROM modelfacts_program p1, modelfacts_program p2,
        program_immediately_downstream pid
        ON pid.child_id = p1.program_id
        AND pid.parent_id = p2.program_id
        WHERE p2.qualified_program_name = :BlockName;"""
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ12(BlockName):
    '''% MQ12: What program blocks are immediately upstream of BlockName?
        :- table mq12/1.
        mq12(UpstreamProgramName) :-
        program(P1, UpstreamProgramName, _, _, _),
        program(P2, _, BlockName, _, _),
        program_immediately_upstream(P1, P2).'''
    query = """SELECT DISTINCT p1.program_name
        FROM modelfacts_program p1, modelfacts_program p2,
        program_immediately_upstream piu
        ON piu.parent_id = p1.program_id
        AND piu.child_id = p2.program_id
        WHERE p2.qualified_program_name = :BlockName;"""
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ13(BlockName):
    '''% MQ13: What program blocks are upstream of BlockName?
        :- table mq13/1.
        mq13(UpstreamProgramName):-
        program(P1, UpstreamProgramName, _, _, _),
        program(P2, _, BlockName, _, _),
        program_upstream(P1, P2).'''
    query = """SELECT DISTINCT p1.program_name
        FROM modelfacts_program p1, modelfacts_program p2,
        program_upstream pu
        ON pu.ancestor_id = p1.program_id
        AND pu.descendent_id = p2.program_id
        WHERE p2.qualified_program_name = :BlockName;"""
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ14(BlockName):
    '''% MQ14: What program blocks are anywhere downstream of BlockName?
        :- table mq14/1.
        mq14(DownstreamProgramName):-
        program(P1, DownstreamProgramName, _, _, _),
        program(P2, _, BlockName, _, _),
        program_downstream(P1, P2).'''
    query = """SELECT DISTINCT p1.program_name
        FROM modelfacts_program p1, modelfacts_program p2,
        program_downstream pd
        ON pd.descendent_id = p1.program_id
        AND pd.ancestor_id = p2.program_id
        WHERE p2.qualified_program_name = :BlockName;"""
    cursor.execute(query, {"BlockName": BlockName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ15(DataName):
    '''% MQ15: What data is immediately downstream of DataName?
        :- table mq15/1.
        mq15(DownstreamDataName) :-
        data(D1, DownstreamDataName, _),
        data(D2, DataName, _),
        data_immediately_downstream(D1, D2).'''
    query = """SELECT DISTINCT d1.data_name
        FROM modelfacts_data d1, modelfacts_data d2,
        data_immediately_downstream did
        ON did.child_data_id = d1.data_id
        AND did.parent_data_id = d2.data_id
        WHERE d2.qualified_data_name = :DataName;"""
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ16(DataName):
    '''% MQ16: What data is immediately upstream of DataName?
        :- table mq16/1.
        mq16(UpstreamDataName) :-
        data(D1, UpstreamDataName, _),
        data(D2, DataName, _),
        data_immediately_upstream(D1, D2).'''
    query = """SELECT DISTINCT d1.data_name
        FROM modelfacts_data d1, modelfacts_data d2,
        data_immediately_upstream diu
        ON diu.parent_data_id = d1.data_id
        AND diu.child_data_id = d2.data_id
        WHERE d2.qualified_data_name = :DataName;"""
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ17(DataName):
    '''% MQ17: What data is downstream of accepted_sample?
    :- table mq17/1.
    mq17(DownstreamDataName):-
        data(D1, DownstreamDataName, _),
        data(D2, 'accepted_sample', _),
        data_downstream(D1, D2).'''
    query = """SELECT DISTINCT d1.data_name 
            FROM modelfacts_data d1, modelfacts_data d2, 
            data_downstream dd 
            ON dd.descendent_data_id = d1.data_id 
            AND dd.ancestor_data_id = d2.data_id 
            WHERE d2.qualified_data_name = :DataName;"""
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ18(DataName):
    '''% MQ18: What data is upstream of DatName?
    :- table mq18/1.
    mq18(UpstreamDataName):-
        data(D1, UpstreamDataName, _),
        data(D2, DataName, _),
        data_upstream(D1, D2).'''
    query = """SELECT DISTINCT d1.data_name 
            FROM modelfacts_data d1, modelfacts_data d2, 
            data_upstream du 
            ON du.ancestor_data_id = d1.data_id 
            AND du.descendent_data_id = d2.data_id 
            WHERE d2.qualified_data_name = :DataName;"""
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ19(DataName):
    '''% MQ19: What URI variables are associated with writes of data DataName?
    :- table mq19/1.
    mq19(VariableName) :-
        data(D, _, DataName),
        channel(C, D),
        port_connects_to_channel(OUT, C),
        has_out_port(_, OUT),
        uri_variable(_, VariableName, OUT).
    '''
    query = """SELECT uri.variable_name FROM modelfacts_data d 
            NATURAL JOIN modelfacts_channel c NATURAL JOIN modelfacts_port_connects_to_channel pcc 
            NATURAL JOIN modelfacts_has_out_port hop NATURAL JOIN modelfacts_uri_variable uri 
            WHERE d.qualified_data_name = :DataName;"""
    cursor.execute(query, {"DataName": DataName})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def MQ20(Data1, Data2):
    '''% MQ20: What URI variables do data written to raw_image and corrected_image have in common?
    :- table mq20/1.
    mq20(VariableName) :-
        data(D1, _, 'simulate_data_collection[raw_image]'),
        data(D2, _, 'simulate_data_collection[corrected_image]'),
        output_data_has_uri_variable(D1, V1),
        output_data_has_uri_variable(D2, V2),
        uri_variable(V1, VariableName, _),
        uri_variable(V2, VariableName, _).'''
    query = """SELECT DISTINCT uri1.variable_name FROM modelfacts_data d1
                NATURAL JOIN output_data_has_uri_variable ohu 
                NATURAL JOIN modelfacts_uri_variable uri1 
                JOIN modelfacts_uri_variable uri2 ON uri1.variable_name = uri2.variable_name 
                JOIN output_data_has_uri_variable ohu2 ON uri2.uri_variable_id = ohu2.uri_variable_id 
                JOIN modelfacts_data d2 ON ohu2.data_id = d2.data_id 
                WHERE d1.qualified_data_name = :Data1 AND d2.qualified_data_name = :Data2;"""
    cursor.execute(query, {"Data1": Data1, "Data2": Data2})
    results = cursor.fetchall()
    for r in results:
        print r[0]

def data_downstream():
    '''% Data D1 is downstream of data D2.
    :- table data_downstream/2.
    data_downstream(D1, D2) :-
        data_immediately_downstream(D1, D2).
    data_downstream(D1, D2):-
        data_immediately_downstream(D, D2),
        data_downstream(D1, D).'''
    view = """DROP VIEW IF EXISTS data_downstream;
            CREATE VIEW data_downstream AS
            WITH RECURSIVE data_down(x,y) AS 
            (SELECT * from data_immediately_downstream 
            UNION ALL 
            SELECT data_down.x, did.parent_data_id 
            FROM data_down, data_immediately_downstream did 
            ON data_down.y = did.child_data_id 
            WHERE data_down.x != data_down.y
            LIMIT 1000000) 
            SELECT x AS descendent_data_id, y AS ancestor_data_id FROM data_down;
    """
    cursor.executescript(view)

def data_immediately_downstream():
    '''% Data D1 is immediately downstream of data D2.
        :- table data_immediately_downstream/2.
        data_immediately_downstream(D1, D2) :-
        channel(C2, D2),
        port_connects_to_channel(In, C2),
        has_in_port(P, In),
        has_out_port(P, Out),
        port_connects_to_channel(Out, C1),
        channel(C1, D1).'''
    view = """DROP VIEW IF EXISTS data_immediately_downstream;
        CREATE VIEW data_immediately_downstream AS
        SELECT DISTINCT c1.data_id AS child_data_id,
        c2.data_id AS parent_data_id
        FROM modelfacts_channel c2
        NATURAL JOIN modelfacts_port_connects_to_channel pc2 
        NATURAL JOIN modelfacts_has_in_port hip  
        JOIN modelfacts_has_out_port hop 
        ON hop.block_id = hip.block_id 
        JOIN modelfacts_port_connects_to_channel pc1 
        ON hop.port_id = pc1.port_id 
        JOIN modelfacts_channel c1 
        ON pc1.channel_id = c1.channel_id;
        """
    cursor.executescript(view)

def data_immediately_upstream():
    '''% Data D1 is immediately upstream of data D2.
    :- table data_immediately_upstream/2.
    data_immediately_upstream(D1, D2) :-
    data_immediately_downstream(D2, D1).
    '''
    view = """DROP VIEW IF EXISTS data_immediately_upstream;
            CREATE VIEW data_immediately_upstream AS
            SELECT parent_data_id, child_data_id 
            FROM data_immediately_downstream;
    """
    cursor.executescript(view)

def data_in_port():
    '''
    data_in_port(P, D) :-
        port_connects_to_channel(P, C),
        channel(C, D),
        has_in_port(_, P).'''
    view = """DROP VIEW IF EXISTS data_in_port;
            CREATE VIEW data_in_port AS
            SELECT pc.port_id, c.data_id 
            FROM modelfacts_port_connects_to_channel pc 
            JOIN modelfacts_channel c 
            ON pc.channel_id = c.channel_id 
            JOIN modelfacts_has_in_port hip 
            ON hip.port_id = pc.port_id; 
    """
    cursor.executescript(view)
    
def data_in_port_count():
    '''data_in_port_count(PortCount, D) :-
    data(D, _, _),
    count(data_in_port(_, D), PortCount).'''    
    view = """DROP VIEW IF EXISTS data_in_port_count;
            CREATE VIEW data_in_port_count AS
            SELECT COUNT(*) AS total, d.data_id 
            FROM modelfacts_data d 
            JOIN data_in_port ON d.data_id = data_in_port.data_id 
            GROUP BY d.data_id;
    """
    cursor.executescript(view)

def data_in_workflow_read_by_multiple_ports():
    '''data_in_workflow_read_by_multiple_ports(D, W) :-
    has_subprogram(W, P),
    has_in_port(P, IN),
    port_connects_to_channel(IN, C),
    channel(C, D),
    data_in_port_count(Count, D),
    Count > 1.'''
    view = """DROP VIEW IF EXISTS data_in_workflow_read_by_multiple_ports;
            CREATE VIEW data_in_workflow_read_by_multiple_ports AS
            SELECT DISTINCT c.data_id, s.program_id 
            FROM modelfacts_has_subprogram s 
            JOIN modelfacts_has_in_port hip 
            ON s.subprogram_id = hip.block_id 
            JOIN modelfacts_port_connects_to_channel pc 
            ON hip.port_id = pc.port_id 
            JOIN modelfacts_channel c 
            ON pc.channel_id = c.data_id 
            JOIN data_in_port_count dipc 
            ON dipc.data_id = c.data_id 
            WHERE dipc.total > 1;

    """
    cursor.executescript(view)
 
def data_upstream():
    view = """DROP VIEW IF EXISTS data_upstream;
            CREATE VIEW data_upstream AS
            SELECT ancestor_data_id, descendent_data_id 
            FROM data_downstream;
    """
    cursor.executescript(view)
     
def port_data():
    '''% Port P reads or writes data D with name N and qualified name QN.
    :- table port_data/3.
    port_data(P, N, QN) :-
        port_connects_to_channel(P, C),
        channel(C, D),
        data(D, N, QN).'''
    view = """DROP VIEW IF EXISTS port_data;
            CREATE VIEW port_data AS
            SELECT DISTINCT pc.port_id, d.data_name, d.qualified_data_name 
            FROM modelfacts_port_connects_to_channel pc 
            JOIN modelfacts_channel c 
            ON pc.channel_id = c.channel_id 
            JOIN modelfacts_data d 
            ON c.data_id = d.data_id;
    """
    cursor.executescript(view)
 
def port_description():
    '''\
    % Port P has description D.
    :- table port_description/2.
    port_description(P,D) :-
        port(P, _, _, _, PA, _),
        annotation_qualifies(DA, PA),
        annotation(DA, _, _, 'desc', _, D).
    '''
    view = """DROP VIEW IF EXISTS port_description;
            CREATE VIEW port_description AS
            SELECT p.port_id port_id, a.value value
            FROM modelfacts_port p 
            JOIN extractfacts_annotation_qualifies aq 
            ON p.port_annotation_id = aq.primary_annotation_id 
            JOIN port_alias_description a 
            ON aq.qualifying_annotation_id = a.annotation_id GROUP BY line_number;"""
    cursor.executescript(view)

def output_data_has_uri_variable():
    '''% Data D with URI variable V passed through output port P.
    :- table output_data_has_uri_variable/2.
    output_data_has_uri_variable(D, V) :-
        channel(C, D),
        port_connects_to_channel(P, C),
        has_out_port(_, P),
        uri_variable(V, _, P).   '''
    view = """DROP VIEW IF EXISTS output_data_has_uri_variable;
            CREATE VIEW output_data_has_uri_variable AS
            SELECT c.data_id, uri.uri_variable_id 
            FROM modelfacts_channel c NATURAL JOIN modelfacts_port_connects_to_channel 
            NATURAL JOIN modelfacts_has_out_port NATURAL JOIN modelfacts_uri_variable uri;
           """
    cursor.executescript(view)

def port_alias_description():
    view = """DROP VIEW IF EXISTS port_alias_description;
            CREATE VIEW port_alias_description AS
            SELECT * FROM extractfacts_annotation a1 WHERE a1.tag IN ('desc', 'as');"""
    cursor.executescript(view)

def program_description():
    '''% Program P has description D.
    :- table program_description/2.
    program_description(P,D) :-
        program(P, _, _, BA, _),
       annotation_qualifies(DA, BA),
       annotation(DA, _, _, 'desc', _, D).'''
    view = """DROP VIEW IF EXISTS program_description;
            CREATE VIEW program_description AS
            SELECT DISTINCT p.program_id, a.value 
            FROM modelfacts_program p
            JOIN extractfacts_annotation_qualifies aq 
            ON p.begin_annotation_id = aq.primary_annotation_id 
            JOIN extractfacts_annotation a 
            ON a.annotation_id = aq.qualifying_annotation_id 
            WHERE a.tag = 'desc';"""
    cursor.executescript(view)

def program_downstream():
    '''% Program P1 is downstream of Program P2.
    :- table program_downstream/2.
    program_downstream(P1, P2) :-
        program_immediately_downstream(P1, P2).
    program_downstream(P1, P2) :-
        program_downstream(P1, P),
        program_immediately_downstream(P, P2).'''
    view = """DROP VIEW IF EXISTS program_downstream;
            CREATE VIEW program_downstream AS
            WITH RECURSIVE prog_down(x,y) AS 
            (SELECT * from program_immediately_downstream 
            UNION ALL 
            SELECT prog_down.x, pid.parent_id 
            FROM prog_down, program_immediately_downstream pid 
            ON prog_down.y = pid.child_id 
            WHERE prog_down.x != prog_down.y
            LIMIT 1000000) 
            SELECT x AS descendent_id, y AS ancestor_id FROM prog_down;
    """
    cursor.executescript(view)

def program_immediately_downstream():
    '''% Program P1 is immediately downstream of Program P2.
    :- table program_immediately_downstream/2.
    program_immediately_downstream(P1, P2) :-
        has_in_port(P1, In),
        port_connects_to_channel(In, C),
        port_connects_to_channel(Out, C),
        has_out_port(P2, Out).'''
    view = """DROP VIEW IF EXISTS program_immediately_downstream;
            CREATE VIEW program_immediately_downstream AS
            SELECT DISTINCT hip.block_id AS child_id, 
            hop.block_id AS parent_id 
            FROM modelfacts_has_in_port hip 
            JOIN modelfacts_port_connects_to_channel pc1 
            ON hip.port_id = pc1.port_id 
            JOIN modelfacts_port_connects_to_channel pc2 
            ON pc1.channel_id = pc2.channel_id 
            JOIN modelfacts_has_out_port hop 
            ON pc2.port_id = hop.port_id;        
    """
    cursor.executescript(view)

def program_immediately_upstream():
    '''% Program P1 is immediately upstream of Program P2.
    :- table program_immediately_upstream/2.
    program_immediately_upstream(P1, P2) :-
        program_immediately_downstream(P2, P1).'''

    view = """DROP VIEW IF EXISTS program_immediately_upstream;
            CREATE VIEW program_immediately_upstream AS
            SELECT parent_id, child_id 
            FROM program_immediately_downstream;
    """
    cursor.executescript(view)

def program_source():
    '''% Program with qualified name QN is defined in source file SF from first line F to last line L.
    :- table program_source/4.
    program_source(QN, SF, F, L) :-
        program(_, _, QN, BA, EA),
        annotation(BA, S, F, _, _, _),
        annotation(EA, S, L, _, _, _),
        extract_source(S, SF).'''
    view = """DROP VIEW IF EXISTS program_source;
            CREATE VIEW program_source AS
            SELECT DISTINCT p.qualified_program_name, es.source_path,
            a1.line_number AS begin_line, a2.line_number AS end_line
            FROM modelfacts_program p 
            JOIN extractfacts_annotation a1 
            ON p.begin_annotation_id = a1.annotation_id 
            JOIN extractfacts_annotation a2 
            ON p.end_annotation_id = a2.annotation_id 
            JOIN extractfacts_extract_source es 
            ON es.source_id = a1.source_id 
            AND es.source_id = a2.source_id;"""
    cursor.executescript(view)

def program_upstream():
    '''% Program P1 is upstream of Program P2.
        :- table program_upstream/2.
        program_upstream(P1, P2) :-
            program_downstream(P2, P1).'''
    view = """DROP VIEW IF EXISTS program_upstream;
            CREATE VIEW program_upstream AS
            SELECT ancestor_id, descendent_id 
            FROM program_downstream;"""
    cursor.executescript(view)

def subprogram():
    view = """DROP VIEW IF EXISTS subprogram;
            CREATE VIEW subprogram AS
            SELECT subprogram_id
            FROM modelfacts_has_subprogram WHERE EXISTS
               (SELECT a.program_id, b.program_id
               FROM modelfacts_program a JOIN modelfacts_program b);"""
    cursor.executescript(view)


def top_workflow():
    ''' % Workflow W is the top-level workflow.
     :- table top_workflow/1.
     top_workflow(W) :-
         workflow(W),
         not subprogram(W).'''
    view = """DROP VIEW IF EXISTS top_workflow;
            CREATE VIEW top_workflow AS
            SELECT program_id 
            FROM modelfacts_workflow
            WHERE program_id NOT IN subprogram;"""
    cursor.executescript(view)

def run_rules():
    subprogram()
    top_workflow()
    program_description()
    port_alias_description()
    port_description()
    program_source()
    port_data()
    data_in_port()
    data_in_port_count()
    data_in_workflow_read_by_multiple_ports()
    program_immediately_downstream()
    program_immediately_upstream()
    program_downstream()
    program_upstream()
    data_immediately_downstream()
    data_immediately_upstream()
    data_downstream()
    data_upstream()
    output_data_has_uri_variable()

if __name__ == '__main__':
    DataName1 = "simulate_data_collection[raw_image]"
    BlockName1 = "simulate_data_collection.collect_data_set"
    uriData1 = DataName1
    uriData2 = "simulate_data_collection[corrected_image]"
    connection = sqlite3.connect('facts.db')
    cursor = connection.cursor()
    run_rules()
    print "\nMQ1:  Where is the definition of block", BlockName1,"?"
    MQ1(BlockName1)
    print "\nMQ2:  What is the name and description of the top-level workflow?"
    MQ2()
    print "\nMQ3:  What are the names of any top-level functions?"
    MQ3()
    print "\nMQ4:  What are the names of the programs comprising the top-level workflow?"
    MQ4()
    print "\nMQ5:  What are the names and descriptions of the inputs to the top-level workflow?"
    MQ5()
    print "\nMQ6:  What data is output by program block", BlockName1,"?"
    MQ6(BlockName1)
    print "\nMQ7: What program blocks provide input directly to", BlockName1,"?"
    MQ7(BlockName1)
    print "\nMQ8: What programs have input ports that receive data", DataName1,"?"
    MQ8(DataName1)
    print "\nMQ9: How many ports read data", DataName1,"?"
    MQ9(DataName1)
    print "\nMQ10: How many data are read by more than 1 port in workflow?"
    MQ10()
    print "\nMQ11: What program blocks are immediately downstream of", BlockName1,"?"
    MQ11(BlockName1)
    print "\nMQ12: What program blocks are immediately upstream of", BlockName1,"?"
    MQ12(BlockName1)
    print "\nMQ13: What program blocks are upstream of", BlockName1,"?"
    MQ13(BlockName1)
    print "\nMQ14: What program blocks are downstream of", BlockName1,"?"
    MQ14(BlockName1)
    print "\nMQ15: What data is immediately downstream of", DataName1,"?"
    MQ15(DataName1)
    print "\nMQ16: What data is immediately upstream of", DataName1,"?"
    MQ16(DataName1)
    print "\nMQ17: What data is downstream of", DataName1,"?"
    MQ17(DataName1)
    print "\nMQ18: What data is uptream of", DataName1,"?"
    MQ18(DataName1)
    print "\nMQ19: What URI variables are associated with writes of data", uriData1,"?"
    MQ19(DataName1)
    print "\nMQ20: What URI variables do data written to ", uriData1, "and", uriData2, " have in common?"
    MQ20(uriData1,uriData2)
    cursor.close()
    connection.close()

