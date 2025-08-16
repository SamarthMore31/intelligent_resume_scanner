# utils/file_loader.py

def load_jd_skills_with_weights(jd_path):
    """
    Loads skills from JD text file and assigns weights based on importance.
    Only skills present in the JD are returned.
    """
    with open(jd_path, 'r', encoding='utf-8') as f:
        jd_text = f.read().lower()

    # Define skill weights — tweak freely
    skill_weights = {
        'python': 3,
        'machine learning': 3,
        'deep learning': 2,
        'tensorflow': 2,
        'communication': 1,
        'java': 1,
        'c++': 1,
        'sql': 1,
    }

    # Return only those skills actually mentioned in the JD
    matched_skills = {
        skill: weight
        for skill, weight in skill_weights.items()
        if skill in jd_text
    }

    return matched_skills


def load_jd_skills_with_weights_from_text(jd_text):
    """
    Loads skills from a given JD text string and assigns weights.
    Use this when you already have JD content as string (e.g. from uploaded file).
    """
    jd_text = jd_text.lower()

    skill_weights = {
        'python': 3,
        'machine learning': 3,
        'deep learning': 2,
        'tensorflow': 2,
        'communication': 1,
        'java': 1,
        'c++': 1,
        'sql': 1,
    }

    matched_skills = {
        skill: weight
        for skill, weight in skill_weights.items()
        if skill in jd_text
    }

    return matched_skills
