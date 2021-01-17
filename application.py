"""
Object detection and image description on LINE bot
"""
from datetime import datetime, timezone, timedelta
import os
import re
import json
import requests
from flask import Flask, request, abort
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FlexSendMessage,
    ImageMessage,
)
from imgur_python import Imgur
from PIL import Image, ImageDraw, ImageFont
import time

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

LINE_SECRET = "7a33ea27fe76abfcb892fe6bab73d3e9"
LINE_TOKEN = "oyrxPFqR4Bq/DUtFNVB0HoZDBMFc+LlVuWtQgW4Rcf7UwMA/ZwZEiNDgQEC/5CjOfODkZJkqoj/QoE+MGcSombZckN07C1uPlLVERXCO+5MVwiDaouEtaXJxPol49+fG5iiyoJMToUbtsAQJxJZdhAdB04t89/1O/w1cDnyilFU="
LINE_BOT = LineBotApi(LINE_TOKEN)
HANDLER = WebhookHandler(LINE_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    # X-Line-Signature: 數位簽章
    signature = request.headers["X-Line-Signature"]
    print(signature)
    body = request.get_data(as_text=True)
    print(body)
    try:
        HANDLER.handle(body, signature)
    except InvalidSignatureError:
        print("Check the channel secret/access token.")
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    url_dict = {
      "TIBAME":"https://www.tibame.com/coursegoodjob/traffic_cli", 
      "HELP":"https://developers.line.biz/zh-hant/docs/messaging-api/",
      "location":"https://line.me/R/nv/location/"}
# 將要發出去的文字變成TextSendMessage
    try:
        url = url_dict[event.message.text.upper()]
        message = TextSendMessage(text=url)
    except:
        message = TextSendMessage(text=event.message.text)
# 回覆訊息
    LINE_BOT.reply_message(event.reply_token, message)
    



@app.route("/")
def hello():
    "hello world"
    return """
        <html>
        <head>
            <title>CEB101</title>
        <head>
        <body>
            <center><h1>HI Bitch</h1></center>
        </body>
        """






    








