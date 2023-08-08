import requests
import json
import os
import base64
import random
import soundfile as sf
import re


class _VoiceMessageUtils:
    @staticmethod
    def GenerateWaveform(length=64):
        characters = " !#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~Çüéâäàå"
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
    
    @staticmethod
    def CleanString(string):
        pattern = r'[^a-zA-Z0-9\s]'
        cleaned_string = re.sub(pattern, '', string)
        return cleaned_string

    @staticmethod
    def EncodeToB64(string):
        encoded_bytes = base64.b64encode(string.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        return encoded_string
    
    @staticmethod
    def GetAudioDuration(filename):
        audio_data, sample_rate = sf.read(filename)
        duration = round(len(audio_data) / sample_rate, 1)
        return duration
    

class VoiceMessageSender:
    def __init__(self, token, channel_id, debug=False):
        self.TOKEN = token
        self.CHANNEL_ID = channel_id
        self.DEBUG = debug

    def SendVoiceMessage(self, file_path):
        print("Processing file:", file_path)
        rep = self.__GetUrl(file_path)
        self.__UploadFile(rep, file_path)
        self.__SendVoiceMessage(rep, file_path)

    def __GetUrl(self, file_path):
        url = f"https://discord.com/api/v9/channels/{self.CHANNEL_ID}/attachments"
        with open(file_path, 'rb') as file:
            file.seek(0, os.SEEK_END)
            payload = json.dumps({
            "files": [
                {
                "filename": os.path.basename(file.name),
                "file_size": file.tell(),
                "id": "261"
                }
            ]
            })
            headers = {
            'accept': '*/*',
            'authorization': self.TOKEN,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36',
            }
            
            
            response = requests.request("POST", url, headers=headers, data=payload)

            response_data = response.json()
            if 'attachments' in response_data:
                attachments = response_data['attachments']
                return attachments
            else:
                raise(f"Attachment URL returned {response_data}")
                
        

    def __UploadFile(self, url, file_path):
        with open(file_path, 'rb') as file:
            url = url[0]['upload_url']

            payload = file.read()
            headers = {
            'authority': 'discord-attachments-uploads-prd.storage.googleapis.com',
            'accept': '*/*',
            'content-type': 'audio/ogg',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36'
            }

            response = requests.request("PUT", url, headers=headers, data=payload)
            
            if self.DEBUG:
                print(json.dumps(response.json(), indent=4))
        

    def __SendVoiceMessage(self, response, file_path, length=None):
        with open(file_path, 'rb') as file:
            
            url = f"https://discord.com/api/v9/channels/{self.CHANNEL_ID}/messages"
        
            duration = _VoiceMessageUtils.GetAudioDuration(file.name) or length
        
            if self.DEBUG:
                print(file.name + " | " + response[0]['upload_filename'])
                print("sending " + file.name + " with duration " + str(_VoiceMessageUtils.GetAudioDuration(file.name)))
                print(response)

            
            file.seek(0, os.SEEK_END)
            payload = json.dumps({
            "content": "",
            "channel_id": self.CHANNEL_ID,
            "type": 0,
            "sticker_ids": [],
            "attachments": [
                {
                "content_type": "audio/ogg",
                "duration_secs": duration,
                "filename": "voice-message.ogg",
                "id": self.CHANNEL_ID,
                "size": 4096,
                "uploaded_filename": response[0]['upload_filename'],
                "waveform": _VoiceMessageUtils.EncodeToB64(_VoiceMessageUtils.GenerateWaveform()),
                "spoiler": False,
                "sensitive": False
                }
            ],
            "flags": 8192,
            })
            headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'authorization': self.TOKEN,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': f'https://discord.com/channels/^@me/{self.CHANNEL_ID}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36',
            'x-discord-locale': 'en-US',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDEzIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDQiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTMgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMiBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMjIuMy4yIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjAzNjcwLCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozMjI2NiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if self.DEBUG:
                print(json.dumps(response.json(), indent=4))
            