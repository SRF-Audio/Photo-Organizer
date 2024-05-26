import base64
import requests
import logging

class OpenAIHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def enhance_descriptions(self, image_path, keywords):
        try:
            base64_image = self.encode_image(image_path)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Generate a description for this photo. Only respond with the actual description text for the photo. Here are some keywords from AWS Rekognition to influence your description: {', '.join(keywords)}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            enhanced_description = result['choices'][0]['message']['content'][0]['text'].strip()
            logging.info(f"Enhanced description: {enhanced_description}")
            return enhanced_description
        except Exception as e:
            logging.error(f"Error in OpenAI API: {e}")
            return "Failed to generate description"

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
