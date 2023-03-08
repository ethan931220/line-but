from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('TAcQb6f3AmePfbwigjkehcUfQ7tsFnn10pv7ZKrp2QAmHM6qRAzW/D/h3wg+fSKnmQfo19+JclgfBmjJ8ktJ6Yq/7u2nbs/+/Y0NKuz9I6BFbgBJJc7I5hwMFI48Wd6Le3oQFNc+HUW6WYDpemMSkwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2d04ba8681d8e838b5c9900ac5d78650')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
