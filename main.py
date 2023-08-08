from voicemessages import VoiceMessageSender

TOKEN = "your_token_here" # Replace with your token
CHANNEL_ID = 123  # Replace with your channel ID

voicemessage = VoiceMessageSender(TOKEN, CHANNEL_ID)
voicemessage.SendVoiceMessage("D:\path\to\your\audio\file.mp3")