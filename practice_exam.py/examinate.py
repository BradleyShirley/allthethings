import json
import random
import os

def list_json_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json')]

def choose_json_file(files):
    print("📚 Available Exams:\n")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {file}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the exam you'd like to take: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print("❌ Please enter a valid number.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def load_questions(filepath):
    print(f"\n📖 Loading questions from: {filepath}")
    with open(filepath, 'r') as f:
        return json.load(f)

def run_exam(questions):
    random.shuffle(questions)
    score = 0
    option_labels = ['a', 'b', 'c', 'd']

    for idx, q in enumerate(questions, 1):
        print(f"\nQuestion {idx}: {q['question']}")
        options = q['options']
        label_to_option = dict(zip(option_labels, options))

        for label in option_labels[:len(options)]:
            print(f"  {label}) {label_to_option[label]}")

        while True:
            choice = input("Your answer (a, b, c, d): ").lower()
            if choice in label_to_option:
                break
            else:
                print("❌ Invalid input. Try again.")

        selected = label_to_option[choice]
        if selected == q['answer']:
            print("✅ Correct!")
            score += 1
        else:
            correct_letter = [k for k, v in label_to_option.items() if v == q['answer']][0]
            print(f"❌ Incorrect. The correct answer is: {correct_letter}) {q['answer']}")

    total = len(questions)
    percentage = (score / total) * 100
    print(f"\n🎓 Exam completed! You scored {score}/{total} ({percentage:.2f}%)")

if __name__ == "__main__":
    print("🚀 examinate is running...\n")
    json_dir = "json"

    if not os.path.exists(json_dir):
        print(f"❌ JSON directory '{json_dir}' not found.")
    else:
        files = list_json_files(json_dir)
        if not files:
            print("❌ No .json files found in the 'json/' directory.")
        else:
            selected_file = choose_json_file(files)
            filepath = os.path.join(json_dir, selected_file)
            try:
                questions = load_questions(filepath)
                run_exam(questions)
            except json.JSONDecodeError as e:
                print(f"❌ Failed to load JSON: {e}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

