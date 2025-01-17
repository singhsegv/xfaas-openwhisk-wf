from serwo_objects import SerWOObject
import logging
import networkx as nx
from networkx.readwrite import json_graph
# import cpuinfo
# import subprocess as sp
# import platform

def handle(body):
 
    graph = nx.adjacency_graph(body.get("graph"))

    startVertex = body.get("startVertex")
    if startVertex == None:
        startVertex = 0

    bfs_list = nx.bfs_successors(graph,startVertex)

    bfs = []
    i = 0
    for nd in bfs_list:
        if i == 0:
            bfs.append(nd[0])
        for e in nd[1]:
            bfs.append(e)
        i += 1

    returnbody = {
        "function": "BFS",
        "result": bfs,
    }

    return returnbody

def user_function(xfaas_object) -> SerWOObject:
    try:
        body = xfaas_object.get_body()
        returnbody = handle(body)
        return SerWOObject(body=returnbody)
    except Exception as e:
        print(e)
        logging.info(e)
        raise Exception("[SerWOLite-Error]::Error at user function",e)


def main(args):
    print("------ Entered BFT ------")
    # print(args)
    print("------------------")

    resp_body = user_function(SerWOObject(body=args["body"])).get_body()
    metadata = SerWOObject(body=args).get_metadata()
    response = dict(statusCode=200, body=resp_body, metadata=metadata)

    return response
