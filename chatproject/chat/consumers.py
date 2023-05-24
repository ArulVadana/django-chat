import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name+"group"

        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    


    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json["username"]
    

        await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'username':username,

            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'username':username,
        }))

    async def disconnect(self, close_code):
        # Leave room group
        print("channel layer",self.channel_layer)
        await(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )