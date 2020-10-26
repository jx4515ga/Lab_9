from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestHomePage(TestCase):
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response,'travel_wishlist/wishlist.html')
        self.assertContains(response,'You have no places in your wishlist')


class TestWishList(TestCase):
    fixtures = ['test_places']

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo' )
        self.assertContains(response, 'New York' )
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')