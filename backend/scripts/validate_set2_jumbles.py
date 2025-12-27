import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def check_set2_jumble_words():
    """Analyze all Set 2 jumble word questions for errors."""
    
    set2 = Test.objects.get(name='IQ Test - Set 2')
    questions = Question.objects.filter(test=set2).order_by('bank_order')
    
    errors_found = []
    
    # Known jumble word solutions from Set 2
    jumble_solutions = {
        # These will be populated as we analyze the questions
    }
    
    # First pass: collect all jumble words
    print("="*60)
    print("SET 2 JUMBLE WORD ANALYSIS")
    print("="*60)
    
    for q in questions:
        if 'jumble word' in q.question_text.lower() or 'rearrange' in q.question_text.lower():
            print(f"\n=== Q{q.bank_order}: {q.question_text[:80]}...")
            
            # Extract jumble
            jumble = None
            for word in q.question_text.split():
                cleaned = word.replace('=', '').replace('.', '').replace(':', '').replace(',', '')
                if cleaned.isupper() and len(cleaned) > 3:
                    jumble = cleaned
                    break
            
            if jumble:
                print(f"Jumble: {jumble}")
                
                # Try to find solution from explanation or question text
                solution = None
                if q.explanation:
                    # Look for "The word is X" pattern
                    if 'word is' in q.explanation:
                        parts = q.explanation.split('word is')
                        if len(parts) > 1:
                            solution = parts[1].split('.')[0].split()[0].upper()
                    elif 'answer is' in q.explanation:
                        parts = q.explanation.split('answer is')
                        if len(parts) > 1:
                            solution = parts[1].split('.')[0].split()[0].upper()
                
                if solution:
                    print(f"Solution: {solution}")
                    jumble_solutions[jumble] = solution
                    
                    # Find what position is asked
                    position_asked = None
                    if 'last letter' in q.question_text.lower():
                        position_asked = len(solution)
                    elif 'first letter' in q.question_text.lower() or '1st letter' in q.question_text.lower():
                        position_asked = 1
                    elif '2nd letter' in q.question_text.lower():
                        position_asked = 2
                    elif '3rd letter' in q.question_text.lower():
                        position_asked = 3
                    elif '4th letter' in q.question_text.lower():
                        position_asked = 4
                    elif '5th letter' in q.question_text.lower():
                        position_asked = 5
                    elif '6th letter' in q.question_text.lower():
                        position_asked = 6
                    elif '7th letter' in q.question_text.lower():
                        position_asked = 7
                    elif '8th letter' in q.question_text.lower():
                        position_asked = 8
                    
                    if position_asked and position_asked <= len(solution):
                        expected_letter = solution[position_asked - 1]
                        print(f"Position asked: {position_asked} (should be {expected_letter})")
                        
                        # Find correct answer letter
                        correct_option = None
                        for opt in q.options:
                            if opt['id'] == q.correct_answer:
                                correct_option = opt['text']
                                break
                        
                        print(f"Current answer: {q.correct_answer} = {correct_option}")
                        
                        if correct_option != expected_letter:
                            error_msg = f"Q{q.bank_order}: WRONG ANSWER! Expected {expected_letter}, got {correct_option}"
                            print(f"❌ {error_msg}")
                            errors_found.append({
                                'q_num': q.bank_order,
                                'q_id': q.id,
                                'jumble': jumble,
                                'solution': solution,
                                'position': position_asked,
                                'expected': expected_letter,
                                'current': correct_option,
                                'error': error_msg
                            })
                        else:
                            print(f"✓ Correct!")
                else:
                    print(f"⚠ Could not determine solution from explanation")
                    print(f"Explanation: {q.explanation}")
    
    print(f"\n\n{'='*60}")
    print(f"SUMMARY: Found {len(errors_found)} errors")
    print(f"{'='*60}")
    
    for err in errors_found:
        print(f"\nQ{err['q_num']}: {err['jumble']} → {err['solution']}")
        print(f"  Position {err['position']}: Expected '{err['expected']}', Currently '{err['current']}'")
    
    return errors_found

if __name__ == "__main__":
    errors = check_set2_jumble_words()
