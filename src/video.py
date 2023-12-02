from src.channel import Channel


class Video(Channel):
    """
    Класс для видео, который инициализируется 'id видео', название видео, ссылка на видео,
    количество просмотров, количество лайков
    """
    def __init__(self, video_id: str):
        youtube_object = super().youtube
        video_response = youtube_object.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=video_id).execute()
        self.video_id: str = video_id
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
        self.url = "https://youtu.be/" + str(video_id)

    def __str__(self): # Переопределяем
        return self.video_title


class PLVideo(Video):
    """Класс для видео, который инициализируется 'id видео' и 'id плейлиста, наследуется из 'Video'"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
