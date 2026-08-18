# Two Environment Variables:
# PROCESSING_LAMBDA_NAME: endpoint_test_function
# BUCKET_NAME: index.html's bucket

import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_client = boto3.client('lambda')


def lambda_handler(event, context):
    logger.info('Event: %s', json.dumps(event))

    processing_lambda_name = os.environ["PROCESSING_LAMBDA_NAME"]
    lambda_client.invoke(
        FunctionName=processing_lambda_name,
        InvocationType='Event',
        Payload=json.dumps(event)
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({'message': 'Request received, processing started'})
    }
