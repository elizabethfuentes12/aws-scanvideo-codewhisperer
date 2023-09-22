from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
  


)
from constructs import Construct
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda

class ScanvideoWithCodewhispererStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #code to create a cdk to a amazon s3 bucket
        bucket = aws_s3.Bucket(
             self, "ScanvideoWithCodewhispererBucket",
             versioned=True, removal_policy=RemovalPolicy.DESTROY,
         )
        
        #code to create a cdk sns topic
        topic = aws_s3.Topic(
            self, "ScanvideoWithCodewhispererTopic"  
        )
        #arn topic is
        topic_arn = topic.topic_arn

        #code to create a cdk role to gain access to amazon rekogntion 
        role = aws_iam.Role(
            self, "ScanvideoWithCodewhispererRole",
            assumed_by=aws_iam.ServicePrincipal("rekognition.amazonaws.com"))
        #code to gain accesso to amazon rekognition publish a SNs topic
        role.add_to_policy(aws_iam.PolicyStatement(
            actions=["sns:Publish"],
            resources=[topic_arn]
            ))
        #arn role is
        role_arn = role.role_arn

        #code to define a lamnbda function in cdk to scan video
        function = aws_lambda.Function(
            self, "ScanvideoWithCodewhispererFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="scanvideo_with_codewhisperer.lambda_handler",
            code=aws_lambda.Code.asset("./scanvideo_with_codewhisperer"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TOPIC_ARN": topic_arn,
                "ROLE_ARN": role_arn
                }
        )
        
        #code to grant access to the lamdba function to the s3 bucket
        bucket.grant_read_write(function)
 
        #code to grant access to amazon rekognition to the lamdba function
        function.add_to_role_policy(aws_iam.PolicyStatement(
            actions=["rekognition:DetectLabels"],
            resources=["*"]
        ))
        
        #code to create a s3 bucket event
        bucket.add_event_notification(
            aws_s3.EventType.OBJECT_CREATED,
            aws_s3.LambdaDestination(function),
        )

        #code to create a cdk lambda function to scan video
        function2 = aws_lambda.Function(
            self, "ScanvideoWithCodewhispererFunction2",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="scanvideo_with_codewhisperer.lambda_handler2",
            code=aws_lambda.Code.asset("./scanvideo_with_codewhisperer"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TOPIC_ARN": topic_arn,
                "ROLE_ARN": role_arn
                }
        )
        
        #code to grant access to the lamdba function to the s3 bucket
        bucket.grant_read_write(function2)
 
        #code to grant access to amazon rekognition to the lamdba function
        function2.add_to_role_policy(aws_iam.PolicyStatement(
            actions=["rekognition:DetectLabels"],
            resources=["*"],
        ))
        #code to a LambdaSubscription the lambda function2 to the sns topic
        topic.add_subscription(subs.LambdaSubscription(function2))
        
        #code to add to role policy to lmabda function gran access to sns notification
        function2.add_to_role_policy(aws_iam.PolicyStatement(
            actions=["sns:*"],
            resources=[topic_arn]
            ))

