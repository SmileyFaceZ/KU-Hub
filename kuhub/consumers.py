import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the group when the websocket is connected
        await self.channel_layer.group_add(
            f"post_{self.scope['post_id']}_notifications",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group when the websocket is disconnected
        await self.channel_layer.group_discard(
            f"post_{self.scope['post_id']}_notifications",
            self.channel_name
        )

    async def post_report_notification(self, event):
        # Send notification to websocket
        await self.send(text_data=json.dumps({'message': event['message']}))

    async def comment_notification(self, event):
        # Send notification to websocket
        await self.send(text_data=json.dumps({'message': event['message']}))
