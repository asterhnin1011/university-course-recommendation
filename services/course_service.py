import pandas as pd

from recommendation.recommender import recommend_courses


COURSE_FILE = "data/courses.csv"
STUDENT_FILE = "data/students.csv"


def load_courses():
    return pd.read_csv(COURSE_FILE)


def load_students():
    return pd.read_csv(STUDENT_FILE)


def get_student_by_id(student_id):

    students = load_students()

    student = students[
        students["student_id"] == student_id
    ]

    if student.empty:
        return None

    return student.iloc[0]


def get_recommendations(student_id, top_n=5):

    student = get_student_by_id(student_id)

    if student is None:
        return None

    courses = load_courses()

    recommendations = recommend_courses(
        student,
        courses,
        top_n
    )

    return recommendations
