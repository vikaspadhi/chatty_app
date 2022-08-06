import json
from account.models import User
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from .models import Thread , Chat

class ChatConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print("WS connected...")
        print("Channel Layer - ",self.channel_layer)
        print("Channel Name - ",self.channel_name)
        self.send({'type':'websocket.accept'})


    def websocket_receive(self,event):
        print("WS received msg....")
        data = json.loads(event["text"])
        if data["number"]:
            me = self.scope['user']
            other_user = User.objects.get(mobile=data["number"])
            self.thread_obj = Thread.objects.get_or_create_personal_thread(me, other_user)
            self.room_name = f'{self.thread_obj.id}'
            async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        
            if data['msg'] != '':
                msg = json.dumps({
                'text': data["msg"],
                'username': self.scope['user'].first_name + self.scope['user'].last_name,
                'room_name': self.room_name,
                })

                self.store_message(data["msg"])

                async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                    {
                        'type': 'websocket.message',
                        'text': msg
                    }
                )


    def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message sent - {event["text"]}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    def store_message(self, text):
        Chat.objects.create(
            thread = self.thread_obj,
            sender = self.scope['user'],
            text = text
        )
    
    def websocket_disconnect(self,event):
        print("WS disconnected...")
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)