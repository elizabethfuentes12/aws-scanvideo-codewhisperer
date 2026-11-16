# AGENTS.md

## What this is
CDK (Python) demo of video content moderation: an MP4 uploaded to S3 triggers a Lambda that starts an Amazon Rekognition content-moderation job; when it finishes, a second Lambda stores the results in S3. Written in 2023 as a step-by-step guide for building with AWS CodeWhisperer (now part of Amazon Q Developer).

## Structure
- `scanvideo-with-codewhisperer/app.py` – CDK entrypoint (`ScanvideoWithCodewhispererStack`).
- `scanvideo-with-codewhisperer/scanvideo_with_codewhisperer/scanvideo_with_codewhisperer_stack.py` – S3 buckets, SNS topic + IAM role for Rekognition, two Lambdas, notifications.
- `scanvideo-with-codewhisperer/scanvideo_with_codewhisperer/test.py` – alternative stack draft (not referenced by `app.py`).
- `scanvideo-with-codewhisperer/lambdas_code/lambda_invokes_rekognition/` – `start_content_moderation`.
- `scanvideo-with-codewhisperer/lambdas_code/lambda_process_rekognition/` – `get_content_moderation` + write results.
- `README.md` – Spanish walkthrough; it embeds the stack code, keep snippets in sync with the real stack.

## Commands
```bash
cd scanvideo-with-codewhisperer
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk synth      # CDK CLI: npm install -g aws-cdk
cdk deploy     # creates real resources (S3, Lambda, SNS, IAM)
```

## Dependencies
- `aws-cdk-lib==2.277.0`, `constructs>=10,<11`.
- Lambda runtime **Python 3.13**; handlers use only `boto3`/`json`/`os`.

## Recent changes
- 2026-11: Lambda runtime `python3.8`/`python3.7` -> `python3.13` (stack, `test.py`, README snippets); `aws-cdk-lib` 2.94.0 -> 2.277.0. Verified with `cdk synth` (3 Python functions render `python3.13`; the `nodejs24.x` one is the CDK-managed S3 notification handler) and by importing both handlers under Python 3.13. Not deployed.
