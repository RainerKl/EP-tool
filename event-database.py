# Aim is to build a database for recording breakouts, episodic pivots for later use in backtesting
# Secondary aim is to study the use of databases via Python

# Currently the code takes a CSV uploaded to S3 and puts it into MySQL 

# We do this on S3
#   pip install boto3

import boto3
import pandas

# Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id = 'AKIAVRSURCNSBHJZQG64',
    aws_secret_access_key = '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',
    region_name = 'eu-central-1'
)
    
# Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id = 'AKIAVRSURCNSBHJZQG64',
    aws_secret_access_key = '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',
    region_name = 'eu-central-1'
)
# Fetch the list of existing buckets
clientResponse = client.list_buckets()
    
# Print the bucket names one by one
print('Printing bucket names...')
for bucket in clientResponse['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')
    
# Create the S3 object
obj = client.get_object(
    Bucket = 'mysql-event-server',
    Key = 'EP.csv'
)
    
# Read data from the S3 object
data = pandas.read_csv(obj['Body'])
    
# Print the data frame
print('Printing the data frame...')
print(data)

