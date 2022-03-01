import boto3


from traffic_speed_prediction.util.config.ReadConfig import read_secrets

# Connection to AWS
resource_db = boto3.resource(
    service_name='dynamodb',
    aws_access_key_id = read_secrets()["aws_access_key_id"],
    aws_secret_access_key = read_secrets()["aws_secret_access_key"],
    region_name = read_secrets()["region_name"]
)

# Dynamodb table
table = resource_db.Table('***')

# Put item in table
table.put_item(
        # Data to be inserted
        Item={
            '***': '***',
            '***': '***',
        }
)