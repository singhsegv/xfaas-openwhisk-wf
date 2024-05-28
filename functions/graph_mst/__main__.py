# XFaaS specific imports
from serwo_objects import SerWOObject
import networkx as nx
from networkx.readwrite import json_graph
import logging
import cpuinfo
import subprocess as sp
import platform

def handle(body):
    graph = nx.adjacency_graph(body.get("graph"))


    mst = nx.minimum_spanning_tree(graph)
    result = list(mst.edges)

    returnbody = {
        "function": "MST",
        "result": result,
    }
    return returnbody


def user_function(xfaas_object):
    try:
        body = xfaas_object.get_body()
        returnbody = handle(body)
        return SerWOObject(body=returnbody)
    except Exception as e:
        print(e)
        logging.info(e)
        raise Exception("[SerWOLite-Error]::Error at user function",e)


def main(args):
    print("------ Entered MST ------")
    # print(args)
    print("------------------")

    resp_body = user_function(SerWOObject(body=args["body"])).get_body()
    metadata = SerWOObject(body=args).get_metadata()
    response = dict(statusCode=200, body=resp_body, metadata=metadata)

    return response
