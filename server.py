from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["https://fruit-ai-frontend-eight.vercel.app"]}})

app.config["MONGO_URI"] = os.getenv('DATABASE_URL')
mongo = PyMongo(app)

# function to serialize data from MongoDB
def serialize_faq(faq):
    return {
        '_id': str(faq['_id']),
        'question': faq['question'],
        'answer': faq['answer'],
    }

# Root route
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Welcome to the Fruit FAQ API',
    }), 200

# ------------ Get all FAQ -----------------
@app.route('/faqs', methods=['GET'])
def get_all_faqs():
    faqs = mongo.db.faqs.find()
    return jsonify([serialize_faq(faq) for faq in faqs]), 200

# ------------ Get FAQ by Id ----------------
@app.route('/faqs/<id>', methods=['GET'])
def get_faq(id):
    faq = mongo.db.faqs.find_one({'_id': ObjectId(id)})
    if faq:
        return jsonify(serialize_faq(faq)), 200
    else:
        return jsonify({'message': 'FAQ Id not found!'}), 404

# ------------ Post new FAQ ----------------
@app.route('/faqs', methods=['POST'])
def create_faq():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    if not question or not answer:
        return jsonify({'message': "Invalid input. Please provide 'question' and 'answer'."}), 400

    new_faq = {
        'question': question,
        'answer': answer,
    }
    mongo.db.faqs.insert_one(new_faq)
    return jsonify({'message': 'FAQ added Successfully!'}), 201

# -------------- Update FAQ ----------------
@app.route('/faqs/<id>', methods=['PUT'])
def update_faq(id):
    data = request.get_json()
    faq = mongo.db.faqs.find_one({'_id': ObjectId(id)})

    if not faq:
        return jsonify({'message': 'FAQ not found!'}), 404

    updated_faq = {
        'question': data.get('question', faq['question']),
        'answer': data.get('answer', faq['answer']),
    }
    mongo.db.faqs.update_one({'_id': ObjectId(id)}, {'$set': updated_faq})

    # Fetch the updated FAQ and return it
    updated_faq = mongo.db.faqs.find_one({'_id': ObjectId(id)})
    return jsonify(serialize_faq(updated_faq)), 200

# -------------- Delete FAQ ----------------
@app.route('/faqs/<id>', methods=['DELETE'])
def delete_faq(id):
    result = mongo.db.faqs.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'FAQ deleted successfully'}), 200
    else:
        return jsonify({'message': 'FAQ not found'}), 404
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port, debug=True)