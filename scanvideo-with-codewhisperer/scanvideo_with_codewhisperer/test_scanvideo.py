from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,

    )

from constructs import Construct

class ScanvideoWithCodewhispererStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #cdk code to amazon s3 bucket named "video-storage"
        video_storage = s3.Bucket(self, "video-storage",
                                       versioned=False,
                                       removal_policy=RemovalPolicy.DESTROY,
                                       auto_delete_objects=True)
        
        #cdk code to sns topic named "scan-video-topic"
        scan_video_topic = sns.Topic(self, "scan-video-topic")
        
        #cdk code to role to grant to assume amazon rekognition
        rekognition_role = iam.Role(self, "rekognition-role",
                                    assumed_by=iam.ServicePrincipal("rekognition.amazonaws.com"))
        
        #cdk code to add a policy to the role to allow rekognition to publish sns
        rekognition_role.add_to_policy(iam.PolicyStatement(
            actions=["sns:Publish"],
            resources=[scan_video_topic.topic_arn]
        ))

        

        

                         
                         

        













        
