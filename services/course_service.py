import pandas as pd

from recommendation.recommender import recommend_courses
from services.bedrock_service import (
    generate_recommendation_explanation
)


# ============================================================
# FILE PATHS
# ============================================================

COURSE_FILE = "data/courses.csv"
STUDENT_FILE = "data/students.csv"


# ============================================================
# LOAD COURSES
# ============================================================

def load_courses():
    """
    Load course information from courses.csv.
    """
    return pd.read_csv(COURSE_FILE)


# ============================================================
# LOAD STUDENTS
# ============================================================

def load_students():
    """
    Load student information from students.csv.
    """
    return pd.read_csv(STUDENT_FILE)


# ============================================================
# GET STUDENT BY ID
# ============================================================

def get_student_by_id(student_id):
    """
    Find a student by student ID.

    Returns:
        Student record if found.
        None if student does not exist.
    """

    students = load_students()

    student = students[
        students["student_id"].astype(str) == str(student_id)
    ]

    if student.empty:
        return None

    return student.iloc[0]


# ============================================================
# GET RECOMMENDATIONS
# ============================================================

def get_recommendations(student_id, top_n=5):
    """
    Generate course recommendations using
    the Python recommendation algorithm.

    This function does NOT call Amazon Bedrock.
    """

    student = get_student_by_id(student_id)

    if student is None:
        return None

    courses = load_courses()

    recommendations = recommend_courses(
        student,
        courses,
        top_n=top_n
    )

    return recommendations


# ============================================================
# GET RECOMMENDATIONS WITH BEDROCK
# ============================================================

def get_recommendations_with_ai(student_id, top_n=5):
    """
    Generate course recommendations using the
    Python recommendation algorithm and then
    generate an AI explanation using Amazon Bedrock.

    Workflow:

        Student ID
             ↓
        Student Profile
             ↓
        Course Data
             ↓
        Recommendation Algorithm
             ↓
        Top N Courses
             ↓
        Amazon Bedrock
             ↓
        AI Explanation
    """

    # --------------------------------------------------------
    # Step 1: Find student
    # --------------------------------------------------------

    student = get_student_by_id(student_id)

    if student is None:
        return None

    # --------------------------------------------------------
    # Step 2: Load courses
    # --------------------------------------------------------

    courses = load_courses()

    # --------------------------------------------------------
    # Step 3: Generate recommendations
    # --------------------------------------------------------

    recommendations = recommend_courses(
        student,
        courses,
        top_n=top_n
    )

    # --------------------------------------------------------
    # Step 4: Generate AI explanation
    # --------------------------------------------------------

    explanation = generate_recommendation_explanation(
        student,
        recommendations
    )

    # --------------------------------------------------------
    # Step 5: Return all results
    # --------------------------------------------------------

    return {
        "student": student,
        "recommendations": recommendations,
        "explanation": explanation
    }