# XFaaS specific imports
from serwo_objects import SerWOObject
import networkx as nx
from networkx.readwrite import json_graph
import cpuinfo
import subprocess as sp
import platform
import logging

def handler(body):

    graph = nx.adjacency_graph(body.get("graph"))
 
    # result = nx.pagerank(graph)

    # return {
    #     'function': 'Pagerank',
    #     'result': result,
    # }
    return {
        'function': 'Pagerank',
        'result': "dummy",
    }


def user_function(xfaas_object) -> SerWOObject:
    try:
        body = xfaas_object.get_body()
        returnbody = handler(body)
        print("Request has been processed")
        return SerWOObject(body=returnbody)
    except Exception as e:
        print(e)
        logging.info(e)
        raise Exception("[SerWOLite-Error]::Error at user function",e)


def main(args):
    print("------ Entered Pagerank ------")
    # print(args)
    print("------------------")

    resp_body = user_function(SerWOObject(body=args["body"])).get_body()
    metadata = SerWOObject(body=args).get_metadata()
    response = dict(statusCode=200, body=resp_body, metadata=metadata)

    return response
