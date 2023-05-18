import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from query import get_schema, answer_question

app = Flask(__name__)
slack_token = os.getenv('SLACK_TOKEN')

# Create a WebClient instance
client = WebClient(token=slack_token)

# Get schema
my_schema = get_schema()

# Slash command endpoint
@app.route("/test", methods=["POST"])
def hello():
    data = request.form
    channel_id = data.get("channel_id")

    try:
        # Send a message to the channel
        client.chat_postMessage(channel=channel_id, text=my_schema)

    except SlackApiError as e:
        print(f"Error posting message to Slack: {e.response['error']}")

    return "", 200

if __name__ == "__main__":
    app.run(debug=True, port=5002)
