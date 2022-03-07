from django.test import TestCase


class DatabaseTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


    def test_this_is_true(self):
        self.assertEqual(1,1)


