#!/usr/bin/python
import sys
import logging
import json
from database.queries import logModuleIssue
from responseIO import returnResponse, errString
from utils.validation import postValidate

# POST METHOD USED TO CREATE MODULE ISSUE
def post(conn, header, body, publisherId, userId, headers, retVal, logger):
	errorsList = []
	try:
		## Using JSON.loads function to load the post body (JSON format) into a dictionary called params
		params = json.loads(body)
	except Exception as e:
		retVal = errString('{}'.format(e), retVal)
		return returnResponse(400, json.dumps(retVal), headers, logger, conn)
	
	## If the params dictionary is empty throw an error
	if params is None:
		retVal = errString("Empty HTTP Body or Invalid Structure", retVal)
		return returnResponse(400, json.dumps(retVal), headers, logger, conn)

	for items in params:
		## Create a new dictionary for validation of params JSON and initialize all values. 
		modDict = {}

		## Get all values from the params dict, and parse them into the dictionary for validation
		try:
			modDict['entity'] = items.get('entity', None)
			modDict['module'] = items.get('module', None)
			modDict['process'] = items.get('process', None)
			modDict['level'] = items.get('level', 'ERROR')
			modDict['issue'] = items.get('issue', None)
			modDict['description'] = items.get('description', None)
			modDict['pid'] = publisherId
			modDict['uid'] = userId

		except Exception as e:
			retVal = errString("Error!: {}".format(e), retVal)
			return returnResponse(400, json.dumps(retVal), headers, logger, conn)
		
		## postValidate returns back a set of all invalid parameters within modDict
		modCheck = postValidate(modDict)
		if not modCheck:
			errorsList.append(modCheck)
			retVal['message'] = "Invalid: {}".format(', '.join(errorsList))
			return returnResponse(400, json.dumps(retVal), headers, logger, conn)
		else:
			# if no errors are found log and return success
			oFlag = logModuleIssue(conn, modDict, logger)
			if oFlag is not None:
				retVal["message"] = "Issue successfully logged under id: {}".format(oFlag)
				return returnResponse(200, json.dumps(retVal), headers, logger, conn)
			else:
				retVal['message'] = "Whoops, something went wrong at our end! Please try again later!"
				return returnResponse(502, json.dumps(retVal), headers, logger, conn)
