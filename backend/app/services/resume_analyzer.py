import re
from typing import Any


SKILL_KEYWORDS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "go",
    "rust",
    "php",
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "node.js",
    "nodejs",
    "express",
    "fastapi",
    "flask",
    "django",
    "spring",
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "mongodb",
    "redis",
    "oracle",
    "sqlite",
    "git",
    "github",
    "gitlab",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "computer vision",
    "nlp",
    "natural language processing",
    "pandas",
    "numpy",
    "matplotlib",
    "power bi",
    "tableau",
    "excel",
    "rest api",
    "restful api",
    "graphql",
    "microservices",
    "data structures",
    "algorithms",
]


SECTION_ALIASES = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technical expertise",
        "technologies",
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses",
    ],
}


def normalize_text(text: str) -> str:
    """Normalize resume text for consistent downstream analysis."""
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = []

    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line)
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def clean_heading(text: str) -> str:
    """Clean and normalize a detected resume section heading."""
    text = text.lower().strip()
    text = re.sub(r"[:\-]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def detect_section_heading(line: str) -> str | None:
    """Identify whether a line represents a known resume section."""
    cleaned = clean_heading(line)

    for section, aliases in SECTION_ALIASES.items():
        if cleaned in aliases:
            return section

    return None


def extract_sections(text: str) -> dict[str, str]:
    """Split resume text into recognized sections."""
    normalized = normalize_text(text)

    sections: dict[str, list[str]] = {}
    current_section = "general"

    sections[current_section] = []

    for line in normalized.split("\n"):
        detected = detect_section_heading(line)

        if detected:
            current_section = detected
            sections.setdefault(current_section, [])
            continue

        sections.setdefault(current_section, [])
        sections[current_section].append(line)

    return {
        section: "\n".join(lines).strip()
        for section, lines in sections.items()
        if lines
    }


def extract_skills(text: str) -> list[str]:
    """Extract recognized technical and professional skills from text."""
    normalized = text.lower()

    found = []

    for skill in SKILL_KEYWORDS:
        pattern = rf"(?<![a-zA-Z0-9+#.-]){re.escape(skill.lower())}(?![a-zA-Z0-9+#.-])"

        if re.search(pattern, normalized):
            found.append(skill)

    return sorted(set(found))


def extract_email(text: str) -> str | None:
    """Extract the first email address found in resume text."""
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text,
    )

    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    """Extract a likely phone number from resume text."""
    match = re.search(
        r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)",
        text,
    )

    if not match:
        return None

    phone = match.group(0).strip()

    digits = re.sub(r"\D", "", phone)

    if len(digits) < 10:
        return None

    return phone


def extract_name(text: str) -> str | None:
    """Infer the candidate's name from the beginning of the resume."""
    lines = normalize_text(text).split("\n")

    if not lines:
        return None

    excluded = {
        "resume",
        "cv",
        "curriculum vitae",
        "profile",
        "professional summary",
    }

    for line in lines[:5]:
        cleaned = line.strip()

        if cleaned.lower() in excluded:
            continue

        if "@" in cleaned:
            continue

        if re.search(r"\d", cleaned):
            continue

        words = cleaned.split()

        if 2 <= len(words) <= 5:
            return cleaned

    return None


def calculate_score(
    text: str,
    sections: dict[str, str],
    skills: list[str],
) -> int:
    """Calculate a resume quality score from content, sections, and skills."""
    score = 0

    if text:
        score += 15

    if len(text) >= 300:
        score += 10

    if len(text) >= 800:
        score += 5

    if sections.get("summary"):
        score += 10

    if sections.get("skills") or skills:
        score += 15

    if sections.get("education"):
        score += 10

    if sections.get("experience"):
        score += 15

    if sections.get("projects"):
        score += 10

    if sections.get("certifications"):
        score += 5

    return min(score, 100)


def analyze_resume(text: str) -> dict[str, Any]:
    """Analyze resume content and return structured candidate information."""
    normalized = normalize_text(text)

    sections = extract_sections(normalized)
    skills = extract_skills(normalized)

    score = calculate_score(
        normalized,
        sections,
        skills,
    )

    return {
        "name": extract_name(normalized),
        "email": extract_email(normalized),
        "phone": extract_phone(normalized),
        "summary": sections.get("summary"),
        "skills": skills,
        "education": sections.get("education"),
        "experience": sections.get("experience"),
        "projects": sections.get("projects"),
        "certifications": sections.get("certifications"),
        "sections": sections,
        "score": score,
    }
