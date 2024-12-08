from flask import Blueprint, request, render_template
from logic.blockchain_utils import (
    create_course_blockchain,
    enroll_in_course_blockchain,
    get_course_details_blockchain,
)
from web3.exceptions import ContractLogicError
from threading import Lock

routes = Blueprint('routes', __name__)

# Define locks to prevent race conditions
create_course_lock = Lock()
enroll_lock = Lock()
course_details_lock = Lock()


@routes.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        course_id = request.form.get('courseId')
        name = request.form.get('name')
        seats = request.form.get('seats')

        if not course_id or not name or not seats:
            return render_template('create_course.html', error="All fields are required.")

        try:
            course_id = int(course_id)
            seats = int(seats)
            if seats <= 0 or course_id <= 0:
                raise ValueError
        except ValueError:
            return render_template('create_course.html', error="Course ID and Seats must be positive integers.")

        with create_course_lock:
            try:
                response = create_course_blockchain(course_id, name, seats)
                return render_template('create_course.html', success="Course created successfully!", response=response)
            except ContractLogicError as e:
                return render_template('create_course.html', error=f"Blockchain logic error: {str(e)}")
            except Exception as e:
                return render_template('create_course.html', error=f"Unexpected error: {str(e)}")

    return render_template('create_course.html')


@routes.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        course_id = request.form.get('courseId')
        student_address = request.form.get('studentAddress')

        if not course_id or not student_address:
            return render_template('enroll.html', error="Both Course ID and Student Address are required.")

        try:
            course_id = int(course_id)
        except ValueError:
            return render_template('enroll.html', error="Course ID must be a positive integer.")

        with enroll_lock:
            try:
                response = enroll_in_course_blockchain(course_id, student_address)
                return render_template('enroll.html', success="Enrollment successful!", response=response)
            except ContractLogicError as e:
                return render_template('enroll.html', error=f"Blockchain logic error: {str(e)}")
            except Exception as e:
                return render_template('enroll.html', error=f"Unexpected error: {str(e)}")

    return render_template('enroll.html')


# Route to get course details
@routes.route('/course_details', methods=['GET'])
def course_details():
    course_id = request.args.get('courseId')
    if course_id:
        try:
            course_id = int(course_id)
        except ValueError:
            return render_template('course_details.html', error="Course ID must be a positive integer.")

        with course_details_lock:
            try:
                response = get_course_details_blockchain(course_id)
                if not response:
                    return render_template('course_details.html', error=f"Course with ID {course_id} not found.")

                return render_template('course_details.html', course=response)
            except ContractLogicError as e:
                return render_template('course_details.html', error=f"Blockchain logic error: {str(e)}")
            except Exception as e:
                return render_template('course_details.html', error=f"Unexpected error: {str(e)}")

    return render_template('course_details.html')
