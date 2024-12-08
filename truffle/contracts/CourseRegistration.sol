// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract CourseRegistration {
    struct Course {
        string name;
        uint256 seats;
        uint256 enrolledCount;
        address[] students;
    }

    mapping(uint256 => Course) public courses;

    // Event to track course creation
    event CourseCreated(uint256 courseId, string name, uint256 seats);

    // Event to track student enrollment
    event StudentEnrolled(uint256 courseId, address student);

    /**
     * @dev Create a new course with a unique ID, name, and available seats.
     * @param courseId Unique identifier for the course.
     * @param name Name of the course.
     * @param seats Total number of available seats in the course.
     */
    function createCourse(
        uint256 courseId,
        string memory name,
        uint256 seats
    ) public {
        require(courses[courseId].seats == 0, "Course already exists");
        require(seats > 0, "Number of seats must be greater than 0");

        Course storage newCourse = courses[courseId];
        newCourse.name = name;
        newCourse.seats = seats;
        newCourse.enrolledCount = 0;

        emit CourseCreated(courseId, name, seats);
    }

    /**
     * @dev Enroll a student in a course.
     * @param courseId Unique identifier for the course.
     */
    function enrollInCourse(uint256 courseId) public {
        Course storage course = courses[courseId];

        require(course.seats > 0, "Course not found");
        require(course.enrolledCount < course.seats, "No seats available");

        for (uint256 i = 0; i < course.students.length; i++) {
            require(
                course.students[i] != msg.sender,
                "Student already enrolled"
            );
        }

        course.students.push(msg.sender);
        course.enrolledCount++;

        emit StudentEnrolled(courseId, msg.sender);
    }

    /**
     * @dev Get details of a course by its ID.
     * @param courseId Unique identifier for the course.
     * @return name Name of the course.
     * @return availableSeats Number of remaining seats.
     */
    function getCourseDetails(
        uint256 courseId
    ) public view returns (string memory name, uint256 availableSeats) {
        Course storage course = courses[courseId];

        require(course.seats > 0, "Course not found");

        name = course.name;
        availableSeats = course.seats - course.enrolledCount;
    }
}
