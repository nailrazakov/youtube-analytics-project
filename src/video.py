import os
from googleapiclient.discovery import build


class Video:
    """
    Класс для видео, который инициализируется 'id видео', название видео, ссылка на видео,
    количество просмотров, количество лайков
    """
    # YOUT_API_KEY скопирован из гугла и вставлен в переменные окружения
    API_KEY: str = os.getenv('YOUT_API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id: str):
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_id).execute()
            self.video_id: str = video_id
            self.title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
            self.url = "https://youtu.be/" + str(video_id)
        except IndexError:  # у экземпляра инициализируется только свойство `video_id`, а остальные поля `None`.
            self.video_id: str = video_id
            self.title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None
            self.url = None

    def __str__(self):  # Переопределяем
        return self.title


class PLVideo(Video):
    """Класс для видео, который инициализируется 'id видео' и 'id плейлиста, наследуется из 'Video'"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
