import pandas as pd


# ============================================================
# CALCULATE RECOMMENDATION SCORE
# ============================================================

def calculate_recommendation_score(student, course):
    """
    Calculate the recommendation score for one student
    and one course.

    Maximum score = 100 points

    Major Match       = 30 points
    Interest Match    = 30 points
    Skill Match       = 25 points
    GPA/Difficulty    = 15 points
    """

    score = 0

    # --------------------------------------------------------
    # 1. Major Match - 30 points
    # --------------------------------------------------------

    student_major = str(student["major"]).strip().lower()
    course_major = str(course["major"]).strip().lower()

    if student_major == course_major:
        score += 30

    # --------------------------------------------------------
    # 2. Interest Match - 30 points
    # --------------------------------------------------------

    student_interests = {
        item.strip().lower()
        for item in str(student["interests"]).split(",")
        if item.strip()
    }

    course_interest = (
        str(course["interest"])
        .strip()
        .lower()
    )

    if course_interest in student_interests:
        score += 30

    # --------------------------------------------------------
    # 3. Skill Match - 25 points
    # --------------------------------------------------------

    student_skills = {
        item.strip().lower()
        for item in str(student["skills"]).split(",")
        if item.strip()
    }

    course_skills = {
        item.strip().lower()
        for item in str(course["skills"]).split(",")
        if item.strip()
    }

    matching_skills = (
        student_skills.intersection(course_skills)
    )

    if course_skills:

        skill_score = (
            len(matching_skills)
            / len(course_skills)
        ) * 25

        score += skill_score

    # --------------------------------------------------------
    # 4. GPA / Difficulty Match - 15 points
    # --------------------------------------------------------

    try:
        gpa = float(student["gpa"])
    except (ValueError, TypeError):
        gpa = 0.0

    difficulty = (
        str(course["difficulty"])
        .strip()
        .lower()
    )

    if difficulty == "beginner":

        if gpa >= 2.0:
            score += 15

    elif difficulty == "intermediate":

        if gpa >= 2.8:
            score += 15

    elif difficulty == "advanced":

        if gpa >= 3.5:
            score += 15

        elif gpa >= 3.0:
            score += 8

    # --------------------------------------------------------
    # Return final score
    # --------------------------------------------------------

    return round(score, 2)


# ============================================================
# RECOMMEND COURSES
# ============================================================

def recommend_courses(student, courses, top_n=5):
    """
    Generate ranked course recommendations.

    The recommendation process:

        Student Profile
              ↓
        Compare with Courses
              ↓
        Calculate Score
              ↓
        Sort by Score
              ↓
        Return Top N Courses
    """

    recommendations = []

    # --------------------------------------------------------
    # Calculate score for every course
    # --------------------------------------------------------

    for _, course in courses.iterrows():

        score = calculate_recommendation_score(
            student,
            course
        )

        # ----------------------------------------------------
        # Store recommendation information
        # ----------------------------------------------------

        recommendations.append({

            "course_id": course["course_id"],

            "course_name": course["course_name"],

            "major": course["major"],

            "interest": course["interest"],

            "skills": course["skills"],

            "difficulty": course["difficulty"],

            "score": score

        })

    # --------------------------------------------------------
    # Sort courses from highest score to lowest score
    # --------------------------------------------------------

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # --------------------------------------------------------
    # Return Top N courses
    # --------------------------------------------------------

    return recommendations[:top_n]