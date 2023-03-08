# Data Engineering Take Home: ETL with an AWS SQS Queue


### Getting Started

1. Clone the repository
2. Make sure you have pip installed as well as at least python 3.10
3. In the terminal run the command **pip install -r requirements.txt** to install all dependencies needed to run this project
4. Now in order to proceed you need docker-compose and docker desktop installed as well as psql, though DataGrip by Jetbrains is a good alternative
5. in the path of the repository cloned, run the command **docker compose up .** to build the database and SQS queue for testing
6. To run the code, all that needs to be done is run the **main.py** file











- #### How would you deploy this application in production?
  
    To deploy this application into  production, I would most likely first deploy a postgres database in the cloud,

    along with an SQS queue. Then I would make a Docker image of my codebase and upload it to AWS ECR.
    
    Depending on expected scale and volume of SQS messages expected to be processed as well as cost constraints

    I would definitely lean towards deploying the application on AWS Batch with Fargate as it is very cost effective for
    
    smaller applications while still allowing room for scaling if the demand grows over time. Another alternative would
    
    be to utilize Step Functions to contain the content of the application's code.
- #### What other components would you want to add to make this production ready?
    
    Some other features that would be nice to add would be a notification system for if reading from the queue failed or
    
    if ingesting data into the database failed. Maybe another cool feature to add would be the ability to read multiple
    
    SQS queues and ingest into multiple database tables.
- #### How can this application scale with a growing dataset?

    This application will scale fairly wel with a growing dataset, as I made sure to use funtions that don't use
    
    nested for loops for more time complexity efficiency. Scaling would most likely depend on the compute power behind

    the applicaiton, and AWS Batch can scale up while having virtually no timeout time.
- #### How can PII be recovered later on?

    Using the Fernet library in python, I generated separate keys for each column needing to be masked. The best way to
    
    recover PII would be to cache/save the keys in a secure format. In a cloud environment I would be using

    tools like Amazon Macie and KMS to encrypt, mask, and decrypt PII when needed, and storing encryption

    keys locally is almost never ideal.

- #### What are the assumptions you made?
    Some assumptions I made is that the data in columns like ip and device_id were standardized and would never change

    format unless some update occured. Another assumption I made was that version_id wasn't meant to be an int because
    
    it was formatted as 'x.x.x' and there isn't a way to format a string with characters like this as an INTEGER datatype
 
    in postgres without causing data integrity issues
