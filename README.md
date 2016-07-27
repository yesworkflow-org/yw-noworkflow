YesWorkflow-NoWorkflow Bridge
=============================
#Overview
The yw-noworkflow repository contains experimental code that explores how the complementary provenance 
information provided by [YesWorkflow](https://github.com/yesworkflow-org/yw-prototypes/tree/master) and [NoWorkflow](https://github.com/gems-uff/noworkflow) can be used together to yield visualizations and 
query results that neither can provide on its own.

#Installation
YesWorkflow-NoWorkflow Bridge requires the installation of both YesWorkflow and NoWorkflow, in order to perform XSB Prolog and SQL queries.

###YesWorkflow
YesWorkflow is a scientific workflow management system that extracts YW commends that users add to scripts that reveal the computational modules and dataflows, render graphical output that reveals the stages of computation and the flow of data in the script, and store the prospective provenance of the data products of scripts. 

YesWorkflow installation details and instructions can be found in [yw-prototype repository](https://github.com/yesworkflow-org/yw-prototypes).

Note that this demonstratiion requires YesWorkflow 0.2.1.The latest version of YesWorkflow can be obtained from:
```
    https://opensource.ncsa.illinois.edu/bamboo/browse/KURATOR-YSF-3/artifact
```
You may also want to define an alias to simplify running YesWorkflow at the command line.

If you have saved yesworkflow-0.2-SNAPSHOT-jar-with-dependencies.jar to the bin subdirectory of your home directory, the following command will create a bash alias for running YesWorkflow simply by typing yw:

alias yw='java -jar ~/bin/yesworkflow-0.2-SNAPSHOT-jar-with-dependencies.jar'
On Windows the command to create the yw macro is:

doskey yw=java -jar %USERPROFILE%\bin\yesworkflow-0.2-SNAPSHOT-jar-with-dependencies.jar $*

###NoWorkflow
NoWorkflow collects provenance for Python scripts in SQLite database. It could show provenance of a trial, compare the collected provenance of different trials, visualize the dataflow, and perform Prolog and SQL queries.

NoWorkflow installation details and instructions can be found in [noWorkflow repository](https://github.com/gems-uff/noworkflow).

###XSB Prolog and SQLite
XSB is a Logic Programming system for Unix and Windows-based platforms. SQLite is a relational database management system contained in a C programming library, and is an embedded SQL database engine. YesWorkflow-NoWorkflow Bridge will use XSB and SQLite to define rules for YesWorkflow, NoWorkflow, and the bridge, and perform queries for them. 

You can find instructions for installing XSB at [XSB Website](http://xsb.sourceforge.net/), or on [the Github page](https://github.com/flavioc/XSB).

Go to [SQLite download page](http://www.sqlite.org/download.html), and download precompiled binaries.

If you are on a Linux or Mac OS X machine, it probably is pre-installed with SQLite. Check if you already have SQLite installed on your machine or not.
```
$ sqlite3
SQLite version 3.8.10.2 2015-05-20 18:17:19
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite>
```