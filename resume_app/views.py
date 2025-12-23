from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resume
from job_app.models import Job
from careerboost.utils.ai import ai_score_resume
import PyPDF2

@login_required
def resume_result(request, resume_id):
    resume = Resume.objects.get(id=resume_id)
    
    return render(request, "resume_result.html", {
        "resume": resume,
        "resume_text": resume.analyzed_text,
        "match_percent": resume.score
    })


# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except:
        return "Error reading PDF file."
    return text


@login_required
def upload_resume(request):
    if request.method == "POST":

        if "resume_file" not in request.FILES:
            return render(request, "resume_upload.html", {"error": "Please upload a PDF file."})

        uploaded_file = request.FILES["resume_file"]

        # Save file to DB
        resume_obj = Resume.objects.create(
            user=request.user,
            resume_file=uploaded_file
        )

        # Extract resume text
        resume_text = extract_text_from_pdf(resume_obj.resume_file.path)

        # Combine all job descriptions
        all_job_descriptions = " ".join(Job.objects.values_list("description", flat=True))

        # AI scoring
        ai_result = ai_score_resume(resume_text, all_job_descriptions)

        match_percent = ai_result["match_percent"]
        resume_skills = ai_result["resume_skills"]
        job_keywords = ai_result["job_keywords"]
        matched = ai_result["matched"]
        missing = ai_result["missing"]
        
        
        # Save analysis
        resume_obj.analyzed_text = resume_text
        resume_obj.score = match_percent
        resume_obj.save()

        return render(request, "resume_result.html", {
            "resume": resume_obj,
            "resume_text": resume_text,
            "resume_skills": resume_skills,
            "job_keywords": job_keywords,
            "matched": matched,
            "missing": missing,
            "match_percent": match_percent
        })

    return render(request, "resume_upload.html")
