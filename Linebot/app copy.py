import os
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest,
    TextMessage, QuickReply, QuickReplyItem, MessageAction,
    TemplateMessage, ButtonsTemplate, CarouselTemplate, CarouselColumn,
    URIAction, PostbackAction
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from typing import Callable, Dict

app = Flask(__name__)

# Load configuration from environment variables
CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET must be set in environment variables")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

def send_reply(reply_token: str, messages: list) -> None:
    """Send a reply to the user."""
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=messages)
        )

def handle_text_message(event: MessageEvent) -> None:
    """Handle text messages based on user input."""
    text = event.message.text
    handler_func = message_handlers.get(text, default_handler)
    handler_func(event)

def simple_text_reply(text: str) -> Callable[[MessageEvent], None]:
    """Create a simple text reply handler."""
    def handler(event: MessageEvent) -> None:
        send_reply(event.reply_token, [TextMessage(text=text)])
    return handler

def quickreply_handler(event: MessageEvent) -> None:
    """Handle quick reply message."""
    quick_reply = QuickReply(items=[
        QuickReplyItem(action=MessageAction(label="Send photo", text="Send photo")),
        QuickReplyItem(action=MessageAction(label="Open camera", text="Open camera"))
    ])
    send_reply(event.reply_token, [TextMessage(text="Here are some quick options:", quick_reply=quick_reply)])

def button_template_handler(event: MessageEvent) -> None:
    """Handle button template message."""
    buttons_template = TemplateMessage(
        alt_text="Button Template",
        template=ButtonsTemplate(
            title="Menu",
            text="Please select an option",
            actions=[
                PostbackAction(label="Buy", data="action=buy&itemid=1"),
                MessageAction(label="Say Hello", text="Hello!"),
                URIAction(label="Visit our website", uri="http://example.com")
            ]
        )
    )
    send_reply(event.reply_token, [buttons_template])

def carousel_template_handler(event: MessageEvent) -> None:
    """Handle carousel template message."""
    carousel_template = TemplateMessage(
        alt_text="Carousel Template",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item1.jpg",
                    title="This is item 1",
                    text="Description for item 1",
                    actions=[
                        PostbackAction(label="Buy Item 1", data="action=buy&itemid=1"),
                        MessageAction(label="More Info", text="More info about item 1")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item2.jpg",
                    title="This is item 2",
                    text="Description for item 2",
                    actions=[
                        PostbackAction(label="Buy Item 2", data="action=buy&itemid=2"),
                        MessageAction(label="More Info", text="More info about item 2")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item3.jpg",
                    title="This is item 3",
                    text="Description for item 3",
                    actions=[
                        PostbackAction(label="Buy Item 3", data="action=buy&itemid=3"),
                        MessageAction(label="More Info", text="More info about item 3")
                    ]
                )
            ]
        )
    )
    send_reply(event.reply_token, [carousel_template])

def default_handler(event: MessageEvent) -> None:
    """Handle default case by echoing the user's message."""
    send_reply(event.reply_token, [TextMessage(text=event.message.text)])

# Map user inputs to handler functions
message_handlers: Dict[str, Callable[[MessageEvent], None]] = {
    "1": simple_text_reply("good"),
    "2": simple_text_reply("nice"),
    "3": quickreply_handler,
    "4": button_template_handler,
    "5": carousel_template_handler
}

@app.route("/callback", methods=['POST'])
def callback():
    """Handle LINE webhook callback."""
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent) -> None:
    """Route incoming messages to appropriate handlers."""
    try:
        handle_text_message(event)
    except Exception as e:
        app.logger.error(f"Error handling message: {str(e)}")
        send_reply(event.reply_token, [TextMessage(text="An error occurred. Please try again later.")])

if __name__ == "__main__":
    app.run(debug=True)