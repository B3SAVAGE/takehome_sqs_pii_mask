import datetime
import json
import pandas as pd
import boto3


def read(endpoint_url, queue_name):
    # create the boto3 client to interface with the SQS queue
    sqs_queue = boto3.client('sqs', endpoint_url=str(endpoint_url))
    queue_url = str(endpoint_url) + "/queue/" + str(queue_name)
    response = ""
    # start consuming the SQS queue, try-except for logging
    try:
        response = sqs_queue.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=15,
            WaitTimeSeconds=2
        )
    except:
        print("Reading queue failed, check the queueURL")
    messages = response.get('Messages', [])


    # get the message body and transform into a dataframe
    msg_objs = []
    for message in messages:
        body_obj = message.get('Body')
        body = json.loads(body_obj)

        msg_objs.append(body)
        # delete each message after it is processed
        sqs_queue.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

    df = pd.DataFrame.from_dict(msg_objs)
    df.to_csv("test.csv")
    return df

