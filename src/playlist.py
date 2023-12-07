import os
import isodate
from datetime import datetime, time, timedelta
from googleapiclient.discovery import build


class PlayList:
    """
    класс `PlayList`, который инициализируется _id_ плейлиста и имеет следующие публичные атрибуты:
    - название плейлиста
    - ссылку на плейлист
    """
    # API_KEY переменная окружения содержащий ключ для доступа
    API_KEY: str = os.getenv('YOUT_API_KEY')
    # специальный объект для работы с API YouTube
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.url = "https://www.youtube.com/playlist?list=" + str(playlist_id)
        # список с id video, содержащихся в плейлисте
        self.list_playlist = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # первое видео из списка
        self.video_id = self.list_playlist[0]  # выбираем первый элемент
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id
                                                    ).execute()
        title = video_response['items'][0]['snippet']['title']  # название
        self.title: str = title[0:title.find('.')]  # сокращаем название до первой точки

    @property
    def total_duration(self):
        video_ids = self.list_playlist
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        total_duration = 0
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration.total_seconds()  # общее количество секунд
        return timedelta(seconds=int(total_duration))  # Конвертация секунд в формат часы:минуты:секунды

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        url_video = ''
        max_like_count = 0
        for video_id in self.list_playlist:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_id
                                                        ).execute()
            like_count: int = video_response['items'][0]['statistics']['likeCount']
            if int(like_count) > max_like_count:
                max_like_count = int(like_count)
                url_video = "https://youtu.be/" + str(video_id)
        return url_video
