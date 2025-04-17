from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Resume
from .utils import extract_and_summarize_resume

@api_view(['POST'])
def upload_resume(request):
    # Get data from request
    name = request.data.get('name')
    current_designation = request.data.get('current_designation')
    experiences = request.data.get('experiences')
    skills = request.data.get('skills')
    file = request.FILES.get('file')

    # Validate input
    if not all([name, current_designation, experiences, skills, file]):
        return Response({"error": "All fields (name, current_designation, experiences, skills, file) are required"}, status=400)

    # Create and save resume object first to get a file path
    resume = Resume.objects.create(
        name=name,
        current_designation=current_designation,
        experiences=int(experiences),
        skills=skills,
        file=file
    )

    # Extract text and generate summary using the saved file path
    summary = extract_and_summarize_resume(resume.file.path) if resume.file else "No summary generated"

    # Update the resume object with the summary
    resume.summary = summary
    resume.save()

    # Prepare response
    response = {
        "id": resume.id,
        "name": resume.name,
        "current_designation": resume.current_designation,
        "experiences": resume.experiences,
        "skills": resume.skills,
        "summary": resume.summary,
        "created_at": resume.created_at.isoformat()
    }

    return Response(response, status=201)