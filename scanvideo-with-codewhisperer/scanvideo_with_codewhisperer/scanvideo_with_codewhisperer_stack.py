from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_s3 as s3,
    aws_sns as sns,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_s3_notifications,
    aws_sns_subscriptions as subscriptions,

  )

from constructs import Construct

class ScanvideoWithCodewhispererStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
                    
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++ Create an Amazon S3 Bucket +++++++++++++++++++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        
        #cdk code to amazon s3 bucket named "video-storage"
        video_storage = s3.Bucket(self, "video-storage",
                                       versioned=False,
                                       removal_policy=RemovalPolicy.DESTROY,
                                       auto_delete_objects=True)

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #+++++++++ Create an Amazon SNS topic +++++++++++++++++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html
        #https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_sns/Topic.html
        #https://pypi.org/project/aws-cdk.aws-sns-subscriptions/

        
        #cdk code to sns topic named "scan-video-topic"
        scan_video_topic = sns.Topic(self, "scan-video-topic")
                                        

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++ Role Rekognition to be able to publish on SNS +++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #cdk code to role to grant to assume amazon rekognition
        rekognition_role = iam.Role(self, "rekognition-role",
                                    assumed_by=iam.ServicePrincipal("rekognition.amazonaws.com"))
        
        #cdk code to add a policy to the role to allow rekognition to publish sns
        rekognition_role.add_to_policy(iam.PolicyStatement(
            actions=["sns:Publish"],
            resources=[scan_video_topic.topic_arn]
        ))

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++The Lambda function invokes Amazon Rekognition for content moderation on videos ++++++++++++++++
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #cdk code to create a lambda function to scan the video
        scan_video_lambda = lambda_.Function(self, "lambda_invokes_Rekognition",
                                              runtime=lambda_.Runtime.PYTHON_3_8,
                                              handler="lambda_function.lambda_handler",
                                              code=lambda_.Code.from_asset("./lambdas_code/lambda_invokes_rekognition"),
                                              timeout=Duration.seconds(300),description = "Invokes Amazon Rekognition",
                                              environment={
                                                  "SNS_TOPIC_ARN": scan_video_topic.topic_arn,
                                                  "VIDEO_STORAGE_BUCKET": video_storage.bucket_name,
                                                  "REKOGNITION_ROLE_ARN": rekognition_role.role_arn
                                                  }
        )

        #cdk code to add a permission to the lambda function to allow it to read from the video storage
        video_storage.grant_read(scan_video_lambda)
        #cdk code to add a lambda function role policy to invoke amazon rekognition StartContentModeration 
        scan_video_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["rekognition:StartContentModeration", "rekognition:GetContentModeration"],
            resources=["*"]
            ))
        
        #cdk code to amazon s3 bucket event to trigger lambda function LambdaDestination
        video_storage.add_event_notification(s3.EventType.OBJECT_CREATED,
                                              aws_s3_notifications.LambdaDestination(scan_video_lambda),
                                              s3.NotificationKeyFilter(prefix="videos/"))
        
        #cdk code to add a lambda function role policy passrole action to resources rekognition
        scan_video_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["iam:PassRole"],
            resources=[rekognition_role.role_arn]
            ))

        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++The Lambda function invokes Amazon Rekognition for content moderation on videos ++++++++++++++++
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         
        
        #cdk code to create a lambda function to process result of content moderation
        process_result_lambda = lambda_.Function(self, "lambda_process_rekognition",
                                                  runtime=lambda_.Runtime.PYTHON_3_8,
                                                  handler="lambda_function.lambda_handler",
                                                  timeout=Duration.seconds(300),description = "Process Amazon Rekognition ",
                                                  code=lambda_.Code.from_asset("./lambdas_code/lambda_process_rekognition"),
                                                  environment={
                                                      "BUCKET_NAME": video_storage.bucket_name
                                                      }
                                                      )
        #cdk code to add a permission to the lambda function to allow it write to the video storage
        video_storage.grant_write(process_result_lambda)
        #cdk code to add a lambda function role policy to invoke amazon rekognition GetContentModeration 
        process_result_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["rekognition:GetContentModeration"],
            resources=["*"]
            ))
        
        #cdk code to add a LambdaSubscription 
        scan_video_topic.add_subscription(subscriptions.LambdaSubscription(process_result_lambda))

    
        
