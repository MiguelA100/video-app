import self
from django.test import TestCase
from django.urls import reverse
from .models import Video
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestHomePageMessage(TestCase):
    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Exercise Videos')

class TestAddVideos(TestCase):
    def test_add_video(self):
        valid_video = {
            'name': 'Messi',
            'url': 'https://www.youtube.com/watch?v=V1SJGmgX67A',
            'notes': 'The best of Messi'

    }

        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)

        self.assertTemplateUsed('video_collections/video_list.html')

        self.assertContains(response, 'Messi')
        self.assertContains(response, 'The best of Messi')
        self.assertContains(response, 'https://www.youtube.com/watch?v=V1SJGmgX67A')

        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()

        self.assertEqual('Messi', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=V1SJGmgX67A', video.url)
        self.assertEqual('The best of Messi', video.notes)
        self.assertEqual('V1SJGmgX67A', video.video_id)

    def test_add_video_invalid_url_not_added(self):
        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?abc=123',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
            'https://minneapolis.edu'
            'https://minneapolis.edu?v=123456'
        ]

        for invalid_video_url in invalid_video_urls:
            new_video = {
                'name': 'example',
                'url': invalid_video_url,
                'notes': 'example notes'

            }

            url = reverse('add_video')
            response = self.client.post(url, new_video)

            self.assertTemplateUsed('video_collection/add.html')

            messages = response.context['messages']
            message_text = [ message.message for message in messages ]
            self.assertIn('Invalid Youtube URL', messages)
            self.assertIn('Please check the data entered.', message_text)

            video_count = Video.objects.count()
            self.assertEqual(0, video_count)

class TestVideoList(TestCase):

    def test_all_videos_displayed_in_correct_order(self):

        v1 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')

        expected_video_order = [ v3, v2, v4, v1]

        url = reverse('video_list')
        response = self.client.get(url)

        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_video_order)

    def test_no_video_message(self):
        url = reverse('video_list')
        response = self.client.get(url)
        self.assertContains(response, "No videos")
        self.assertEqual(0,len(response.context['videos']))

    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '1 video')
        self.assertNotContains(response, '1 videos')

    def test_video_number_message_two_video(self):
            v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
            v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')
            url = reverse('video_list')
            response = self.client.get(url)

            self.assertContains(response, '2 videos')
            


class TestVideoSearch(TestCase):
    pass

class TestVideoModel(TestCase):

    def test_invalid_url_raises_validation_error(self):
        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch/somethingelse',
            'https://www.youtube.com/watch?abc=123',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
            '12334455',
            'https://minneapolis.edu'
            'https://minneapolis.edu?v=123456'
        ]

        for invalid_video_url in invalid_video_urls:
            with self.assertRaises(ValidationError):

                Video.objects.create(name='example', url=invalid_video_url, notes='example note')

            self.assertEqual(0, Video.objects.count())

    def test_duplicate_video_raises_integrity_error(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')

# Create your tests here.
