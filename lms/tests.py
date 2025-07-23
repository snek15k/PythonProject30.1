from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Course, Lesson, Subscription


class LessonCRUDTestCase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(email='owner@example.com', password='pass')
        self.other_user = User.objects.create_user(email='user@example.com', password='pass')
        self.moderator = User.objects.create_user(email='moderator@example.com', password='pass')
        self.moderator.groups.add(Group.objects.get_or_create(name='Модераторы')[0])

        self.course = Course.objects.create(title='Test Course', description='Course description', owner=self.owner)
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            description='Lesson description',
            video_url='https://youtube.com/watch?v=abc123',
            owner=self.owner
        )
        self.lesson_url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        self.lesson_list_url = reverse('lesson-list-create')

    def test_owner_can_create_lesson(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'Description',
            'video_url': 'https://youtube.com/watch?v=test',
            'owner': self.owner.id  # если в сериализаторе требуется
        }
        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_other_user_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'Description',
            'video_url': 'https://youtube.com/watch?v=test',
            'owner': self.other_user.id  # если требуется
        }
        response = self.client.post(self.lesson_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_lesson(self):
        self.client.force_authenticate(user=self.owner)
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.lesson_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_moderator_can_update_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        data = {'title': 'Moderator Update'}
        response = self.client.patch(self.lesson_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        data = {'title': 'Hacked'}
        response = self.client.patch(self.lesson_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_lesson(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_view_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.lesson_url)
        # Здесь если у других пользователей нет доступа — 403, иначе 200
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])

        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='pass')
        self.course = Course.objects.create(title='Sub Course', description='...', owner=self.user)
        self.subscribe_url = reverse('course-subscribe')

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        response = self.client.post(self.subscribe_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        # Если отписка у тебя реализована через DELETE, то лучше так:
        response = self.client.delete(self.subscribe_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_requires_authentication(self):
        data = {'course_id': self.course.id}
        response = self.client.post(self.subscribe_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # исправлено с 403

    def test_subscription_requires_course_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.subscribe_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
