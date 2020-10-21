#!/usr/bin/python
import sys
import logging
from rdsConfig import getDbConfig
import json
import config
from responseIO import returnResponse, errString
from keyCheck import verifyPublisher, verifyUsers
import datetime
from modules.post import post
from dbCommons import createModuleIssue

## Creating a lambda handler function which serves as a response to an event
def lambda_handler(event, context):

    ## Creation of retVal Dict which will act as the body of the returnResponse function (JSON)
    retVal = {}
    headers = {}

    ## Initalize Logger
    logger = config.getLogger()

    ## Initalize DB connection
    conn = getDbConfig(logger)
    if conn is None:
        retVal['message'] = "Whoops, something went wrong at out end! Please try again later!"
        return returnResponse(502, json.dumps(retVal), headers, logger)

    ## Check for HTTP Request completion 
    try:
        qsp = event['queryStringParameters']
        header = {k.lower(): v for k, v in event['headers'].items()}
        httpMethod = str(event['httpMethod'])
    except Exception as e:
        retVal['message'] = "Invalid / Incomplete HTTP Request"
        return returnResponse(400, json.dumps(retVal), headers, logger, conn)
        
    # Debug the event
    logger.debug('Event = {}'.format(json.dumps(event)))

    ## Check if publisher key has been parsed in as part of the header
    publisherId = verifyPublisher(conn, header, logger)
    if publisherId is None:
        retVal['message'] = "Error: PublisherKey invalid or Missing"
        return returnResponse(403, json.dumps(retVal), headers, logger, conn)

    ## Validate user based on Infomo user-Key
    userId = verifyUsers(conn, header, logger)

    if httpMethod == 'POST':
        return post(conn, header, event['body'], publisherId, userId, headers, retVal, logger)
    else:
        retVal = errString("Invalid Request!", retVal)
        return returnResponse(403, json.dumps(retVal), headers, logger, conn)