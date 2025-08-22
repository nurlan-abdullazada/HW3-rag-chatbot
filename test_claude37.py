import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Claude 3.7 Sonnet with inference profile...")

client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 200,
    "messages": [
        {
            "role": "user", 
            "content": "Hello! Please tell me about Azercell telecommunications company in Azerbaijan."
        }
    ]
}

try:
    response = client.invoke_model(
        body=json.dumps(body),
        modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",  # Using inference profile
        accept='application/json',
        contentType='application/json'
    )
    
    result = json.loads(response.get('body').read())
    print("✅ SUCCESS! Claude 3.7 Sonnet is working:")
    print("Response:", result['content'][0]['text'])
    
except Exception as e:
    print(f"❌ ERROR: {e}")
