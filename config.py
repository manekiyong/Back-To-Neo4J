NEO4J_ENDPT='localhost'
AUTH_ID='neo4j'
AUTH_PWD='123'
WITH_AUTH=True     #if dbms.security.auth_enabled=true, WITH_AUTH = True and vice versa. 
BATCH_SIZE = 50    #How many nodes created at once; Recommended 50~100
FILE_NAME = 'neo4j.csv'
BOLT_PORT=7687