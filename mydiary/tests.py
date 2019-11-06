from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from mydiary.models import Document
from django.urls import reverse
import datetime

class DocumentModelTests(TestCase):
    def test_post_and_get(self):
        Document.objects.create(
            title="hoge",
            content="hogehoge",
            next_action="moge",
            related_hash="Django",
            day='2019-10-10'
        )
        response = self.client.get(reverse('mydiary:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], '日記一覧')
        self.assertContains(response, "hoge")
        self.assertEqual("hogehoge", response.context['data'][0].content)
        self.assertEqual("moge", response.context['data'][0].next_action)
        self.assertEqual("Django", response.context['data'][0].related_hash)
        self.assertEqual(datetime.date(2019, 10, 10), response.context['data'][0].day)