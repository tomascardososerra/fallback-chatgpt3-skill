from mycroft import FallbackSkill, intent_handler
import requests
import urllib
import json

api_endpoint = "https://api.openai.com/v1/completions"
api_key = [YOUR KEY HERE]
model = "text-davinci-001"

# Define the request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
}

class FallbackChatgpt(FallbackSkill):
    def __init__(self):
        FallbackSkill.__init__(self)

    def initialize(self):
        self.register_fallback(self.handle_fallback_ChatGPT, 8)

    def handle_fallback_ChatGPT(self, message):
        try:
            payload = {
                "model": model,
                "prompt": message.data['utterance'],
                "max_tokens": 2048,
                "temperature": 0.4,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
            response_json = response.json()
            freason = response_json["choices"][0]["finish_reason"]
            self.log.info(freason)
            response = response_json["choices"][0]["text"]
            response = response.replace("\n", ". ")
            response = response.replace("\r", ". ")
            self.speak(response)
            return True
        except:
            self.log.info("error in ChatGPT fallback request")
            return False

def create_skill():
    return FallbackChatgpt()
