import pandas as pd


def calculate_recommendation_score(student, course):
    score = 0

    # --------------------------------------------------
    # 1. Major Match - 30 points
    # --------------------------------------------------
    if student["major"].lower() == course["major"].lower():
        score += 30

    # --------------------------------------------------
    # 2. Interest Match - 30 points
    # --------------------------------------------------
    student_interests = [
        item.strip().lower()
        for item in str(student["interests"]).split(",")
    ]

    course_interest = course["interest"].strip().lower()

    if course_interest in student_interests:
        score += 30

    # --------------------------------------------------
    # 3. Skill Match - 25 points
    # --------------------------------------------------
    student_skills = {
        item.strip().lower()
        for item in str(student["skills"]).split(",")
    }

    course_skills = {
        item.strip().lower()
        for item in str(course["skills"]).split(",")
    }

    matching_skills = student_skills.intersection(course_skills)

    if course_skills:
        skill_score = (
            len(matching_skills) / len(course_skills)
        ) * 25

        score += skill_score

    # --------------------------------------------------
    # 4. GPA / Difficulty Match - 15 points
    # --------------------------------------------------
    gpa = float(student["gpa"])
    difficulty = course["difficulty"].lower()

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

    return round(score, 2)


def recommend_courses(student, courses, top_n=5):

    recommendations = []

    for _, course in courses.iterrows():

        score = calculate_recommendation_score(
            student,
            course
        )

        recommendations.append({
            "course_id": course["course_id"],
            "course_name": course["course_name"],
            "major": course["major"],
            "interest": course["interest"],
            "skills": course["skills"],
            "difficulty": course["difficulty"],
            "score": score
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:top_n]
