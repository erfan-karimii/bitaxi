from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from model_bakery import baker

from account.models import User, CustomerProfile, DriverProfile
from trips.models import Comment, Trips


class TestCustomerCommentView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse("trips:customer_comment")

        cls.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        cls.customer_profile = CustomerProfile.objects.get(user=cls.customer)
        cls.customer_token = Token.objects.create(user=cls.customer)

        cls.customer2 = User.objects.create_user(
            email="test1@test.com", password="1", is_customer=True,is_verified=True
        )
        customer_profile2 = CustomerProfile.objects.get(user=cls.customer2)

        cls.not_customer = User.objects.create_user(
            email="test2@test.com", password="1", is_customer=False
        )
        cls.not_customer_token = Token.objects.create(user=cls.not_customer)

        cls.driver = User.objects.create_user(
            email="test3@test.com", password="1", is_driver=True
        )
        cls.driver_profile = DriverProfile.objects.get(user=cls.driver)

        cls.trip = baker.make(
            Trips, customer=cls.customer_profile, driver=cls.driver_profile
        )

        cls.comment = baker.make(Comment, customer=cls.customer_profile, is_show=True)
        cls.comment2 = baker.make(Comment, customer=customer_profile2, is_show=True)

    def test_get_customer_comments(self):
        response = self.client.get(
            self.url, headers={"Authorization": f"Token {self.customer_token.key}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_notcustomer_comment(self):
        response = self.client.get(
            self.url, headers={"Authorization": f"Token {self.not_customer_token.key}"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_customer_comment(self):
        data = {
            "customer": self.customer_profile.id,
            "driver": self.driver_profile.id,
            "trip": self.trip.id,
            "text": "test",
            "score ": 5,
        }
        response = self.client.post(
            self.url,
            data,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 3)

    def test_create_with_unvalid_data(self):
        data = {
            "customer": 1000,
            "driver": 1000,
            "trip": 1000,
            "text": "test" * 1000,
        }
        response = self.client.post(
            self.url,
            data,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(len(response.data.keys()), 4)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Comment.objects.count(), 2)

 
class TestCustomerCommentDetailView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        customer_profile = CustomerProfile.objects.get(user=cls.customer)
        cls.customer_token = Token.objects.create(user=cls.customer)

        cls.not_customer = User.objects.create_user(
            email="test2@test.com", password="1", is_customer=False
        )
        cls.not_customer_token = Token.objects.create(user=cls.not_customer)

        cls.driver = User.objects.create_user(
            email="test3@test.com", password="1", is_driver=True
        )
        cls.driver_profile = DriverProfile.objects.get(user=cls.driver)

        cls.trip = baker.make(
            Trips, customer=customer_profile, driver=cls.driver_profile
        )

        cls.comment = baker.make(Comment, customer=customer_profile, is_show=True)

    def test_get_detail_comment(self):
        url = reverse("trips:customer_comment_detail", kwargs={"id": self.comment.id})
        response = self.client.get(
            url,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(response.status_code, 200)
    
    def test_get_wrong_id(self):
        url = reverse("trips:customer_comment_detail", kwargs={"id": 1000})
        response = self.client.get(
            url,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get('detail'),"Not found.")

    def test_get_invalid_user(self):
        url = reverse("trips:customer_comment_detail", kwargs={"id": self.comment.id})
        response = self.client.get(
            url,
            headers={"Authorization": f"Token {self.not_customer_token.key}"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get('detail'), 'You are not a valid customer!')
    
    def test_delete_comemnt_detail(self):
        url = reverse("trips:customer_comment_detail", kwargs={"id": self.comment.id})
        response = self.client.delete(
            url,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("msg"), "comment delete successfully")
        self.assertEqual(Comment.objects.count(), 1)
        self.assertFalse(Comment.objects.first().is_show)

    
class TestSuperuserCommentView(APITestCase):    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse("trips:superuser_comment") 

        cls.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        customer_profile = CustomerProfile.objects.get(user=cls.customer)

        cls.superuser = User.objects.create_superuser(
            email="test2@test.com", password="1"
        )
        cls.superuser_token = Token.objects.create(user=cls.superuser)


        cls.comment = baker.make(Comment, customer=customer_profile, is_show=False)
        cls.comment = baker.make(Comment, customer=customer_profile, is_show=True)

    

    def test_get_superuser_all_comment(self):
        response = self.client.get(
            self.url,
            headers={"Authorization": f"Token {self.superuser_token.key}"},
        )

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),2)


class TestSuperuserCommentDetailView(APITestCase):    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        customer_profile = CustomerProfile.objects.get(user=cls.customer)

        cls.superuser = User.objects.create_superuser(
            email="test2@test.com", password="1"
        )
        cls.superuser_token = Token.objects.create(user=cls.superuser)


        cls.comment_1 = baker.make(Comment, customer=customer_profile,score=2 ,is_show=False)
        cls.comment_2 = baker.make(Comment, customer=customer_profile, is_show=True)


    def test_superuser_delete_comment(self):
        comment = baker.make(Comment)
        url = reverse("trips:superuser_comment_detail",kwargs={'id':comment.id}) 

        response = self.client.delete(
            url,
            headers={"Authorization": f"Token {self.superuser_token.key}"},
        )

        self.assertEqual(response.status_code,204)
        self.assertEqual(Comment.objects.count(),2)
    

    def test_superuser_patch_comment(self):
        url = reverse("trips:superuser_comment_detail",kwargs={'id':self.comment_1.id}) 
        data = {
            'show':True,
            'score':3
        }
        response = self.client.patch(
            url,
            data=data,
            headers={"Authorization": f"Token {self.superuser_token.key}"},
        )

        self.comment_1.refresh_from_db()
        
        self.assertEqual(response.status_code,202)
        self.assertDictEqual(response.data,{"msg": "comment change successfully"})
        self.assertTrue(self.comment_1.is_show)
        self.assertNotEqual(self.comment_1.score,data.get("score"))


class TestDriverCommentView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse("trips:driver_comment")

        cls.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        customer_profile = CustomerProfile.objects.get(user=cls.customer)

        cls.driver = User.objects.create_user(
            email="test1@test.com", password="1", is_driver=True
        )
        driver_profile = DriverProfile.objects.get(user=cls.driver)
        cls.driver_token = Token.objects.create(user=cls.driver)

        cls.comment_1 = baker.make(Comment,text='test1', customer=customer_profile,driver=driver_profile,is_show=False)
        cls.comment_2 = baker.make(Comment,text='test2', customer=customer_profile,driver=driver_profile,is_show=True)
    

    def test_driver_get_comments(self):
        response = self.client.get(
            self.url,
            headers={"Authorization": f"Token {self.driver_token.key}"},
        )

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0].get('text'),'test2')
    

class TestDriverCommentDetailView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        customer_profile = CustomerProfile.objects.get(user=cls.customer)

        cls.driver = User.objects.create_user(
            email="test1@test.com", password="1", is_driver=True
        )
        driver_profile = DriverProfile.objects.get(user=cls.driver)
        cls.driver_token = Token.objects.create(user=cls.driver)

        cls.comment_1 = baker.make(Comment,text='test1', customer=customer_profile,driver=driver_profile,is_show=False)
        cls.comment_2 = baker.make(Comment,text='test2', customer=customer_profile,driver=driver_profile,is_show=True)

    def test_driver_report_comment(self):
        url = reverse("trips:driver_comment_detail",kwargs={'id':self.comment_2.id})
        data = {
            'msg':'bad comment'
        }

        response = self.client.post(
            url,
            data,
            headers={"Authorization": f"Token {self.driver_token.key}"},
        )
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.data,{'msg':'feed back received.'})


class TestCancelTripView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.customer = User.objects.create_user(
            email="test@test.com", password="1", is_customer=True,is_verified=True
        )
        cls.customer_profile = CustomerProfile.objects.get(user=cls.customer)
        cls.customer_token = Token.objects.create(user=cls.customer)

        cls.customer2 = User.objects.create_user(
            email="test2@test.com", password="1", is_customer=True,is_verified=True
        )
        cls.customer_profile2 = CustomerProfile.objects.get(user=cls.customer2)
        cls.customer2_token = Token.objects.create(user=cls.customer2)


        cls.driver = User.objects.create_user(
            email="test1@test.com", password="1", is_driver=True
        )
        cls.driver_profile = DriverProfile.objects.filter(user=cls.driver)
        
        cls.driver_profile.update(status = 'traveling')
        cls.driver_profile = cls.driver_profile[0]
        cls.trip = baker.make(Trips,customer=cls.customer_profile,driver=cls.driver_profile,cost=100)
        cls.trip2 = baker.make(Trips,customer=cls.customer_profile2,driver=cls.driver_profile,cost=100,is_cancel=True)
        cls.trip3 = baker.make(Trips,customer=cls.customer_profile2,driver=cls.driver_profile,cost=100,is_end=True)

        


    def test_cancel_trip(self):
        url = reverse("trips:cancel_trip",kwargs={"id":self.trip.id})

        response = self.client.post(
            url,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.driver_profile.refresh_from_db()
        self.trip.refresh_from_db()
        self.customer_profile.refresh_from_db()

        self.assertEqual(response.status_code,200)
        self.assertEqual(self.driver_profile.status ,"No-travel")
        self.assertTrue(self.trip.is_cancel)
        self.assertEqual(self.customer_profile.cash_bank,50)
    
    def test_wrong_trip_id(self):
        url = reverse("trips:cancel_trip",kwargs={"id":self.trip2.id})

        response = self.client.post(
            url,
            headers={"Authorization": f"Token {self.customer_token.key}"},
        )

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.data,{'msg':'not valid trip requested.'})
    
    def test_cancel_ended_trip(self):
        url = reverse("trips:cancel_trip",kwargs={"id":self.trip2.id})

        response = self.client.post(
            url,
            headers={"Authorization": f"Token {self.customer2_token.key}"},
        )

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.data,{'msg':'not valid trip requested.'})
    
    def test_cencel_cenceled_trip(self):
        url = reverse("trips:cancel_trip",kwargs={"id":self.trip3.id})

        response = self.client.post(
            url,
            headers={"Authorization": f"Token {self.customer2_token.key}"},
        )

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.data,{'msg':'not valid trip requested.'})
            

