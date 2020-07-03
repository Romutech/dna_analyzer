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

    def test_number_nucleotides(self):
        self.sequence.number_nucleotides()
        self.assertEqual(self.sequence.nb_bases, 40)
        self.assertEqual(self.sequence.nb_a, 10)
        self.assertEqual(self.sequence.nb_c, 10)
        self.assertEqual(self.sequence.nb_g, 10)
        self.assertEqual(self.sequence.nb_t, 10)

    def test_percentage_nucleotide(self):
        self.sequence.number_nucleotides()

        self.sequence.percentage_nucleotide()
        self.assertEqual(self.sequence.percentage_a, 25.0)
        self.assertEqual(self.sequence.percentage_c, 25.0)
        self.assertEqual(self.sequence.percentage_g, 25.0)
        self.assertEqual(self.sequence.percentage_t, 25.0)


