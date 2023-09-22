from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_iam,
    aws_s3 as s3,
    aws_s3_notifications,
    aws_sns as sns,
    aws_lambda,
    aws_sns_subscriptions as subscriptions,

    )

from constructs import Construct

class ScanvideoWithCodewhispererStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        REGION_NAME = self.region
                    
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++ Create an Amazon S3 Bucket +++++++++++++++++++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        
        #cdk code to amazon s3 bucket named "video-storage"
        my_bucket = s3.Bucket(self, "video-storage",
                        versioned=False,
                        removal_policy=RemovalPolicy.DESTROY,
                        auto_delete_objects=True)

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #+++++++++ Create an Amazon SNS topic +++++++++++++++++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html
        #https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_sns/Topic.html
        #https://pypi.org/project/aws-cdk.aws-sns-subscriptions/

        
        #code to create a cdk sns topic
        my_topic_rekognition = sns.Topic(self, "my_topic_rekognition",
                                        display_name="my_topic_rekognition",
        )
                                        
        #arn topic is
        SNS_ARN_rekognition = my_topic_rekognition.topic_arn

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++ Role Rekognition to be able to publish on SNS +++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #code to create a cdk role to gain access to amazon rekogntion 

        rekognitionServiceRole = aws_iam.Role( self, "RekognitionServiceRole", assumed_by=aws_iam.ServicePrincipal('rekognition.amazonaws.com'))
        
        #code to grant access to amazon rekognition publish a sns 
       
        rekognitionServiceRole.add_to_policy(
            aws_iam.PolicyStatement(
                actions=["sns:Publish"], 
                resources=[my_topic_rekognition.topic_arn])
                )
         #arn topic isc

        SNS_ROLE_ARN_REKO = rekognitionServiceRole.role_arn


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++The Lambda function invokes Amazon Rekognition for content moderation on videos ++++++++++++++++
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        lambda_invokes_Rekognition= aws_lambda.Function(self, "lambda_invokes_Rekognition",
                                    handler = "lambda_function.lambda_handler",
                                    timeout = Duration.seconds(300),
                                    runtime = aws_lambda.Runtime.PYTHON_3_8,
                                    memory_size = 256, description = "Invokes Amazon Rekognition ",
                                    code = aws_lambda.Code.from_asset("./lambdas_code/lambda_invokes_rekognition"),
                                    environment = {
                                        'ENV_SNS_REKOGNITION': SNS_ARN_rekognition,
                                        "ENV_SNS_ROLE_ARN_REK":SNS_ROLE_ARN_REKO}
                                    )

        lambda_invokes_Rekognition.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=["rekognition:*"], 
                resources=['*'])
              )
        
        lambda_invokes_Rekognition.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions =['iam:PassRole'],
                resources =[rekognitionServiceRole.role_arn]  
            )
        )

        #grant access to the bucket to the lambda function
        bucket.grant_read(lambda_invokes_Rekognition) 
        notification = aws_s3_notifications.LambdaDestination(lambda_invokes_Rekognition)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification) 

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++The Lambda function invokes Amazon Rekognition for content moderation on videos ++++++++++++++++
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        lambda_process_Rekognition= aws_lambda.Function(self, "lambda_process_Rekognition",
                                    handler = "lambda_function.lambda_handler",
                                    timeout = Duration.seconds(300),
                                    runtime = aws_lambda.Runtime.PYTHON_3_8,
                                    memory_size = 256, description = "Process Amazon Rekognition ",
                                    code = aws_lambda.Code.from_asset("./lambdas_code/lambda_process_Rekognition"),
                                    environment = {
                                        'ENV_REGION_NAME': REGION_NAME,
                                        "BUCKET_KEY_MODERATION" :bucket_key_moderation,
                                        "BUCKET_NAME":bucket.bucket_name,
                                        "ENV_SNS_REKOGNITION":SNS_ARN_rekognition,}
                                    )
        

        lambda_process_Rekognition.add_to_role_policy(
            aws_iam.PolicyStatement( 
                actions=["rekognition:*"], 
                resources=['*']))

        lambda_process_Rekognition.add_to_role_policy(
            aws_iam.PolicyStatement(
                actions=["sns:*"], 
                resources=['*']))
        
        bucket.grant_write(lambda_process_Rekognition) 
        
        my_topic_rekognition.add_subscription(subscriptions.LambdaSubscription(lambda_process_Rekognition))