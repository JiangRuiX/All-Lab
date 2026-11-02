def get_student_data():
    """Prompt the user for a student name and score."""
    name  = input("Student name: ")
    score = float(input("Score (0-100): "))
    return name, score


def calculate_grade(score):
    """Return a letter grade for a numeric score."""
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"


def print_result(name, score, grade):
    """Print a formatted student result."""
    print("-" * 30)
    print(f"Student: {name}")
    print(f"Score:   {score:.1f}")
    print(f"Grade:   {grade}")
    print("-" * 30)


# Main program
name, score = get_student_data()
grade       = calculate_grade(score)
print_result(name, score, grade)
