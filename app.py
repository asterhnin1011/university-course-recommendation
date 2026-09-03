from flask import Flask, render_template, request

from services.course_service import (
    load_students,
    get_recommendations_with_ai
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():

    students = load_students()

    return render_template(
        "index.html",
        students=students.to_dict("records")
    )


# ============================================================
# COURSE RECOMMENDATION
# ============================================================

@app.route("/recommend", methods=["POST"])
def recommend():

    # --------------------------------------------------------
    # Get student ID from the form
    # --------------------------------------------------------

    student_id = request.form.get("student_id")

    # --------------------------------------------------------
    # Generate recommendations + Bedrock explanation
    # --------------------------------------------------------

    result = get_recommendations_with_ai(
        student_id,
        top_n=5
    )

    # --------------------------------------------------------
    # Student not found
    # --------------------------------------------------------

    if result is None:
        return "Student not found", 404

    # --------------------------------------------------------
    # Extract results
    # --------------------------------------------------------

    recommendations = result["recommendations"]
    explanation = result["explanation"]
    student = result["student"]

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    return render_template(
        "recommendations.html",
        recommendations=recommendations,
        explanation=explanation,
        student=student
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )