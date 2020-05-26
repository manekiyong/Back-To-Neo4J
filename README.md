Existingly, after exporting CSV file with APOC, users cannot rebuild the graph out of the exported CSV file. This script parses the CSV data and rebuilds the original graph based on the APOC exported CSV file.

The CSV Data should have minimally the following header columns:
'_id'
'_labels'
'_start'
'_end'
'_type'

Important notes:
1) The internal id of each node and relation may NOT be the same as the original graph, because users are not allowed to tweak the internal id of each nodes and relation.
2) Constraints are not copied. Users are required to recreate their own constraints
3) If required, run requirements.txt (pip install -r example-requirements.txt)

To export CSV File (Refer to https://neo4j.com/docs/labs/apoc/current/export/csv/ for full details):
1) Install APOC Plugin to database
2) Configure settings and include line 'apoc.export.file.enabled=true'
3) Run Cypher Query "CALL apoc.export.csv.all("filename.csv", {})" on Neo4J Browser
4) If file destination is not set, click on 'Open Folder', and CSV file is in 'import' folder.


To import CSV File (APOC NOT REQUIRED):
1) Place the previously exported CSV file in 'Back_In_Neo4J' root folder (Together with config.py and Back_In_Neo4J.py)
2) Check Auth settings, and change FILE_NAME
3) Run 'Back_In_Neo4J.py"

