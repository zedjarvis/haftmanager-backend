import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from .api.serializers import Notification, NotificationSerializer

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, code=5277):
        await self.close(code=code)
    
    @classmethod
    async def decode_json(cls, text_data):
        if isinstance(text_data, str):
            return text_data 
        return json.loads(text_data)
    
    async def receive_json(self, content, **kwargs):
        content = 'pong' if content == 'ping' else content
        print(self.scope['query_string'])
        await self.send_json(content)