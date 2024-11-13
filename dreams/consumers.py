from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from dreams.models import Dream

class LikeConsumer(WebsocketConsumer):
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'dream_{self.id}'

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

        # Надсилання початкового статусу
        self.send_initial_like_status()

    def send_initial_like_status(self):
        user = self.scope['user']
        dream = get_object_or_404(Dream, id=self.id)
        is_liked = dream.likes.filter(id=user.id).exists() if user.is_authenticated else False

        self.send(text_data=json.dumps({
            'action': 'initial_like_status',
            'is_liked': is_liked,
            'likes_count': dream.likes.count(),
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        user = self.scope['user']
        if isinstance(user, AnonymousUser):
            return

        data = json.loads(text_data)
        action = data.get('action')

        if action == 'like':
            self.handle_like(user)
        elif action == 'unlike':
            self.handle_unlike(user)

        like_count = self.get_like_count()
        async_to_sync(self.channel_layer.group_send)(  # Надсилаємо оновлення на головну сторінку
            'main_page_likes',
            {
                'type': 'send_like_count',
                'dream_id': self.id,
                'action': 'like_update',
                'like_count': like_count,
            }
        )

        print(f'dream_id: {self.id}\n like_count: {like_count}')

    def handle_like(self, user):
        dream = get_object_or_404(Dream, id=self.id)
        dream.likes.add(user)
        self.update_like_count(dream)

    def handle_unlike(self, user):
        dream = get_object_or_404(Dream, id=self.id)
        dream.likes.remove(user)
        self.update_like_count(dream)

    def update_like_count(self, dream):
        likes_count = dream.likes.count()

        # Якщо поточний канал є частиною room_group_name, надсилаємо like_update
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'like_update',
            'action': 'like_update',
            'likes_count': likes_count
        })

    def get_like_count(self):
        dream = get_object_or_404(Dream, id=self.id)
        return dream.likes.count()

    def like_update(self, event):
        self.send(text_data=json.dumps({
            'action': 'like_update',
            'likes_count': event['likes_count']
        }))


class MainPageLikeConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'main_page_likes'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def send_like_count(self, data):
        self.send(text_data=json.dumps(data))
