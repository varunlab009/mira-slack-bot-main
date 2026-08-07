from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask
import os

# Initialize Slack app
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Initialize Flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(slack_app)

# Listen to app mentions
@slack_app.event("app_mention")
def handle_mention(body, say, logger):
    try:
        text = body["event"]["text"]
        user = body["event"]["user"]

        # Simple response
        response = f"Hi <@{user}>! 👋 Mira here. I received your message: '{text}'\n\nI'm monitoring your workspace and will help with:\n• Project updates\n• Team coordination\n• Anubhav requests\n• Blocker alerts\n\nPost your issue and I'll get back to you!"

        say(response)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        say("Sorry, something went wrong. Please try again.")

# Health check
@flask_app.route("/health", methods=["GET"])
def health():
    return "OK", 200

# Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(flask_app.request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(host="0.0.0.0", port=port)
