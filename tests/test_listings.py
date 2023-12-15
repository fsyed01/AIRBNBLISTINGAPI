# tests/test_listings.py

import unittest
from app import app

class TestListingsEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_listings(self):
        response = self.app.get('/listings')
        self.assertEqual(response.status_code, 200)

    def test_get_listing_by_id(self):
        response = self.app.get('/listings/1')
        self.assertEqual(response.status_code, 200)

    def test_get_filtered_listings(self):
        response = self.app.get('/listings?price_gt=100&neighborhood=Downtown')
        self.assertEqual(response.status_code, 200)

class TestListingsEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # ... (Previous code for GET endpoint tests)

    def test_create_new_listing(self):
        new_listing_data = {
            'name': 'Cozy Apartment',
            'price': 120,
            'neighborhood': 'Suburb',
            'host_id': 3,
            'room_type': 'Entire home/apt'
        }
        response = self.app.post('/listings', json=new_listing_data)
        self.assertEqual(response.status_code, 201)

    def test_update_listing(self):
        updated_listing_data = {
            'name': 'Updated Cozy Apartment',
            'price': 150,
        }
        response = self.app.patch('/listings/1', json=updated_listing_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_listing(self):
        response = self.app.delete('/listings/1')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
