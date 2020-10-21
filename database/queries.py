#!/usr/bin/python
import json
from dbCommons import createModuleIssue

def logModuleIssue(conn, modDict, logger):
    cursorObject = conn.cursor()
    keySet = ', '.join(modDict.keys())
    valueSet = ', '.join('%s' for k in modDict)
    query = """INSERT INTO allmoduleissues ({}) VALUES ({})""".format(keySet, valueSet)
    try:
        cursorObject.execute(query, list(modDict.values()))
        conn.commit()
        rowId = cursorObject.lastrowid
        cursorObject.close()
        return rowId
    except Exception as e:
        cursorObject.close()
        createModuleIssue(conn, "allModuleIssues", "logModuleIssue", e, logger)
        return None