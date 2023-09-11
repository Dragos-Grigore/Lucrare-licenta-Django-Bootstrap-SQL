from django.test import SimpleTestCase
from jobsite.forms import SearchBarForm
from django.test import TestCase,Client
from jobsite.models import User
from django.urls import reverse,resolve
from jobsite.views import say_hello,sign_up,company_profile

class TestForms(SimpleTestCase):

    def test_search(self):
        form= SearchBarForm(data={
            'searchbar':'test',
            'job_location':'Adelaide',
            'department':'Administration',
            'job_type':'Internship',
            'study_level':'Student',
            'career_level':'No experience',
            'industry':'Administration'
        })

        self.assertTrue(form.is_valid())
    
    def test_search_no_data(self):
        form =SearchBarForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),6)

    

class TestModels(TestCase):

    def setUp(self):
        self.user1=User.objects.create(
            email = 'own@gmail.com',
            password = '1234',
            type = 'human',
            full_name = 'Jack Johnson',
            phone_number='0987654321',
            education = 'High School',
            experience='',
            skills='',
            hobbies='',
            foreign_languages='english',
            current_company= '',
            job_title=''
        )

class TestUrls(SimpleTestCase):

    def test_hello_url_is_resolves(self):
        url=reverse('hello')
        self.assertEquals(resolve(url).func, say_hello)

    def test_sign_up_url_is_resolves(self):
        url= reverse('sign_up')
        self.assertEquals(resolve(url).func, sign_up)

    def test_detail_url_is_resolves(self):
        url=reverse('company_profile',args=[2])
        self.assertEquals(resolve(url).func,company_profile)

class TestViews(TestCase):

    def setUp(self):
        self.client=Client()
        self.hello_url=reverse('hello')
        self.sign_up_url=reverse('sign_up')

    def test_project_hello_GET(self) :
        response=self.client.get(self.hello_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'jobsite/hello.html')

    def test_project_sign_up_GET(self) :
        response=self.client.get(self.sign_up_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'jobsite/sign_up.html')