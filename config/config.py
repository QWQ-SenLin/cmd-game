import json , os

def loda_config():
    global OutWay , Path
    config = None
    Path = os.getcwd()
    with open(Path + '\\config\\config.json' , "r" , encoding = "utf-8") as file:
        config = json.loads(file.read())

    OutWay = config["out_way"]
    # print : 慢 2s
    # sys   : 比较稳定，效率和print差不多，略快  1.8s
    # c-exe : 垃圾  4s