import os
import pathlib
import zipfile

def build_workflow():
    try:
        for folder in os.listdir("./artifacts"):
            if folder.endswith(".zip"):
                os.remove(os.path.join("./artifacts", folder))
    except:
        print("no zip")

    for folder in os.listdir("./functions"):
        func_dir = pathlib.Path("./functions/") / folder

        if not os.path.isdir(func_dir):
            continue

        output_artifact_path = pathlib.Path("./artifacts") / f"{os.path.basename(folder)}.zip"

        with zipfile.ZipFile(output_artifact_path, "w") as f:
            for temp in os.listdir(func_dir):
                final_path = func_dir / temp
                
                if os.path.isdir(final_path):
                    name = os.path.basename(final_path)
                    for item in os.walk(final_path):
                        # leaf node
                        if len(item[1]) == 0:
                            final_name = name
                            final_name += item[0].split(str(final_path))[-1]
                            
                            for filename in item[2]:
                                archive_name = os.path.join(final_name, filename)
                                archive_path = os.path.join(item[0], filename)
                                
                                f.write(archive_path, archive_name)
                else:
                    f.write(final_path, os.path.basename(final_path))
       

def build_composer():
    try:
        os.remove("./artifacts/graph_workflow_composition.json")
    except:
        print("no js")

    composer_input_path = pathlib.Path("./artifacts") / "graph_workflow_composition.js"
    composer_output_path = pathlib.Path("./artifacts") / "graph_workflow_composition.json"
    os.system(f"source ~/.bashrc && compose.js {composer_input_path} -o {composer_output_path}")


def deploy_workflow():
    dag_name = "graphs"
    
    for item in os.listdir("./artifacts"):
        if item.endswith("zip"):
            action_name = f"/guest/{dag_name}/{item.split('.')[0]}"
            os.system(f"wsk -i action delete {action_name}")

    os.system(f"wsk -i action delete /guest/{dag_name}/graphs-composition")

    os.system(f"wsk -i package delete {dag_name}")
    os.system(f"wsk -i package create {dag_name}")
    os.system("""wsk -i package bind /guest/graphs parallel_redis_support --param '$composer' '{\"redis\": {\"uri\": \"redis://owdev-redis.openwhisk.svc.cluster.local:6379\"}}'""")

    # Create actions manually
    for item in os.listdir("./artifacts"):
        if item.endswith("zip"):
            action_name = f"/guest/{dag_name}/{item.split('.')[0]}"
            action_zip_path = os.path.join("./artifacts/", item)
            print(action_name)
            print(action_zip_path)
            print("-------")
            os.system(f"wsk -i action create {action_name} --kind python:3 {action_zip_path} --timeout 300000 --concurrency 10")

    # Create composition
    composition_name = f"/guest/{dag_name}/{dag_name}-composition"
    composer_config_path = pathlib.Path("./artifacts") / "graph_workflow_composition.json"
    os.system(f"source ~/.bashrc && deploy.js {composition_name} {composer_config_path} -w -i")
    # os.system("""wsk -i action update /guest/graphs/graphs-composition --timeout 300000 --concurrency 10 --param '$composer' '{\"redis\": {\"uri\": \"redis://owdev-redis.openwhisk.svc.cluster.local:6379\"}}' --param size 64 --param graph_type complete""")
    # os.system("""wsk -i action update /guest/graphs/graphs-composition --timeout 300000 --concurrency 10 --web true --param size 64 --param graph_type complete""")
 

# def invoke():
#     os.system("wsk -i action invoke /guest/graphs-composition -P input.json")

build_workflow()
build_composer()
deploy_workflow()


# '{"$composer": {"redis": {"uri": "redis://owdev-redis.openwhisk.svc.cluster.local:6379"},"openwhisk": {"ignore_certs": true}},"size": 64,"graph_type": "complete"}'

# --param "$composer" {"redis": {"uri": "redis://owdev-redis.openwhisk.svc.cluster.local:6379"} --param size 64 --param graph_type complete

# wsk -i action update /guest/graphs-composition --param '$composer' '{\"redis\": {\"uri\": \"redis://owdev-redis.openwhisk.svc.cluster.local:6379\"}}' --param size 64 --param graph_type complete

# wsk -i action update /guest/graphs-composition --param size 64 --param graph_type complete