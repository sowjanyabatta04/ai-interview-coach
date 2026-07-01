import random
from questions import questions
from analyzer import analyze_answer
from ai_feedback import get_ai_feedback

candidate_name = input("Enter Candidate Name: ")
print(f"\nWelcome {candidate_name} to AI Interview Coach")

print("=== AI Interview Coach ===")
print("1. Python")
print("2. HR")
print("3. AI")

choice = input("Choose category: ")

if choice == "1":
    category = "Python"
elif choice == "2":
    category = "HR"
else:
    category = "AI"

score_list = []

question_list = questions[category].copy()
random.shuffle(question_list)

for round_num in range(5):
    print("\n----------------------")
    print("Round", round_num + 1)
    print("----------------------")

    question = question_list[round_num]
    print("Question:", question)

    answer = input("Your Answer: ")

    score, feedback = analyze_answer(question, answer)
    ai_feedback = get_ai_feedback(question, answer)
    score_list.append(score)

    print("Score:", score, "/10")
    print("Feedback:")
    for item in feedback:
        print("-", item)

    print("\nAI Feedback:")
    print(ai_feedback)

average = sum(score_list) / len(score_list)

print("\n====================")
print("Interview Completed")
print("====================")
print("Candidate Name:", candidate_name)
print("Final Average Score:", round(average, 2), "/10")