import json
import urllib.request
import urllib.error
import getpass

BASE_URL = "http://127.0.0.1:8000"

# 50 realistic test jobs
jobs = [
    ("Python Backend Developer", "TechNova Solutions", "Bangalore, India",
     ["Python", "FastAPI", "PostgreSQL", "REST API", "Git"], 1, 3),

    ("Frontend React Developer", "WebCraft Technologies", "Hyderabad, India",
     ["React", "JavaScript", "HTML", "CSS", "Git"], 1, 3),

    ("Full Stack Developer", "CodeSphere Labs", "Pune, India",
     ["Python", "React", "FastAPI", "PostgreSQL", "REST API"], 2, 5),

    ("Data Analyst", "DataBridge Analytics", "Mumbai, India",
     ["Python", "SQL", "Excel", "Power BI", "Pandas"], 1, 3),

    ("Machine Learning Engineer", "AI Dynamics", "Bangalore, India",
     ["Python", "Machine Learning", "TensorFlow", "PyTorch", "SQL"], 2, 5),

    ("DevOps Engineer", "CloudWorks", "Delhi, India",
     ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"], 2, 5),

    ("Cloud Engineer", "SkyNet Systems", "Hyderabad, India",
     ["AWS", "Azure", "Docker", "Linux", "Terraform"], 2, 5),

    ("Java Backend Developer", "EnterpriseSoft", "Bangalore, India",
     ["Java", "Spring Boot", "PostgreSQL", "REST API", "Git"], 2, 5),

    ("Node.js Developer", "NextGen Software", "Chennai, India",
     ["Node.js", "Express", "JavaScript", "MongoDB", "REST API"], 1, 4),

    ("Data Scientist", "InsightAI", "Bangalore, India",
     ["Python", "Machine Learning", "Pandas", "NumPy", "SQL"], 2, 5),

    ("Python Developer", "SoftMatrix", "Noida, India",
     ["Python", "Django", "REST API", "PostgreSQL", "Git"], 1, 4),

    ("React Developer", "PixelForge", "Pune, India",
     ["React", "JavaScript", "TypeScript", "HTML", "CSS"], 1, 3),

    ("AI Engineer", "NeuralWorks", "Bangalore, India",
     ["Python", "AI", "Machine Learning", "LLM", "PyTorch"], 2, 5),

    ("Software Engineer", "InnovateTech", "Gurgaon, India",
     ["Python", "Java", "SQL", "Git", "REST API"], 1, 4),

    ("Backend Engineer", "AppCore Technologies", "Mumbai, India",
     ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"], 2, 5),

    ("Frontend Engineer", "UI Labs", "Remote, India",
     ["React", "TypeScript", "JavaScript", "CSS", "Git"], 1, 4),

    ("Junior Python Developer", "StartUpHub", "Remote, India",
     ["Python", "SQL", "Git", "REST API"], 0, 2),

    ("Junior Data Analyst", "MarketInsights", "Delhi, India",
     ["SQL", "Excel", "Python", "Power BI"], 0, 2),

    ("Junior Web Developer", "DigitalWorks", "Jaipur, India",
     ["HTML", "CSS", "JavaScript", "React"], 0, 2),

    ("Software Developer", "CodeFactory", "Bangalore, India",
     ["Python", "JavaScript", "SQL", "Git"], 1, 3),

    ("Machine Learning Engineer", "VisionAI", "Hyderabad, India",
     ["Python", "PyTorch", "Machine Learning", "Computer Vision"], 2, 5),

    ("NLP Engineer", "LanguageAI", "Bangalore, India",
     ["Python", "NLP", "Transformers", "PyTorch", "LLM"], 2, 5),

    ("AI/ML Developer", "FutureMind AI", "Pune, India",
     ["Python", "Machine Learning", "TensorFlow", "Scikit-learn"], 1, 4),

    ("Data Engineer", "DataStream", "Bangalore, India",
     ["Python", "SQL", "ETL", "Spark", "AWS"], 2, 5),

    ("Database Developer", "DBTech", "Chennai, India",
     ["PostgreSQL", "SQL", "Python", "Database Design"], 1, 4),

    ("SQL Developer", "Enterprise Data", "Noida, India",
     ["SQL", "PostgreSQL", "Database", "Python"], 1, 3),

    ("AWS Cloud Engineer", "CloudFirst", "Bangalore, India",
     ["AWS", "Docker", "Terraform", "Linux", "CI/CD"], 2, 5),

    ("Azure Cloud Engineer", "Microsoft Solutions Partner", "Hyderabad, India",
     ["Azure", "Docker", "Kubernetes", "Terraform"], 2, 5),

    ("DevOps Developer", "DeployFast", "Pune, India",
     ["Docker", "Jenkins", "GitHub Actions", "Linux", "AWS"], 1, 4),

    ("Site Reliability Engineer", "Reliable Systems", "Bangalore, India",
     ["Linux", "Kubernetes", "AWS", "Docker", "Monitoring"], 2, 5),

    ("QA Automation Engineer", "QualityFirst", "Chennai, India",
     ["Python", "Selenium", "Pytest", "API Testing", "Git"], 1, 4),

    ("Software QA Engineer", "TestLabs", "Bangalore, India",
     ["Testing", "Selenium", "Python", "SQL", "API Testing"], 1, 3),

    ("Cybersecurity Analyst", "SecureNet", "Gurgaon, India",
     ["Cybersecurity", "Linux", "Networking", "SIEM", "Python"], 1, 4),

    ("Security Engineer", "CyberShield", "Bangalore, India",
     ["Cybersecurity", "AWS", "Linux", "Networking", "Python"], 2, 5),

    ("Mobile App Developer", "MobileWorks", "Pune, India",
     ["Flutter", "Dart", "Firebase", "REST API", "Git"], 1, 4),

    ("Android Developer", "AppWorld", "Bangalore, India",
     ["Android", "Kotlin", "Java", "Firebase", "Git"], 1, 4),

    ("iOS Developer", "AppleTech Solutions", "Hyderabad, India",
     ["Swift", "iOS", "UIKit", "REST API", "Git"], 2, 5),

    ("Product Engineer", "BuildLabs", "Bangalore, India",
     ["Python", "React", "SQL", "Docker", "Git"], 2, 5),

    ("API Developer", "ServiceStack", "Remote, India",
     ["Python", "FastAPI", "REST API", "PostgreSQL", "Docker"], 1, 4),

    ("Django Developer", "WebSolutions India", "Delhi, India",
     ["Python", "Django", "PostgreSQL", "REST API", "Git"], 1, 4),

    ("FastAPI Developer", "ModernAPI", "Bangalore, India",
     ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Docker"], 1, 4),

    ("React Native Developer", "CrossPlatform Labs", "Mumbai, India",
     ["React Native", "JavaScript", "TypeScript", "Firebase", "Git"], 1, 4),

    ("Business Intelligence Analyst", "BI Solutions", "Pune, India",
     ["SQL", "Power BI", "Excel", "Python", "Tableau"], 1, 4),

    ("Data Visualization Analyst", "VisualData", "Mumbai, India",
     ["Python", "Power BI", "Tableau", "SQL", "Excel"], 1, 3),

    ("Cloud DevOps Engineer", "CloudScale", "Bangalore, India",
     ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD"], 3, 6),

    ("Senior Python Engineer", "PythonWorks", "Bangalore, India",
     ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"], 4, 7),

    ("Senior React Engineer", "FrontendPro", "Hyderabad, India",
     ["React", "TypeScript", "JavaScript", "Redux", "Git"], 4, 7),

    ("Senior Data Scientist", "DataMind", "Bangalore, India",
     ["Python", "Machine Learning", "SQL", "TensorFlow", "Pandas"], 4, 7),

    ("Senior Backend Engineer", "ScaleTech", "Pune, India",
     ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"], 4, 8),

    ("Technical Software Engineer", "TechBridge", "Remote, India",
     ["Python", "SQL", "REST API", "Git", "Linux"], 2, 5),
]


def request_json(url, data, token=None):
    body = json.dumps(data).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode())
        except Exception:
            detail = e.read().decode()
        return e.code, detail


print("=" * 60)
print("CareerMatch AI - Add 50 Jobs")
print("=" * 60)

email = input("Login email: ").strip()
password = getpass.getpass("Login password: ")

print("\nLogging in...")

status, login_response = request_json(
    f"{BASE_URL}/auth/login",
    {
        "email": email,
        "password": password,
    },
)

if status != 200:
    print(f"\nLogin failed ({status})")
    print(login_response)
    raise SystemExit(1)

token = login_response["access_token"]

print("Login successful.")
print(f"Adding {len(jobs)} jobs...\n")

success = 0
failed = 0

for number, job in enumerate(jobs, start=1):
    title, company, location, skills, exp_min, exp_max = job

    job_data = {
        "title": title,
        "company": company,
        "location": location,
        "description": (
            f"We are looking for a {title} to join {company}. "
            f"The candidate will work on software and technology projects "
            f"and collaborate with the engineering team."
        ),
        "skills": skills,
        "experience_min": exp_min,
        "experience_max": exp_max,
        "source_url": f"https://example.com/careermatch/job-{number}",
    }

    status, response = request_json(
        f"{BASE_URL}/jobs",
        job_data,
        token,
    )

    if status == 201:
        success += 1
        print(f"[{number:02}/50] ✓ {title} — {company} (ID: {response.get('id')})")
    else:
        failed += 1
        print(f"[{number:02}/50] ✗ {title} — HTTP {status}")
        print(f"       {response}")

print("\n" + "=" * 60)
print(f"Completed: {success} created, {failed} failed")
print("=" * 60)
