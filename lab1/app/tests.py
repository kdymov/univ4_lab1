from django.test import TestCase
from app.models import Brigade, Worker


# Create your tests here.
class BrigadeTestCase(TestCase):
    def setUp(self):
        w1 = Worker.objects.create(name="Mem 1")
        w2 = Worker.objects.create(name="Mem 2")
        w3 = Worker.objects.create(name="Mem 3")
        Brigade.objects.create(member1=w1, member2=w2, member3=w3)

    def test_brigade_contains(self):
        b = Brigade.objects.get(id=1)
        self.assertEqual(b.member1.name, "Mem 1")
        self.assertEqual(b.member2.name, "Mem 2")
        self.assertEqual(b.member3.name, "Mem 3")
