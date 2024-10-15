from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction,
    TemplateMessage,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    URIAction,
    PostbackAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='ywbRGQlnzStCkk3RBEP+V+QVT+lbOe7OtOxRxfkzBinHbE2mq5rDYfuGmMyvkiouSmKXxIjbth0+gVqKcNyksBXSVDgZ7ju1zTB8yNLpVIhQ+usNNYIFwkpo9O12HpKgUvg9U+OldqmLblx8pWfhiAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4dd03d6c9c52200c7b92173733749743')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if event.message.text == "1":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="good")]
                )
            )
        elif event.message.text == "2":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="nice")]
                )
            )
        elif event.message.text == "3":
            quick_reply = create_quickreply_obj()
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="Here are some quick options:", quick_reply=quick_reply)]
                )
            )
        elif event.message.text == "4":
            buttons_template = create_button_template()
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[buttons_template]
                )
            )
        elif event.message.text == "5":
            carousel_template = create_carousel_template()
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[carousel_template]
                )
            )
        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )

def create_quickreply_obj():
    return QuickReply(
        items=[
            QuickReplyItem(
                action=MessageAction(label="Send photo", text="Send photo")
            ),
            QuickReplyItem(
                action=MessageAction(label="Open camera", text="Open camera")
            )
        ]
    )

def create_button_template():
    return TemplateMessage(
        alt_text="Button Template",
        template=ButtonsTemplate(
            title="Menu",
            text="Please select an option",
            actions=[
                PostbackAction(
                    label="Buy",
                    data="action=buy&itemid=1"
                ),
                MessageAction(
                    label="Say Hello",
                    text="Hello!"
                ),
                URIAction(
                    label="Visit our website",
                    uri="http://example.com"
                )
            ]
        )
    )

def create_carousel_template():
    return TemplateMessage(
        alt_text="Carousel Template",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item1.jpg",
                    title="This is item 1",
                    text="Description for item 1",
                    actions=[
                        PostbackAction(
                            label="Buy Item 1",
                            data="action=buy&itemid=1"
                        ),
                        MessageAction(
                            label="More Info",
                            text="More info about item 1"
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item2.jpg",
                    title="This is item 2",
                    text="Description for item 2",
                    actions=[
                        PostbackAction(
                            label="Buy Item 2",
                            data="action=buy&itemid=2"
                        ),
                        MessageAction(
                            label="More Info",
                            text="More info about item 2"
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/item3.jpg",
                    title="This is item 3",
                    text="Description for item 3",
                    actions=[
                        PostbackAction(
                            label="Buy Item 3",
                            data="action=buy&itemid=3"
                        ),
                        MessageAction(
                            label="More Info",
                            text="More info about item 3"
                        )
                    ]
                )
            ]
        )
    )

if __name__ == "__main__":
    app.run()