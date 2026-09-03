import boto3
from botocore.exceptions import ClientError


REGION = "us-east-1"

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


bedrock = boto3.client(
    "bedrock-runtime",
    region_name=REGION
)


def generate_recommendation_explanation(
    student,
    recommendations
):

    recommendation_text = "\n".join(
        [
            f"- {course['course_name']}: "
            f"{course['score']}%"
            for course in recommendations
        ]
    )

    prompt = f"""
You are a university academic course advisor.

Analyze the student's profile and the recommended
courses below.

Student:
Major: {student['major']}
GPA: {student['gpa']}
Interests: {student['interests']}
Skills: {student['skills']}

Recommended courses:
{recommendation_text}

Explain why the top courses are suitable for this student.

Give a short, clear explanation for each recommended course.
Do not invent course prerequisites or student information.
"""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                }
            ]
        }
    ]

    try:

        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=messages,
            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.3
            }
        )

        return response[
            "output"
        ][
            "message"
        ][
            "content"
        ][0]["text"]

    except ClientError as e:

        return (
            "Unable to generate AI explanation: "
            + str(e)
        )

