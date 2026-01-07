from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from watchmate import models

# Create your tests here.

class StreamPlatformAPITests(APITestCase):

    def setUp(self):
        # To make the password hashed
        self.user = User.objects.create_user(username='jude', password='password@123')

        self.client.force_authenticate(user=self.user)

        # self.token = Token.objects.create(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + self.token.key)

        # Needed to test list and detail
        self.stream = models.StreamPlatform.objects.create(name="netflix", about="Get all the best movies and series in one place", website="https://netflix.com")


    def test_streamplatform_create(self):
        data = {
            "name": "netflix",
            "about": "Get all the best movies and series in one place",
            "website": "https://netflix.com"
        }

        url = reverse('stream-list')
        response = self.client.post(url, data)

        # We use 403 Forbidden because we cannot make our user an ADMIN for the test
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.StreamPlatform.objects.count(), 1)


    def test_admin_can_create_streamplatform(self):
        self.user.is_staff = True
        self.user.save()

        url = reverse('stream-list')
        response = self.client.post(url, {
            "name": "netflix",
            "about": "Get all the best movies and series in one place",
            "website": "https://netflix.com"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_streamplatform_list(self):
        url = reverse('stream-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]['about'], 'Get all the best movies and series in one place')
        self.assertEqual(models.StreamPlatform.objects.count(), 1)


    def test_streamplatform_create_invalid_data(self):
        self.user.is_staff = True
        self.user.save()

        url = reverse('stream-list')
        response = self.client.post(url, {"name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_streamplatform_individual(self):
        url = reverse('stream-detail', args=(self.stream.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_streamplatform_update(self):
        data = {
            "name": "netflix",
            "about": "Get all the best movies and series in one place!!",
            "website": "https://netflix.com"
        }

        url = reverse('stream-detail', args=(self.stream.id,))

        old_name = self.stream.name

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # To ensure no update took place in the db
        self.stream.refresh_from_db()
        self.assertEqual(self.stream.name, old_name)

    
    def test_streamplatform_del(self):
        url = reverse('stream-detail', args=(self.stream.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class WatchListAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='jude', password='password@123')

        self.client.force_authenticate(user=self.user)

        self.stream = models.StreamPlatform.objects.create(name="netflix", about="Get all the best movies and series in one place", website="https://netflix.com")

        self.watch = models.WatchList.objects.create(title='Aladdin', description='It is about a genie and a boy', platform=self.stream, active=True)

    
    def test_watchlist_create(self):
        data = {
            "title": "Aladdin",
            "description": "It is about a genie and a boy",
            "platform": self.stream.id,
            "active": True
        }

        url = reverse('movie-list')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_create_watchlist(self):
        self.user.is_staff = True
        self.user.save()

        data = {
            "title": "47Ronin",
            "description": "It is about a 47Ronins",
            "active": True,
            "platform": self.stream.id
        }

        url = reverse('movie-list')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_create_invalid_data(self):
        self.user.is_staff = True
        self.user.save()
        
        data = {
            "title": ""
        }

        url = reverse('movie-list')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_watchlist_list(self):
        url= reverse('movie-list')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)


    def test_watchlist_individual(self):
        url = reverse('movie-detail', args=(self.watch.id,))
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['title'], 'Aladdin')

    
    def test_watchlist_update(self):
        data = {
            "title": "Barbie"
        }

        old_title = self.watch.title

        url = reverse('movie-detail', args=(self.watch.id,))
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # To ensure no update took place in the db
        self.watch.refresh_from_db()
        self.assertEqual(self.watch.title, old_title)

    
    def test_watchlist_del(self):
        url = reverse('movie-detail', args=(self.watch.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_delete_watchlist(self):
        self.user.is_staff = True
        self.user.save()

        url = reverse('movie-detail', args=(self.watch.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class ReviewAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='jude', password='password@123')

        self.client.force_authenticate(user=self.user)

        self.stream = models.StreamPlatform.objects.create(name="netflix", about="Get all the best movies and series in one place", website="https://netflix.com")

        self.watch1 = models.WatchList.objects.create(title='Aladdin', description='It is about a genie and a boy', platform=self.stream, active=True)

        self.watch2 = models.WatchList.objects.create(title='Spiderman', description='It is about your friendly neighhbourhood spider', platform=self.stream, active=True)

        self.review = models.Review.objects.create(review_user=self.user, description='I like the movie', rating=4, watchlist=self.watch1)

    
    def test_review_create(self):
        data = {
            "review_user": self.user.id,
            "description": "It was great, for real",
            "rating": 5,
            "watchlist": self.watch2.id
        }

        url = reverse('review-create', args=(self.watch2.id,))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_review_list(self):
        url = reverse('review-list', args=(self.watch1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]['rating'], 4)


    def test_review_individual(self):
        url = reverse('review-detail', args=(self.review.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_review_update(self):
        data = {
            "rating": 5
        }

        url = reverse('review-detail', args=(self.review.id,))
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_review_del(self):
        url = reverse('review-detail', args=(self.review.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_user_review_list(self):
        url = '/api/user/reviews/?username=' + self.user.username

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['rating'], 4)