def analyze_answer(question, answer):
    feedback = []
    score = 0

    answer = answer.strip()
    word_count = len(answer.split())

    # Empty answer
    if word_count == 0:
        return 0, ["No answer given."]

    # Very short answer (1-3 words)
    if word_count <= 3:
        score = 1
        feedback.append("Answer is too short.")
        feedback.append("Please explain in detail.")

    # Short answer (4-8 words)
    elif word_count <= 8:
        score = 3
        feedback.append("Short answer.")
        feedback.append("Add explanation and examples.")

    # Medium answer (9-20 words)
    elif word_count <= 20:
        score = 5
        feedback.append("Decent answer.")
        feedback.append("Can be more detailed.")

    # Good answer (21-40 words)
    elif word_count <= 40:
        score = 7
        feedback.append("Good answer.")
        feedback.append("Clear explanation.")

    # Excellent answer (40+ words)
    else:
        score = 9
        feedback.append("Excellent answer.")
        feedback.append("Detailed and well explained.")

    # Bonus for useful keywords
    keywords = [
        "python", "team", "project", "experience",
        "problem", "solution", "learning", "skill"
    ]

    bonus = 0
    lower_answer = answer.lower()

    for word in keywords:
        if word in lower_answer:
            bonus += 0.5

    score += bonus

    if score > 10:
        score = 10

    return round(score), feedback