

from slack_sdk import WebClient

# SLACK_CHANNEL_ID = '****'
SLACK_CHANNEL_ID = "****"
SLACK_TOKEN = "****"

client = WebClient(SLACK_TOKEN)
response = client.conversations_history(channel=SLACK_CHANNEL_ID)
messages = response.get('messages')

print(messages)
