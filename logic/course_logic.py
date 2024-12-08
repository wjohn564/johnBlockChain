from threading import Lock
from mock_data import mock_courses

lock = Lock()


def create_course(course_id, name, seats):
    with lock:
        if course_id in mock_courses:
            return {"status": "Course already exists!"}, 400
        mock_courses[course_id] = {"name": name, "seats": seats, "enrolledCount": 0, "students": []}
        print(f"Created course: {mock_courses[course_id]}")
        return {"status": "Course created successfully!"}, 200


def enroll_in_course(course_id, student_address):
    with lock:
        course = mock_courses.get(course_id)
        if not course:
            return {"status": "Course not found!"}, 404
        max_seats = int(course["seats"] * 1.2)
        if course["enrolledCount"] >= max_seats:
            return {"status": "No seats available!"}, 400
        course["enrolledCount"] += 1
        course["students"].append(student_address)
        return {"status": "Enrolled successfully!"}, 200



def get_course_details(course_id):
    course = mock_courses.get(course_id)
    if not course:
        return {"status": "Course not found!"}, 404
    available_seats = course["seats"] - course["enrolledCount"]
    print(f"Course details for {course_id}: {course}")
    return {"name": course["name"], "availableSeats": available_seats}, 200
