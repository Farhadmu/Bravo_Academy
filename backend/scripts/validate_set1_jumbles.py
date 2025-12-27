import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def check_jumble_word_validity():
    """Analyze all Set 1 jumble word questions for errors."""
    
    set1 = Test.objects.get(name='IQ Test - Set 1')
    questions = Question.objects.filter(test=set1).order_by('bank_order')
    
    errors_found = []
    
    # Known jumble word solutions (from question text)
    jumble_solutions = {
        'ATRCSFNAM': ('CRAFTSMAN', 'Name of a maker'),
        'RASMIARCH': ('ARMCHAIR', 'Name of a furniture'),
        'EGDIRBYEKNOM': ('MONKEYBRIDGE', 'Name of an obstacle'),  # MONKEY BRIDGE (compound)
        'FIDCFITULY': ('DIFFICULTY', None),
        'RESAUPLE': ('PLEASURE', 'Part of past time'),
        'RILSAO': ('SAILOR', 'Name of a profession'),
        'TEAYUB': ('BEAUTY', 'Part of attraction'),
        'ONHSEYT': ('HONESTY', 'Name of a virtue'),
        'YKSIWH': ('WHISKY', 'Name of a drink'),
        'EGAPR': ('GRAPE', 'Name of a fruit'),
        'LEICONET': ('ELECTION', 'Peoples Judgment'),
        'ROPAITR': ('AIRPORT', 'A busy place'),
        'PUMOCERT': ('COMPUTER', 'Name of a Machine'),
        'STIYUVNIER': ('UNIVERSITY', 'An educational institute'),
        'WASTRYRBER': ('STRAWBERRY', 'Name of a fruit'),
        'TRYMISHEC': ('CHEMISTRY', 'Name of a subject'),
        'RITEG': ('TIGER', 'Name of an animal'),
        'NESTIN': ('TENNIS', 'Name of a Game'),
        'LSARBIA': ('BARISAL', 'Name of a district'),
        'NHEPTOELE': ('TELEPHONE', 'Name of a media'),
        'TENCED': ('DECENT', 'Means graceful'),
        'VAPOPARL': ('APPROVAL', 'Means agreement'),
    }
    
    for q in questions:
        if 'jumble word' in q.question_text.lower():
            print(f"\\n=== Q{q.bank_order}: {q.question_text[:80]}...")
            
            # Extract jumble
            jumble = None
            for word in q.question_text.split():
                if word.isupper() and len(word) > 3:
                    jumble = word.replace('=', '').replace('.', '').replace(':', '')
                    break
            
            if jumble and jumble in jumble_solutions:
                solution, hint = jumble_solutions[jumble]
                print(f"Jumble: {jumble}")
                print(f"Solution: {solution}")
                
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
                
                if position_asked:
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
    
    print(f"\\n\\n{'='*60}")
    print(f"SUMMARY: Found {len(errors_found)} errors")
    print(f"{'='*60}")
    
    for err in errors_found:
        print(f"\\nQ{err['q_num']}: {err['jumble']} → {err['solution']}")
        print(f"  Position {err['position']}: Expected '{err['expected']}', Currently '{err['current']}'")
    
    return errors_found

if __name__ == "__main__":
    errors = check_jumble_word_validity()
