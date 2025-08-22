import json

import boto3
from config import config


class BedrockService:
    def __init__(self):
        self.bedrock_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_REGION,
        )
        self.model_id = config.CLAUDE_MODEL_ID

    def generate_response(self, message: str) -> str:
        """Generate response using available model"""
        try:
            # Check if using Claude or Titan model
            if "claude" in self.model_id.lower():
                return self._generate_claude_response(message)
            elif "titan" in self.model_id.lower():
                return self._generate_titan_response(message)
            else:
                return "Unknown model type configured."

        except Exception as e:
            return f"I apologize, but I'm having trouble accessing the AI service right now. Error: {str(e)}"

    def _generate_claude_response(self, message: str) -> str:
        """Generate response using Claude model"""
        prompt = f"""You are a helpful AI assistant for Azercell, Azerbaijan's leading mobile operator.

        Here's some information about Azercell:
        - Azercell is Azerbaijan's first and largest mobile network operator
        - Founded in 1996, serving millions of customers
        - Offers 4G/5G mobile services, internet, and digital solutions
        - Known for innovation and quality network coverage
        - Headquarters in Baku, Azerbaijan

        User question: {message}

        Please provide a helpful response about Azercell services or general assistance."""

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = self.bedrock_client.invoke_model(
            body=json.dumps(body),
            modelId=self.model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]

    def _generate_titan_response(self, message: str) -> str:
        """Generate response using Amazon Titan model"""
        prompt = f"""You are a helpful AI assistant for Azercell, Azerbaijan's leading mobile operator.

Azercell Information:
- Founded in 1996, Azerbaijan's first mobile operator
- Serves millions of customers nationwide
- Offers 4G/5G networks, mobile internet, digital solutions
- Headquarters in Baku, Azerbaijan
- Known for reliable coverage and innovation

User Question: {message}

Please provide a helpful response about Azercell services or general assistance:"""

        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 1000,
                "stopSequences": [],
                "temperature": 0.7,
                "topP": 0.9,
            },
        }

        response = self.bedrock_client.invoke_model(
            body=json.dumps(body),
            modelId=self.model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        return response_body["results"][0]["outputText"]

    def health_check(self) -> bool:
        """Check if Bedrock service is accessible"""
        try:
            # Simple test call
            test_response = self.generate_response("Hello")
            return len(test_response) > 0
        except Exception:
            return False
