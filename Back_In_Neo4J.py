from neo4j import GraphDatabase
import pandas as pd
import numpy as np
import math

import config

if config.WITH_AUTH: #dbms.security.auth_enabled=true
    graph = GraphDatabase.driver('bolt://{0}:{1}'.format(config.NEO4J_ENDPT, config.BOLT_PORT) , auth=(config.AUTH_ID, config.AUTH_PWD), encrypted=False)
else: #dbms.security.auth_enabled=false
    graph = GraphDatabase.driver('bolt://{0}:{1}'.format(config.NEO4J_ENDPT, config.BOLT_PORT))

def read_cypher_query(graph, query):
    with graph.session() as session:
        return session.read_transaction(commit_read_transaction, query)

def commit_read_transaction(tx, query):
    return tx.run(query)

def getNewID(oldID):
    return nodedf.loc[nodedf['_id']==oldID]['mapID'].values[0]

def cleanString(unclean):
    cleaning = unclean.replace("\'","\\\'")
    return cleaning.replace("\"", "\\\"")

data = pd.read_csv (r'{0}'.format(config.FILE_NAME))

count=0 #Find the separating column between nodes & relations
for i in data:
    if(i=="_start"):
        break
    count+=1

nodedf = data.iloc[:,:count].dropna(axis = 0, how = 'all')
rlsdf = data.iloc[:,count:].dropna(axis = 0, how = 'all')

##################### Creation of Nodes ############################
print("Creating Nodes...")
fullarr = []
query = """"""
count=0
totalcount = 0
batchCount = 0
batchSize = config.BATCH_SIZE
totalSize = len(nodedf)
numBatch = math.ceil(totalSize/batchSize)
nodecount = 0

for index, rows in nodedf.iterrows():
    nodecount+=1
    query = query + """MERGE(x{0}{1}""".format(count,rows['_labels'])
    if not pd.isnull(rows[2:]).all():
        query=query+"""{"""
        for i in nodedf.columns[2:]:
            if not pd.isnull(rows[i]):
                if isinstance(rows[i], str):
                    formattedData = cleanString(rows[i])
                else:
                    formattedData=rows[i]
                query=query+i+""":"{0}",""".format(formattedData)
        query=query[:-1]+"""}"""
    query=query+""")
"""
    count+=1
    totalcount+=1
    if count == batchSize or totalcount == totalSize:
        query=query+"""return """
        for j in range(count):
            query=query+"""id(x{}), """.format(j)
        query=query[:-2]
        fullarr = fullarr+read_cypher_query(graph, query).values()[0]
        query=""""""
        count=0
        batchCount+=1
        print(batchCount,"/",numBatch,"Batches Completed")
    

nodedf['mapID']=np.array(fullarr)

##################### Creation of Relations ############################
print("Creating Relations...")
count=0
lineCount = 0
total = len(rlsdf)
numOfLines = len(rlsdf)
for index, rows in rlsdf.iterrows():
    query=""""""
    newStart = getNewID(rows['_start'])
    newEnd = getNewID(rows['_end'])
    query = query+"""MATCH (x{0}) WHERE id(x{0})={1}
MATCH (x{2}) WHERE id(x{2})={3}
MERGE (x{0})-[:{4}""".format(count, newStart, count+1, newEnd, rows['_type'])
    if not pd.isnull(rows[3:]).all():
        query=query+"""{"""
        for i in rlsdf.columns[3:]:
            if not pd.isnull(rows[i]):
                query=query+i+""":"{0}",""".format(rows[i])
        query=query[:-1]+"""}"""
    query=query+"""]->(x{0})""".format(count+1)
    read_cypher_query(graph, query)
    lineCount+=1
    print(lineCount,"/",numOfLines,"Relations Created")
    count+=2

print(totalcount, "Nodes Created; ", lineCount, "Relations Created")
print("Done")