# XFaaS specific imports
from serwo_objects import SerWOObject
import networkx as nx
# function specific imports
import logging
from networkx.readwrite import json_graph
import json
import cpuinfo
import subprocess as sp
import platform

def handler(event):

    size = event.get('size', 64)
    for key in event.keys():
        if key == "startVertex":
            startVertex = event.get('startVertex')
            break
    else:
        startVertex = None

    if "graph_type" in event:
        graph_type = event.get("graph_type")
    else:
        graph_type = "complete"

    if graph_type.lower() == "barabasi":
        edges = event.get('edges')
        graph = nx.barabasi_albert_graph(size,edges)
    elif graph_type.lower() == "binomial_tree":
        graph = nx.binomial_tree(size)
    elif graph_type.lower() == "power_law":
        edges = event.get('edges')
        graph = nx.powerlaw_cluster_graph(size,edges,p=0.5)
    else:
        graph = nx.complete_graph(size)

    graph_dict = json_graph.adjacency_data(graph)
    returnbody = {
        "graph": graph_dict,
        "startVertex": startVertex
    }
    
    return returnbody


def user_function(xfaas_object) -> SerWOObject:
    try:
        body = xfaas_object.get_body()
        result = handler(body)
        print("Request has been processed")
        return SerWOObject(body=result)
    except Exception as e:
        print(e)
        logging.info(e)
        raise Exception("[SerWOLite-Error]::Error at user function",e)


def main(args):
    # from approximate understanding of the codebase
    # print("------ Args ------")
    # print(args)
    # print("------------------")
    
    resp_body = user_function(SerWOObject(body=args)).get_body()
    metadata = SerWOObject(body=args).get_metadata()
    response = dict(statusCode=200, body=resp_body, metadata=metadata)

    print("------ Resp Gen ------")
    print(response)
    print("------------------")
    
    return response
