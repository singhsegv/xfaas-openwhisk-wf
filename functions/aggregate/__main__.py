# XFaaS specific imports
from serwo_objects import SerWOObject, SerWOObjectsList
import logging
import cpuinfo
import subprocess as sp
import platform

def aggregate(body, returnbody):
    returnbody["RESULT"][body["function"]] = body["result"]
    return returnbody

def user_function(xfaas_object) -> SerWOObject:
    try:
        returnbody = {}
        returnbody["RESULT"] = {}
        for obj in enumerate(xfaas_object.get_objects()):
            try:
                body = obj.get_body()
                print("------ Body ------")
                print(body)
                aggregate(body, returnbody)
            except:
                pass
        return SerWOObject(body=returnbody)

    except Exception as e:
        print(e)
        logging.info(e)
        raise Exception("[SerWOLite-Error]::Error at user function",e)

def main(args):
    print("------ Entered Aggregate ------")
    print(args)
    print("------------------")

    input = SerWOObjectsList()
    for item in args["value"]:
        input.add_object(SerWOObject(body=item["body"]))

    resp_body = user_function(input).get_body()
    metadata = SerWOObject(body=args).get_metadata()
    response = dict(statusCode=200, body=resp_body, metadata=metadata)

    return response
