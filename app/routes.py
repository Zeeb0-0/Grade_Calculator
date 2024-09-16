from flask import render_template, request
from app import app

def calculate_grades(prelim, passing_grade=75):
    """Calculate the minimum required Midterm and Final grades needed to pass."""
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50

    # Calculate the weighted Prelim contribution
    prelim_contribution = prelim * prelim_weight

    # Check if it's mathematically possible to pass
    max_possible_score = prelim_contribution + (100 * midterm_weight) + (100 * final_weight)
    if max_possible_score < passing_grade:
        return None, None

    # Required overall remaining score to achieve a passing grade
    remaining_score = passing_grade - prelim_contribution

    # Set up a simplified equation to calculate required Final grade based on Midterm:
    def required_final(midterm):
        return (remaining_score - (midterm * midterm_weight)) / final_weight

    return required_final, remaining_score

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    prelim = None
    impossible = False
    midterm_needed = None
    final_needed = None

    if request.method == 'POST':
        try:
            prelim = float(request.form['prelim'])

            if prelim < 0 or prelim > 100:
                raise ValueError("Grade must be between 0 and 100.")

            required_final, remaining_score = calculate_grades(prelim)

            if required_final is None:
                impossible = True
            else:
                # Example with Midterm grade of 75, and calculating required Final grade
                midterm_needed = 75
                final_needed = required_final(midterm_needed)

                # If the required Final grade is greater than 100, mark it impossible
                if final_needed > 100:
                    impossible = True
                    final_needed = None  # Clear the impossible value for clarity

        except ValueError:
            error = "Please enter a valid numerical grade between 0 and 100."

    return render_template(
        'index.html',
        prelim=prelim,
        error=error,
        impossible=impossible,
        midterm=midterm_needed,
        final=final_needed
    )
