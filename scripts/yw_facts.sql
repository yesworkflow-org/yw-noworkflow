.mode csv


DROP TABLE IF EXISTS extractfacts_annotation;
CREATE TABLE extractfacts_annotation(
    annotation_id   INTEGER,
    source_id       INTEGER,
    line_number     INTEGER,
    tag             TEXT,
    keyword         TEXT,
    value           TEXT
);
.import ./csv/extractfacts_annotation.csv extractfacts_annotation

DROP TABLE IF EXISTS extractfacts_extract_source;
CREATE TABLE extractfacts_extract_source(
    source_id   INTEGER,
    source_path TEXT    
);
.import ./csv/extractfacts_extract_source.csv extractfacts_extract_source

DROP TABLE IF EXISTS extractfacts_annotation_qualifies;
CREATE TABLE extractfacts_annotation_qualifies(
    qualifying_annotation_id     INTEGER,
    primary_annotation_id        INTEGER
);
.import ./csv/extractfacts_annotation_qualifies.csv extractfacts_annotation_qualifies

DROP TABLE IF EXISTS modelfacts_channel;
CREATE TABLE modelfacts_channel(
    channel_id  INTEGER,
    data_id     INTEGER
);
.import ./csv/modelfacts_channel.csv modelfacts_channel

DROP TABLE IF EXISTS modelfacts_data;
CREATE TABLE modelfacts_data(
    data_id             INTEGER,
    data_name           TEXT,
    qualified_data_name TEXT
);
.import ./csv/modelfacts_data.csv modelfacts_data

DROP TABLE IF EXISTS modelfacts_function;
CREATE TABLE modelfacts_function(
    program_id  	INTEGER
);
.import ./csv/modelfacts_function.csv modelfacts_data

DROP TABLE IF EXISTS modelfacts_has_in_port;
CREATE TABLE modelfacts_has_in_port(
    block_id    INTEGER,
    port_id     INTEGER
);
.import ./csv/modelfacts_has_in_port.csv modelfacts_has_in_port

DROP TABLE IF EXISTS modelfacts_has_out_port;
CREATE TABLE modelfacts_has_out_port(
    block_id    INTEGER,
    port_id     INTEGER
);
.import ./csv/modelfacts_has_out_port.csv modelfacts_has_out_port

DROP TABLE IF EXISTS modelfacts_has_subprogram;
CREATE TABLE modelfacts_has_subprogram(
    program_id      INTEGER,
    subprogram_id   INTEGER
);
.import ./csv/modelfacts_has_subprogram.csv modelfacts_has_subprogram 

DROP TABLE IF EXISTS modelfacts_inflow_connects_to_channel;
CREATE TABLE modelfacts_inflow_connects_to_channel(
    port_id     INTEGER,
    channel_id  INTEGER
);
.import ./csv/modelfacts_inflow_connects_to_channel.csv  modelfacts_inflow_connects_to_channel

DROP TABLE IF EXISTS modelfacts_log_template;
CREATE TABLE modelfacts_log_template(
    log_template_id     INTEGER,
    port_id             INTEGER,
    entry_template      TEXT,
    log_annotation_id   INTEGER
);
.import ./csv/modelfacts_log_template.csv  modelfacts_log_template

DROP TABLE IF EXISTS modelfacts_outflow_connects_to_channel;
CREATE TABLE modelfacts_outflow_connects_to_channel(
    port_id     INTEGER,
    channel_id  INTEGER
);
.import ./csv/modelfacts_outflow_connects_to_channel.csv modelfacts_outflow_connects_to_channel

DROP TABLE IF EXISTS modelfacts_port;
CREATE TABLE modelfacts_port(
    port_id             INTEGER,
    port_type           TEXT,
    port_name           TEXT,
    qualified_port_name TEXT,
    port_annotation_id  INTEGER,
    data_id             INTEGER
);
.import ./csv/modelfacts_port.csv modelfacts_port

DROP TABLE IF EXISTS modelfacts_port_alias;
CREATE TABLE modelfacts_port_alias(
    port_id     INTEGER,
    alias       TEXT
);
.import ./csv/modelfacts_port_alias.csv modelfacts_port_alias

DROP TABLE IF EXISTS modelfacts_port_connects_to_channel;
CREATE TABLE modelfacts_port_connects_to_channel(
    port_id     INTEGER,
    channel_id  INTEGER
);
.import ./csv/modelfacts_port_connects_to_channel.csv modelfacts_port_connects_to_channel

DROP TABLE IF EXISTS modelfacts_port_uri_template;
CREATE TABLE modelfacts_port_uri_template(
    port_id     INTEGER,
    uri         TEXT
);
.import ./csv/modelfacts_port_uri_template.csv modelfacts_port_uri_template 

DROP TABLE IF EXISTS modelfacts_program;
CREATE TABLE modelfacts_program(
    program_id              INTEGER,
    program_name            TEXT,
    qualified_program_name  TEXT,
    begin_annotation_id     INTEGER,
    end_annotation_id       INTEGER
);
.import ./csv/modelfacts_program.csv modelfacts_program

DROP TABLE IF EXISTS modelfacts_uri_variable;
CREATE TABLE modelfacts_uri_variable(
    uri_variable_id     INTEGER,
    variable_name       TEXT,
    port_id             INTEGER
);
.import ./csv/modelfacts_uri_variable.csv modelfacts_uri_variable

DROP TABLE IF EXISTS modelfacts_workflow;
CREATE TABLE modelfacts_workflow(
    program_id      INTEGER
);
.import ./csv/modelfacts_workflow.csv modelfacts_workflow

