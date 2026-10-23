
"""AI Resume Matcher - A beginner NLP portfolio project."""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = {
    "python", "sql", "java", "c++", "machine learning",
    "deep learning", "pandas", "numpy", "scikit-learn",
    "data analysis", "git", "github", "flask", "fastapi",
    "tensorflow", "pytorch", "nlp", "statistics"
}


def normalize(text: str) -> str:
    """Normalize text for basic skill matching."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> set[str]:
    """Find known skills mentioned in the text."""
    normalized = normalize(text)
    found = set()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, normalized):
            found.add(skill)

    return found


def compare_resume(resume: str, job: str) -> None:
    """Compare resume text with a job description."""
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume, job])

    score = cosine_similarity(
        vectors[0], vectors[1]
    )[0][0] * 100

    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job)

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    print("\n--- AI Resume Matcher Report ---")
    print(f"Text similarity: {score:.2f}%")
    print("\nMatching skills:")
    print(", ".join(sorted(matched)) or "None detected")
    print("\nSkills mentioned in job but not resume:")
    print(", ".join(sorted(missing)) or "None detected")
    print("\nNote: Similarity is not a hiring probability.")


def main() -> None:
    print("AI Resume Matcher")
    resume = input("\nPaste resume text: ").strip()
    job = input("\nPaste job description: ").strip()

    if not resume or not job:
        print("Error: Both inputs are required.")
        return

    try:
        compare_resume(resume, job)
    except ValueError as error:
        print(f"Could not compare the text: {error}")


if __name__ == "__main__":
    main()
