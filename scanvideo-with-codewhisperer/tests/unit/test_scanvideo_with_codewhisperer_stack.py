import aws_cdk as core
import aws_cdk.assertions as assertions

from scanvideo_with_codewhisperer.scanvideo_with_codewhisperer_stack import ScanvideoWithCodewhispererStack

# example tests. To run these tests, uncomment this file along with the example
# resource in scanvideo_with_codewhisperer/scanvideo_with_codewhisperer_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ScanvideoWithCodewhispererStack(app, "scanvideo-with-codewhisperer")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
