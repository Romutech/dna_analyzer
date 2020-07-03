from django.test import TestCase
from .models import *

class SequenceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="User Test", password="TESTtest.1234")

        Sequence.objects.create(
            title="Genome test",
            file="agtcggaccagttaccgattcgaatccctggatcagttag",
            file_path="genome_test.fna",
            user_id=user.id
        )

    def setUp(self):
        self.sequence = Sequence.objects.get(id=1)
