def analyze_answer(question, answer):
    answer = answer.lower()
    score = 0
    feedback = []

    keyword_db = {
        "What is OOP?": ["object", "class", "inheritance", "polymorphism"],
        "What is a list in Python?": ["ordered", "mutable", "elements"],
        "What is machine learning?": ["data", "algorithm", "learn"],
        "Difference between AI and ML?": ["ai", "ml", "subset"],
    }

    if question in keyword_db:
        keywords = keyword_db[question]
        matched = 0

        for word in keywords:
            if word in answer:
                matched += 1

        score = 5 + matched

        if matched == len(keywords):
            feedback.append("Excellent technical answer!")
        elif matched >= 2:
            feedback.append("Good answer but missing some key points.")
        else:
            feedback.append("Answer needs more technical details.")
    else:
        score = 5
        feedback.append("Basic answer recorded.")

    if len(answer.split()) < 6:
        feedback.append("Try to explain in more detail.")
        score -= 1

    if score > 10:
        score = 10

    return score, feedback