# Discord Voice Message Sender

The Voice Message Sender is a Python library that allows you to send voice messages to a Discord channel using a provided user token and channel ID.

## Installation

To use the Voice Message Sender files, follow these steps:

```bash
git clone https://github.com/kaitlek/discord-voicemessage-sender.git # or download the zip with the "Code" button above
cd discord-voicemessage-sender
pip install -r requirements.txt
```

## Usage

1. Create a file named `main.py` in your project directory.

2. Import the `VoiceMessageSender` class from the `voicemessages` module and provide your Discord user token (Can be found by simply running the following in the devtools console), aswell as the channel id in which you want to send the voice message
```javascript
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
```
3.  Use the `SendVoiceMessage` method to send a voice message to the specified Discord channel. Replace `"D:\path\to\your\audio\file.mp3"` with the path to the audio file you want to send.

```python
from voicemessages import VoiceMessageSender

TOKEN = "your_token_here" # Replace with your token
CHANNEL_ID = 123  # Replace with your channel ID

voicemessage = VoiceMessageSender(TOKEN, CHANNEL_ID)
voicemessage.SendVoiceMessage("D:\path\to\your\audio\file.mp3")
```

## Disclaimer

This library is provided as-is and may require additional setup or modifications based on your specific use case. Use it responsibly and in compliance with Discord's terms of service.

`Feel free to modify the text and structure to fit your project's needs. Make sure to provide accurate instructions, replace placeholders with actual values, and provide any additional information that users might find helpful.`