from flask import Flask, render_template, request

from services.course_service import (
    load_students,
    get_recommendations
)


app = Flask(__name__)


@app.route("/")
def index():

    students = load_students()

    return render_template(
        "index.html",
        students=students.to_dict("records")
    )


@app.route("/recommend", methods=["POST"])
def recommend():

    student_id = request.form.get("student_id")

    recommendations = get_recommendations(
        student_id,
        top_n=5
    )

    if recommendations is None:
        return "Student not found", 404

    return render_template(
        "recommendations.html",
        recommendations=recommendations
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
