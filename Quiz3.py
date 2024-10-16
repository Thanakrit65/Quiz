from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest,
    TextMessage, QuickReply, QuickReplyItem, MessageAction,
    TemplateMessage, ButtonsTemplate, CarouselTemplate, CarouselColumn,
    URIAction
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from typing import Callable, Dict

app = Flask(__name__)


CHANNEL_ACCESS_TOKEN = 'ywbRGQlnzStCkk3RBEP+V+QVT+lbOe7OtOxRxfkzBinHbE2mq5rDYfuGmMyvkiouSmKXxIjbth0+gVqKcNyksBXSVDgZ7ju1zTB8yNLpVIhQ+usNNYIFwkpo9O12HpKgUvg9U+OldqmLblx8pWfhiAdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '4dd03d6c9c52200c7b92173733749743'


configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

def send_reply(reply_token: str, messages: list) -> None:
    """ฟังก์ชันตอบกลับผู้ใช้"""
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
    """ตอบกลับด้วยText"""
    def handler(event: MessageEvent) -> None:
        send_reply(event.reply_token, [TextMessage(text=text)])
    return handler

def quickreply_handler(event: MessageEvent) -> None:
    """ตอบกลับด้วยQuickReply"""
    quick_reply = QuickReply(items=[
        QuickReplyItem(action=MessageAction(label="Hello", text="1")),
        QuickReplyItem(action=MessageAction(label="Nice", text="2")),
        QuickReplyItem(action=MessageAction(label="Quickreply", text="3")),
        QuickReplyItem(action=MessageAction(label="Button", text="4")),
        QuickReplyItem(action=MessageAction(label="Carousel", text="5"))
    ])
    send_reply(event.reply_token, [TextMessage(text="เลือกว่าให้บอทตอบแบบใด:", quick_reply=quick_reply)])

def button_template_handler(event: MessageEvent) -> None:
    """ตอบกลับด้วย button template"""
    buttons_template = TemplateMessage(
        alt_text="Button Template",
        template=ButtonsTemplate(
            title="Menu",
            text="Please select an option",
            actions=[
                MessageAction(label="Say Hello", text="Hello!"),
                URIAction(label="Visit our website", uri="http://example.com")
            ]
        )
    )
    send_reply(event.reply_token, [buttons_template])

def carousel_template_handler(event: MessageEvent) -> None:
    """ตอบกลับด้วย carousel template"""
    carousel_template = TemplateMessage(
        alt_text="Carousel Template",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item1.jpg",
                    title="This is item 1",
                    text="Description for item 1",
                    actions=[
                        MessageAction(label="More Info", text="More info about item 1")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item2.jpg",
                    title="This is item 2",
                    text="Description for item 2",
                    actions=[
                        MessageAction(label="More Info", text="More info about item 2")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item3.jpg",
                    title="This is item 3",
                    text="Description for item 3",
                    actions=[
                        MessageAction(label="More Info", text="More info about item 3")
                    ]
                )
            ]
        )
    )
    send_reply(event.reply_token, [carousel_template])

def default_handler(event: MessageEvent) -> None:
    """ตอบกลับด้วยข้อความค่าเริ่มต้นเมื่อผู้ใช้ส่งข้อความไม่ตรงเงื่อนไข"""
    send_reply(event.reply_token, [TextMessage(text="ส่งเลข 1 ถึง 5 เพื่อให้แชทบอทตอบกลับต่อไปนี้\n1 ตอบว่า good \n2 ตอบว่า nice\n3 เลือกquickreply\n4 button\n5 carousel")])

# Map รูปแบบการตอบกลับตามข้อความที่ผู้ใช้ส่งมา
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