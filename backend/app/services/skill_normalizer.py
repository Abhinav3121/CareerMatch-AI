import re


SKILL_ALIASES = {
    "python 3": "python",
    "python3": "python",

    "fast api": "fastapi",
    "fast-api": "fastapi",

    "postgres": "postgresql",
    "postgre sql": "postgresql",
    "postgre-sql": "postgresql",

    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "rest api": "rest api",

    "scikit learn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",

    "machine-learning": "machine learning",
    "machinelearning": "machine learning",

    "javascript": "javascript",
    "js": "javascript",

    "typescript": "typescript",
    "ts": "typescript",

    "react.js": "react",
    "reactjs": "react",

    "node.js": "node",
    "nodejs": "node",

    "c plus plus": "c++",
    "cpp": "c++",

    "c sharp": "c#",
    "csharp": "c#",

    "sql": "sql",

    "docker": "docker",
    "kubernetes": "kubernetes",
    "k8s": "kubernetes",

    "tensorflow": "tensorflow",
    "pytorch": "pytorch",

    "pandas": "pandas",
    "numpy": "numpy",

    "git": "git",
    "github": "github",

    "html5": "html",
    "css3": "css",
}


def normalize_skill(skill: str) -> str:
    """Normalize a skill into a consistent comparison form."""

    if not skill:
        return ""

    skill = str(skill).strip().lower()

    # Normalize whitespace.
    skill = re.sub(r"\s+", " ", skill)

    # Remove common punctuation around the skill.
    skill = skill.strip(".,;:()[]{}")

    # Apply aliases.
    skill = SKILL_ALIASES.get(
        skill,
        skill,
    )

    return skill


def normalize_skills(skills) -> list[str]:
    """Normalize a list of skills and remove duplicates."""

    if not skills:
        return []

    normalized = []

    for skill in skills:

        value = normalize_skill(skill)

        if value and value not in normalized:
            normalized.append(value)

    return normalized


def compare_skills(
    resume_skills,
    job_skills,
):
    """
    Compare resume skills against job-required skills.

    Returns:
        matched_skills
        missing_skills
        extra_skills
        match_percentage
    """

    resume = set(
        normalize_skills(resume_skills)
    )

    job = set(
        normalize_skills(job_skills)
    )

    matched = sorted(
        resume.intersection(job)
    )

    missing = sorted(
        job.difference(resume)
    )

    extra = sorted(
        resume.difference(job)
    )

    if not job:
        percentage = 0
    else:
        percentage = round(
            len(matched) / len(job) * 100,
            2,
        )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "match_percentage": percentage,
    }
