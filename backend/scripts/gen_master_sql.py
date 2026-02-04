import json
import re
import os
import ast

def get_set_id_sql(test_name):
    return f"""
DO $$
DECLARE v_test_id UUID;
BEGIN
  SELECT id INTO v_test_id FROM tests WHERE name = '{test_name}';
  IF v_test_id IS NULL THEN
    RAISE NOTICE 'Test {test_name} not found';
  ELSE
    DELETE FROM questions WHERE test_id = v_test_id;
"""

def get_insert_sql(q, order, bank_prefix):
    text = q['text'].replace("'", "''")
    opts = json.dumps(q['options']).replace("'", "''")
    correct = q['correct']
    difficulty = q['difficulty']
    expl = q['explanation'].replace("'", "''")
    bank_order = bank_prefix + order
    
    return f"    INSERT INTO questions (id, test_id, question_text, question_type, options, correct_answer, difficulty_level, \"order\", explanation, created_at, updated_at, bank_order) " \
           f"VALUES (gen_random_uuid(), v_test_id, '{text}', 'mcq', '{opts}'::jsonb, '{correct}', '{difficulty}', {order}, '{expl}', NOW(), NOW(), {bank_order});"

def get_set_end_sql(count):
    return f"""
    UPDATE tests SET total_questions = {count} WHERE id = v_test_id;
  END IF;
END $$;
"""

def emit_questions_sql(test_name, questions_data, bank_prefix):
    print(get_set_id_sql(test_name))
    for i, q in enumerate(questions_data):
        print(get_insert_sql(q, i + 1, bank_prefix))
    print(get_set_end_sql(len(questions_data)))

def parse_pipe_set(test_name, raw_string, bank_prefix):
    lines = [line.strip() for line in raw_string.strip().split('\n') if line.strip()]
    questions_data = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < 5: continue
        text = parts[1]
        options_str = parts[2]
        correct = parts[3]
        explanation = parts[4]
        options = []
        for opt in options_str.split(','):
            if ':' in opt:
                opt_id, opt_text = opt.split(':', 1)
                options.append({"id": opt_id.strip(), "text": opt_text.strip()})
        questions_data.append({'text': text, 'difficulty': 'medium', 'options': options, 'correct': correct, 'explanation': explanation})
    emit_questions_sql(test_name, questions_data, bank_prefix)

def parse_regex_set(test_name, raw_string, bank_prefix):
    blocks = re.split(r'Question\s+\d+', raw_string.strip())
    blocks = [b.strip() for b in blocks if b.strip()]
    questions_data = []
    for idx, block in enumerate(blocks, 1):
        try:
            explanation_split = block.split('Explanation:')
            explanation_text = explanation_split[1].strip() if len(explanation_split) > 1 else ""
            remainder = explanation_split[0]
            answer_split = remainder.split('Answer:')
            answer_text = answer_split[1].strip() if len(answer_split) > 1 else ""
            remainder = answer_split[0]
            options_split = remainder.split('Options:')
            options_text = options_split[1].strip() if len(options_split) > 1 else ""
            q_text_raw = options_split[0].strip()
            q_text = q_text_raw[9:].strip() if q_text_raw.lower().startswith('question:') else q_text_raw
            options_list = []
            matches = re.findall(r'\(([a-e])\)\s*([^()]+)', options_text)
            for m in matches: options_list.append({"id": m[0].lower(), "text": m[1].strip()})
            correct_match = re.search(r'\(([a-e])\)', answer_text)
            correct_answer = correct_match.group(1).lower() if correct_match else ""
            questions_data.append({'text': q_text, 'difficulty': 'medium', 'options': options_list, 'correct': correct_answer, 'explanation': explanation_text})
        except Exception: continue
    emit_questions_sql(test_name, questions_data, bank_prefix)

if __name__ == "__main__":
    print("-- FINAL REFINED MASTER RESTORATION")
    print("BEGIN;")
    
    # Process Sets 2-10
    for i in range(2, 11):
        test_name = f"Verbal IQ Test - Set {i}"
        filename = f"scripts/seed_questions_set2.py" if i == 2 else f"scripts/seed_set{i}_complete.py"
        
        if not os.path.exists(filename): continue
            
        with open(filename, 'r') as f:
            content = f.read()
            
            if i == 2:
                # Robust extraction for Set 2
                start_ptr = content.find('raw_questions = [')
                # Find the corresponding closing bracket by looking for the one followed by # or newline+create
                # Actually, I'll just look for '# Create Questions in Database' which comes after the list
                end_ptr = content.rfind(']', 0, content.find('# Create Questions in Database')) + 1
                raw_data_str = content[start_ptr+16:end_ptr].strip()
                if not raw_data_str.endswith(']'): raw_data_str += ']'
                raw_data = ast.literal_eval(raw_data_str)
                
                questions_data = []
                for q_text, correct, opts, expl in raw_data:
                    options_json = [{'id': chr(97 + j), 'text': opt} for j, opt in enumerate(opts)]
                    correct_id = next((obj['id'] for obj in options_json if obj['text'] == correct), 'a')
                    questions_data.append({'text': q_text, 'difficulty': 'medium', 'options': options_json, 'correct': correct_id, 'explanation': expl})
                emit_questions_sql(test_name, questions_data, i * 100)
            elif i == 10:
                start = content.find('questions_raw = """') + 19
                end = content.find('"""', start)
                parse_regex_set(test_name, content[start:end], i * 100)
            else:
                start = content.find('ALL_QUESTIONS = """')
                if start == -1: start = content.find('questions_data = """')
                if start != -1:
                    start += content.find('"""', start) - start + 3
                    end = content.find('"""', start)
                    parse_pipe_set(test_name, content[start:end], i * 100)
            
    print("COMMIT;")
