from flask import Blueprint, request, jsonify
from logic.blockchain_utils import create_course_blockchain, enroll_in_course_blockchain, get_course_details_blockchain, \
    web3

routes = Blueprint('routes', __name__)


@routes.route('/createCourse', methods=['POST'])
def create_course_route():
    data = request.json
    course_id = data['courseId']
    name = data['name']
    seats = data['seats']
    return jsonify(create_course_blockchain(course_id, name, seats))


@routes.route('/enrollInCourse', methods=['POST'])
def enroll_in_course_route():
    data = request.json
    course_id = data['courseId']
    student_address = data.get('studentAddress', web3.eth.accounts[1])  # Use a test account
    return jsonify(enroll_in_course_blockchain(course_id, student_address))


@routes.route('/getCourseDetails/<int:course_id>', methods=['GET'])
def get_course_details_route(course_id):
    return jsonify(get_course_details_blockchain(course_id))
