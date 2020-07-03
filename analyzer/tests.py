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
        self.assertEqual(self.sequence.nb_bases, None)
        self.assertEqual(self.sequence.nb_a, None)
        self.assertEqual(self.sequence.nb_c, None)
        self.assertEqual(self.sequence.nb_g, None)
        self.assertEqual(self.sequence.nb_t, None)

        self.sequence.number_nucleotides()

        self.assertEqual(self.sequence.nb_bases, 40)
        self.assertEqual(self.sequence.nb_a, 10)
        self.assertEqual(self.sequence.nb_c, 10)
        self.assertEqual(self.sequence.nb_g, 10)
        self.assertEqual(self.sequence.nb_t, 10)


    def test_percentage_nucleotide(self):
        self.sequence.number_nucleotides()

        self.assertEqual(self.sequence.percentage_a, None)
        self.assertEqual(self.sequence.percentage_c, None)
        self.assertEqual(self.sequence.percentage_g, None)
        self.assertEqual(self.sequence.percentage_t, None)

        self.sequence.percentage_nucleotide()

        self.assertEqual(self.sequence.percentage_a, 25.0)
        self.assertEqual(self.sequence.percentage_c, 25.0)
        self.assertEqual(self.sequence.percentage_g, 25.0)
        self.assertEqual(self.sequence.percentage_t, 25.0)


    def test_percentage_GC_AT(self):
        self.sequence.number_nucleotides()
        self.sequence.percentage_nucleotide()

        self.assertEqual(self.sequence.percentage_gc, None)
        self.assertEqual(self.sequence.percentage_at, None)

        self.sequence.percentage_GC_AT()

        self.assertEqual(self.sequence.percentage_gc, self.sequence.percentage_g + self.sequence.percentage_c)
        self.assertEqual(self.sequence.percentage_at, self.sequence.percentage_a + self.sequence.percentage_t)


    def test_analyze(self):
        self.assertEqual(self.sequence.nb_bases, None)
        self.assertEqual(self.sequence.nb_a, None)
        self.assertEqual(self.sequence.nb_c, None)
        self.assertEqual(self.sequence.nb_g, None)
        self.assertEqual(self.sequence.nb_t, None)
        self.assertEqual(self.sequence.percentage_a, None)
        self.assertEqual(self.sequence.percentage_c, None)
        self.assertEqual(self.sequence.percentage_g, None)
        self.assertEqual(self.sequence.percentage_t, None)
        self.assertEqual(self.sequence.percentage_gc, None)
        self.assertEqual(self.sequence.percentage_at, None)
        self.assertTrue(self.sequence.ratio_g_c_graph_data is None)

        self.sequence.analyze()

        self.assertEqual(self.sequence.nb_bases, 40)
        self.assertEqual(self.sequence.nb_a, 10)
        self.assertEqual(self.sequence.nb_c, 10)
        self.assertEqual(self.sequence.nb_g, 10)
        self.assertEqual(self.sequence.nb_t, 10)
        self.assertEqual(self.sequence.percentage_a, 25.0)
        self.assertEqual(self.sequence.percentage_c, 25.0)
        self.assertEqual(self.sequence.percentage_g, 25.0)
        self.assertEqual(self.sequence.percentage_t, 25.0)
        self.assertEqual(self.sequence.percentage_gc, self.sequence.percentage_g + self.sequence.percentage_c)
        self.assertEqual(self.sequence.percentage_at, self.sequence.percentage_a + self.sequence.percentage_t)
        
