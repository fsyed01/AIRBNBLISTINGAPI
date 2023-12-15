# app.py

from flask import Flask, jsonify, request
from utils.data_handler import read_data, write_data

application = Flask(__name__)

# Set the path to the Airbnb data file
DATA_FILE = 'data/airbnb.json'

# Define the data variable
listings_data = read_data(DATA_FILE)

# Define GET Endpoints
@application.route('/listings', methods=['GET'])
def get_all_listings():
    return jsonify(listings_data), 200

@application.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing_by_id(listing_id):
    listing = next((listing for listing in listings_data if listing['id'] == listing_id), None)
    if listing:
        return jsonify(listing), 200
    else:
        return jsonify({'error': 'Listing not found'}), 404

@application.route('/listings', methods=['GET'])
def get_filtered_listings():
    filters = request.args
    filtered_listings = [listing for listing in listings_data if all(listing[key] == value for key, value in filters.items())]
    return jsonify(filtered_listings), 200

# Define POST Endpoint
@application.route('/listings', methods=['POST'])
def create_listing():
    new_listing = request.json
    new_listing['id'] = max(listing['id'] for listing in listings_data) + 1
    listings_data.append(new_listing)
    write_data(DATA_FILE, listings_data)
    return jsonify(new_listing), 201

# Define PATCH Endpoint
@application.route('/listings/<int:listing_id>', methods=['PATCH'])
def update_listing(listing_id):
    updated_listing = request.json
    existing_listing = next((listing for listing in listings_data if listing['id'] == listing_id), None)
    if existing_listing:
        existing_listing.update(updated_listing)
        write_data(DATA_FILE, listings_data)
        return jsonify(existing_listing), 200
    else:
        return jsonify({'error': 'Listing not found'}), 404

# Define DELETE Endpoint
@application.route('/listings/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    global listings_data
    listings_data = [listing for listing in listings_data if listing['id'] != listing_id]
    write_data(DATA_FILE, listings_data)
    return jsonify({'message': 'Listing deleted successfully'}), 200

# Define GET Endpoint for search
@application.route('/listing/search', methods=['POST'])
def search_listings():
    search_terms = request.json
    search_results = [listing for listing in listings_data if all(term.lower() in listing['name'].lower() for term in search_terms)]
    return jsonify(search_results), 200

# Add error handling
@application.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad Request'}), 400

@application.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    application.run(debug=True)
