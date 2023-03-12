from django.test import TestCase
from django.urls import reverse

# Create your tests here.

# Index page.

class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))