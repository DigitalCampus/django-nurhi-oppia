# CourseResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.tests.utils import getApiKey


class CourseResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['user.json', 'oppia.json']

    def setUp(self):
        super(CourseResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        api_key = getApiKey(user=user)
        self.auth_data = {
            'username': 'demo',
            'api_key': api_key.key,
        }
        self.url = '/api/v1/course/'

    # Post invalid
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))

    # test unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'demo',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))

    # test authorized
    def test_authorized(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)

    # test contains courses (and right no of courses)
    def test_has_courses(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        # should have 2 courses with the test data set
        self.assertEquals(len(response_data['courses']),2)
        # check each course had a download url
        for course in response_data['courses']:
            self.assertTrue('url' in course)
            self.assertTrue('shortname' in course)
            self.assertTrue('title' in course)
            self.assertTrue('version' in course)

    # TODO test course file found
    def test_course_download_file_found(self):
        #resp = self.api_client.get(self.url+"20/download/", format='json', data=self.auth_data)
        #self.assertHttpOK(resp)
        pass

    # TODO course file not found
    def test_course_download_file_not_found(self):
        #resp = self.api_client.get(self.url+"9999/download/", data=self.auth_data)
        #self.assertHttpNotFound(resp)
        pass