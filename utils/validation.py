#!/usr/bin/python
import sys
import logging
import time

# List of exempt mandatory fields for APP
EXEMPTIONS = [
    'pid',
    'uid'
]

# Validation for smooth writing into the DB
def postValidate(modDict):
    errorList = []
    
    for key, param in iter(modDict.items()):
        if key in EXEMPTIONS:
            continue
        if param is None or str(param).strip() == "":
            errorList.append('{} is Missing!'.format(key))
    if not errorList:
        # Insert custom checks below
        if len(modDict['entity']) > 100: errorList.append('entity')
        if len(modDict['module']) > 50: errorList.append('module')
        if len(modDict['process']) > 45: errorList.append('process')
        if modDict['level'] not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']: errorList.append('level')
        if len(modDict['issue']) > 100: errorList.append('issue')
        if len(modDict['description']) > 255: errorList.append('description')

    return errorList