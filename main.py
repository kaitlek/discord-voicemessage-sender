from voicemessages import VoiceMessageSender

TOKEN = "token"
CHANNEL_ID = 123

voicemessage = VoiceMessageSender(TOKEN, CHANNEL_ID)
voicemessage.SendVoiceMessage("D:\...")