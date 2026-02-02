from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume
from .utils import extract_skills, calculate_ats_score
import PyPDF2


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception:
        return ""

    return text


# ============================================================
# RESUME UPLOAD + ATS ANALYSIS
# ============================================================
@login_required
def upload_resume(request):
    if request.method == "POST":

        resume_file = request.FILES.get("resume_file")
        job_description = request.POST.get("job_description")

        if not resume_file or not job_description:
            return render(request, "resume_upload.html", {
                "error": "Please upload resume and paste job description."
            })

        # Save resume
        resume_obj = Resume.objects.create(
            user=request.user,
            resume_file=resume_file,
            job_description=job_description
        )

        # Extract resume text
        resume_text = extract_text_from_pdf(resume_obj.resume_file.path)

        # Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(job_description)

        # ATS Score
        ats_score, matched, missing = calculate_ats_score(
            resume_skills, jd_skills
        )

        # Save analysis
        resume_obj.analyzed_text = resume_text
        resume_obj.score = ats_score
        resume_obj.save()

        # ✅ REDIRECT (Option 2)
        return redirect("resume_result", resume_id=resume_obj.id)

    return render(request, "resume_upload.html")


# ============================================================
# RESUME RESULT PAGE
# ============================================================
@login_required
def resume_result(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    # Recalculate skills for display (no DB duplication)
    resume_skills = extract_skills(resume.analyzed_text)
    jd_skills = extract_skills(resume.job_description) if hasattr(resume, "job_description") else []

    ats_score, matched, missing = calculate_ats_score(
        resume_skills, jd_skills
    )

    if ats_score >= 80:
        feedback = "Strong ATS match"
    elif ats_score >= 60:
        feedback = "Good match, improve missing skills"
    else:
        feedback = "Low ATS match for this role"

    return render(request, "resume_result.html", {
        "resume": resume,
        "resume_text": resume.analyzed_text,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched": matched,
        "missing": missing,
        "ats_score": ats_score,
        "feedback": feedback
    })
