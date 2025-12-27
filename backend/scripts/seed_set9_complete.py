import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def parse_and_create_set9():
    print("Creating 'IQ Test - Set 9'...")
    
    # Create or get the test
    # Note: 'is_paid' field does not exist, derived from price > 0.
    # 'time_limit' is 'duration_minutes'
    set9, created = Test.objects.get_or_create(
        name="IQ Test - Set 9",
        defaults={
            "description": "Ninth set of IQ evaluation questions",
            "duration_minutes": 30,
            "price": 0.00,
            "is_active": True
            # 'is_free_sample' defaults to False
        }
    )
    
    if created:
        print(f"Created new test: {set9.name}")
    else:
        print(f"Found existing test: {set9.name}")

    # Raw content of the questions provided by user
    questions_data = """
Q01|You go miles north, then 3 miles west, then 9 miles south, again 3 miles east. How far are you from starting point now?|a:5 miles North,b:12 miles East,c:9 miles North West,d:2 miles South,e:6 miles SE|d|Horizontal movements cancel and vertical movement results in 2 miles south.
Q02|What fraction is 50 paisa of Tk 100?|a:1/100,b:1/200,c:100,d:200,e:500|a|50 paisa is 0.5 taka which is 1/100 of 100 taka.
Q03|Complete the series: 21, 5, 19, 9, ___ ?|a:11 15,b:15 13,c:12 14,d:15 11,e:11 13|e|The series alternates by -16 and +4.
Q04|If 2514 = Bead, 1945 = Aide, then double it to make a dozen. What is the number?|a:Fruit,b:Fatal,c:Frut,d:Frogt,e:Frick|a|Double of six letters makes twelve forming the word FRUIT.
Q05|Divide a number by 5 and then double it to make a dozen. What is the number?|a:30,b:24,c:12,d:36,e:20|a|30 ÷ 5 = 6 and doubling gives 12.
Q06|Complete the series: 7, 20, 10, 18, 13, 16, ___ ?|a:13 10,b:18 20,c:19 18,d:12 15,e:16 14|d|The series alternates +13 and -10.
Q07|Find the odd one out.|a:Ethiopia,b:Africa,c:Libiya,d:Egypt,e:Cameron|b|Africa is a continent while others are countries.
Q08|May is to August as M is to ___?|a:P,b:A,c:U,d:O,e:T|c|August starts with the same letter shift as May to August.
Q09|Complete the series: 2, 6, 2, 8, 4, 10, 5, ___ ?|a:10 5,b:8 16,c:15 11,d:12 8,e:12 16|d|The pattern alternates multiplication and addition.
Q10|Wash is to soap as Train is to ___?|a:Drive,b:Diesel,c:Railway,d:Master,e:Prevent|b|Soap is required to wash just as diesel is required to run a train.
Q11|Find the odd one out.|a:Recover & Region,b:Pray & Play,c:Ruin & Crush,d:Force & Compel,e:Dark & Shadow|a|They are not synonyms unlike the other pairs.
Q12|Monday is to April as Thursday is to ___?|a:May,b:June,c:August,d:July,e:March|d|Both represent the same positional order in week and months.
Q13|If 52318 = PROVE and 9728 = TYRE, then 5378297 = ___?|a:Poyetry,b:Poetrii,c:Tyoport,d:Ritopy,e:Poyerty|e|Each digit maps consistently to corresponding letters.
Q14|Find the odd one out.|a:Pray & Play,b:Plum & Pear,c:Mango & Orange,d:Pomegranate & Olive,e:Tree & Plant|a|All others are related to fruits or plants.
Q15|What is found once in OCTOBER, twice in NOVEMBER, but never in MARCH & AUGUST?|a:Eclipse,b:E,c:F,d:Tide,e:Sunlight|b|The letter "E" appears once in October and twice in November.
Q16|MIMTER is coded 121345 and YRT is 653. Then MTYR is ___?|a:1364,b:6584,c:1350,d:5312,e:1365|a|Each letter has a fixed numeric code value.
Q17|What is found in NAIL, FINGER & HAND but never in ARM?|a:Hair,b:Hard,c:W,d:Kytin,e:N|e|The letter "N" is common in the first three words only.
Q18|A's father Mr. Symon is uncle of my daughter and I have no sister. Mr. Symon has no daughter. What is A to me?|a:Sister,b:Brother,c:Cousin,d:Nephew,e:Uncle|b|Mr. Symon must be the father's brother making A my brother.
Q19|Rearrange: TSRAEWE and find the last letter.|a:T,b:S,c:H,d:W,e:R|d|The word rearranges to "SWEATER".
Q20|5 shirts dry in 1.5 hours and 2 pants dry in 2 hours. How long will 10 shirts and 4 pants take?|a:2.5 hrs,b:2 hrs,c:1.5 hrs,d:1 hr,e:3 hrs|c|Drying happens simultaneously so maximum time remains 1.5 hours.
Q21|Rearrange NUDHBAS (Relation). Fill the middle letter.|a:H,b:S,c:N,d:B,e:U|b|The word rearranges to "HUSBAND".
Q22|Find the first letter: HUCHCR (Religion)|a:C,b:H,c:R,d:U,e:S|b|The rearranged word is "CHURCH".
Q23|BREAD = 12345 & STREET = 782338, then DRESST = ___?|a:523748,b:783298,c:879327,d:952479,e:523778|b|Each letter retains its assigned numeric value.
Q24|Laugh is to cry as ___ is to sad.|a:Tears,b:Unfortunate,c:Pulse,d:Enjoy,e:Unhappy|d|Laugh is opposite of cry just as enjoy is opposite of sad.
Q25|"Flock of a father together birds" - comment.|a:True,b:False,c:Neither,d:Both,e:N/A|b|The correct proverb is "Birds of a feather flock together".
Q26|Rearrange the jumble word: MADTBINON (Games). Find the first letter.|a:t,b:a,c:n,d:m,e:b|d|The word rearranges to "BADMINTON".
Q27|Which one is odd?|a:Circle,b:Square,c:Triangle,d:Rhombus,e:Rectangle|a|Circle has no straight sides unlike the others.
Q28|If A = 3, B = 4, C = 5 and so on, then 4810 = ___?|a:BHF,b:CIG,c:BFH,d:CGI,e:BOK|c|Numbers map sequentially to alphabet values.
Q29|Foot is to walk as nose is to ___?|a:Smell,b:Eat,c:Wind,d:See,e:Feel|a|Foot is used to walk and nose is used to smell.
Q30|Complete the series: 10, C, 11, E, 13, G, 16, J, 20, K, 25, ___?|a:31 M,b:J 48,c:31 N,d:K 49,e:M 31|c|Numbers increase progressively while letters advance alphabetically.
Q31|The sum of age Arjoonazski & Birstnxy is 45 years. The difference between their ages is 5 years. What are their ages?|a:20 15,b:25 30,c:40 45,d:20 25,e:40 50|d|Two numbers whose sum is 45 and difference is 5 are 20 and 25.
Q32|Rearrange: LOFAUGWERIL (Vegetables). Fill the second last letter.|a:C,b:E,c:O,d:R,e:W|b|The rearranged word is CAULIFLOWER whose second last letter is E.
Q33|Steam is to Train as petrol is to ___?|a:Cart,b:Manual,c:Engine,d:Cycle,e:Barrel|c|Steam runs a train just as petrol runs an engine.
Q34|Rearrange and find similar: PITLLEUM|a:lpsdcine,b:easiernc,c:argud,d:rdgraen,e:oofl|d|PITLLEUM rearranges to MULTIPLE which matches GARDEN in pattern.
Q35|A spy is trying to send a secret message. "shnoppy droppy groppy" means (mission dangerously executed) and "swappy trappy droppy" means (abort mission immediately) and "drippy groppy wippy" means (plan executed successfully). Then what does "shnoppy" mean?|a:Mission,b:Abort,c:Executed,d:Dangerously,e:Successfully|d|Shnoppy appears only in the phrase meaning dangerously executed.
Q36|July had a number of raisins. After eating one, she gave half the remainder to her sister. After eating another raisin, she gave a third of what was left to her brother. Judy now had only six raisins left. How many raisins did she start with?|a:35,b:42,c:21,d:45,e:51|b|Working backwards gives the original number as 42.
Q37|Latoya is taller than Kito, and Mike is shorter than Latoya. Which would be most accurate?|a:Kito is shorter,b:Mike is taller than Kito,c:Mike is shorter than Kito,d:Mike is as tall as Kito,e:It is impossible to tell who is taller/shorter|e|No direct height comparison between Mike and Kito is given.
Q38|Complete the series: 7, C, 10, E, 15, G, 22, I, ___?|a:31 K,b:41 L,c:K 49,d:46 J,e:M 31|a|Numbers increase by +3, +5, +7, +9 while letters skip one alphabet each time.
Q39|"Oop nostrum signi" means "You eat lead", "Nostrum inglbot inx" means "How you read", "Ogslim inx blit" means "How are fireworks", Blit means Are. Now tell "How are you"?|a:Oop signi inx,b:nostrum signi inglbot,c:nostrum Oop signi,d:inx blit nostrum,e:inx inglbot blit|e|Words common to known phrases map correctly to "How are you".
Q40|The day before yesterday was three days after Saturday. Today is ___?|a:Mon,b:Tue,c:Thu,d:Wed,e:Fri|d|Three days after Saturday is Tuesday making today Wednesday.
Q41|Fill in the gap: 5, 16, 49, ___, 445|a:240,b:132,c:148,d:164,e:192|d|Each term follows the pattern x3 +1.
Q42|As a store, you cut the price 40% for a particular item. By what percent must the item be increased if you want to sell it at the original price?|a:66.70%,b:30.00%,c:40.00%,d:45.00%,e:50.00%|a|A 40% reduction requires a 66.7% increase to return to original price.
Q43|Which one letter does not belong in the series: D-F-H-J-N-P-R|a:H,b:K,c:J,d:N,e:P|d|All letters follow a +2 pattern except N which breaks the sequence.
Q44|Mike, six years old, is twice as old as his brother. How old will Mike be when he is one and a half times as old as his brother?|a:10,b:7,c:8,d:9,e:12|a|At age 10, Mike will be 1.5 times his brother's age.
Q45|Imagine numbers 1 through 30 written in a row; if you add any two adjacent numbers, you always get an odd number.|a:False,b:True,c:Neither,d:Both,e:None|b|Each adjacent pair contains one odd and one even number.
Q46|Which one of the series is wrong and should be replaced? 2-4-16-20-22-44|a:4,b:8,c:16,d:44,e:22|e|The correct pattern alternates x2 and x4.
Q47|P is the father of Q but Q is not the son of P. What is the relationship between Q and P?|a:Daughter,b:Father and mother,c:Brother and sister,d:None,e:Uncle & nephew|a|If Q is not a son, Q must be a daughter.
Q48|Complete the series: 10, 18, 11, 17, 14, 16, ___?|a:20 25,b:22 28,c:19 18,d:15 22,e:19 15|e|The pattern alternates increasing and decreasing sequences.
Q49|Rearrange and find similar: ATCKTA|a:blade,b:tree,c:tower,d:diellors,e:dofo|b|ATCKTA rearranges to TACKTA matching TREE in letter pattern.
Q50|If some trees stand in a straight row 400 meters apart on both sides of the road, how many trees are required in 2 km roads?|a:10,b:20,c:11,d:22,e:12|d|2 km gives 6 intervals per side resulting in 11 trees per side.
Q51|If the day after tomorrow is Tuesday, what is the day before yesterday?|a:Mon,b:Tue,c:Wed,d:Thu,e:Fri|a|If day after tomorrow is Tuesday then today is Sunday.
Q52|Complex: X, 2, T, 9, P, 28, L, 65, H, 126, ___?|a:D 215,b:F 217,c:D 217,d:E 196,e:E 217|c|Letters move backward by four while numbers follow n^3 + 1.
Q53|At the end of a banquet 10 people shake hands with each other. How many handshakes will there be in total?|a:45,b:20,c:100,d:50,e:90|a|Each person shakes hands once with every other person, so total handshakes = n(n-1)/2.
Q54|Complete: Y, 2, U, 9, Q, 28, M, 65, I, __, __, 217 ?|a:126 D,b:126 E,c:132 F,d:120 G,e:119 H|a|Numbers follow n^3+1 and letters move backward by 4 positions.
Q55|You are at a field. Go 8 miles north, then 6 miles east to pond. What is the distance from field to pond?|a:16,b:15,c:10,d:6,e:36|b|Distance is square root of (8^2 + 6^2) using the Pythagorean theorem.
Q56|If the word NECK is written above SALT and SALT above BLIP, then NAIL is formed diagonally. True or False?|a:F,b:True,c:False,d:T,e:Columbus|b|Diagonal letters N-A-I-L can be correctly traced.
Q57|Complete: 2, B, 5, D, 11, F, 20, H, 32, J, __ ?|a:L 47,b:27 M,c:28 K,d:47 L,e:47 K|d|Numbers increase by +3, +6, +9... and letters advance by 2.
Q58|"If some Toogs and Bloogs and all Gleems are Bloogs, then some Toogs are definitely Gleems."|a:Neither,b:True,c:False,d:Both,e:Only Toogs|c|There is no definite logical connection between Toogs and Gleems.
Q59|A thief saw a picture which is his father-in-law's grandson. What is the relation?|a:Niece,b:Son,c:Uncle,d:Brother,e:Sister|b|Father-in-law's grandson through wife is the thief's son.
Q60|If MANILLA = BDEGFFD and YAC = ZDH, then CAMALLA = ?|a:FGDHDBD,b:DBDHFGD,c:BDHDFGD,d:GDHDBDF,e:HDBDRGD|c|Each letter is replaced by the next consonant sequence.
Q61|What comes next: 2, F, 5, J, 10, N, __, 26, V|a:17 S,b:19 R,c:17 R,d:20 P,e:19 T|c|Numbers increase by +3, +5, +7 and letters by +4.
Q62|Complete the series: 78, 72, 60, 54, 42, 36, __ ?|a:17 24,b:24 20,c:16 18,d:24 18|d|Each number decreases alternately by 6 and 12.
Q63|Rearrange GUARD BIRME B (Obstacle), find last letter.|a:R,b:A,c:E,d:G,e:B|a|Rearranged word is "BARRICADE" whose last letter is R.
Q64|CJKL = GMTV as ICMA = ?|a:MFVK,b:MFKV,c:MKVF,d:MVKF,e:MVFK|e|Each letter shifts forward by +4, +4, +4, +4.
Q65|Rearrange ATNDGMORHRE, find the last letter.|a:O,b:D,c:M,d:R,e:C|d|Rearranged word is "HEADMASTER" which ends with R.
Q66|3,Y,6,W,12,U,21,S,33,__ ?|a:38 S,b:R 63,c:P 47,d:48 Q,e:Q 48|d|Numbers increase by +3, +6, +9, +12 and letters move backward by 2.
Q67|Complete: 7, 13, 19, 25, 31, __ ?|a:36 40,b:37 43,c:37 41,d:36 43,e:43 36|b|The series increases consistently by +6.
Q68|14, 42, 21, 63, 31.5, 94.5, __ ?|a:94.5,b:87,c:74,d:63,e:99|d|The pattern alternates x3 and /2.
Q69|Complete: 8, 3, 9, 4, 10, 5, 11, __ ?|a:7 12,b:12 14,c:6 13,d:6 12,e:6 14|c|Two interleaved sequences increasing by +1.
Q70|Rearrange RNERIMA (a profession), find the second letter.|a:E,b:A,c:N,d:M,e:I|b|Rearranged word is "MARINER" whose second letter is A.
Q71|Complete: 15, 29, 59, 119, 239, __ ?|a:458 959,b:479 957,c:458 959,d:959 477,e:479 959|e|Each term is (previous x2) - 1.
Q72|Rearrange RICTHPE (household chores), find last letter.|a:P,b:C,c:S,d:R,e:E|c|Rearranged word is "PITCHER S" -> "CHORES = PITCHES" ending with S.
Q73|Two planes leave at 1:00 pm, one North at 150 mph and one West at 20 mph; distance at 3:00 pm?|a:50,b:100,c:500,d:700,e:900|c|Distances are 300 and 40 miles, so square root of (300^2 + 40^2) is approx 500.
Q74|If ADD = 122, KISS = 3455, CLASS = 67155 then SAD = ?|a:534,b:551,c:125,d:512,e:345|a|Each letter is replaced by its alphabetical position.
Q75|"Nero fiddles while Rome burns", the sentence is __ ?|a:None,b:Both,c:True,d:False,e:Both a & b|d|The statement is historically inaccurate.
Q76|Z, 82, W, 65, T, 50, Q, 37, __ ?|a:N 26,b:N 35,c:M 24,d:O 28,e:P 26|a|Letters move back by 3 and numbers decrease progressively.
Q77|CFJ, KPU, HQ, __ ?|a:X,b:W,c:C,d:Z,e:D|d|Alphabet gaps increase consistently.
Q78|Find the odd: Bullock, Cart, Truck, Car, Wagon|a:Bullock,b:Cart,c:Truck,d:Car,e:Wagon|a|Bullock is an animal, others are vehicles.
Q79|Find the odd: Principal, Professor, Headmaster, Teacher, Student|a:Principal,b:Professor,c:Headmaster,d:Teacher,e:Student|e|Student is not a teaching or administrative profession.
Q80|Rearrange: "The largest planet in our solar system is Jupiter". Statement is -|a:False,b:None,c:Both,d:N/A,e:True|e|Jupiter is scientifically proven to be the largest planet in the solar system.
Q81|Rearrange: UPNKPIM, related with -|a:war,b:insect,c:vegetables,d:fish,e:fruits|b|UPNKPIM rearranges to "PUMPKIN" which is associated with insects in farming context.
Q82|Divide 500 into two parts such that one third of the first part is more by 60 than one fifth of the second part.|a:300 200,b:200 369,c:261 200,d:100 200,e:300 400|a|One-third of 300 exceeds one-fifth of 200 by exactly 60.
Q83|Complete the series: 8, 24, 2, 4, 30, 5, 4, __, 11|a:35,b:66,c:42,d:38,e:52|a|The series alternates between multiplication and addition patterns.
Q84|Command is to direction as prohibit is to -|a:Defy,b:fearless,c:daring,d:courage,e:exclude|a|Command relates to obey, while prohibit relates to defy.
Q85|Find odd:|a:Orange,b:Banana,c:Carrot,d:Lychee,e:Jackfruit|c|Carrot is a vegetable while others are fruits.
Q86|Rearrange OACLCACO (DRINK), find the second last letter -|a:L,b:C,c:A,d:O,e:A|a|OACLCACO rearranges to "COCA COLA" and the second last letter is L.
Q87|There are two planets between the Sun and Earth, which are that?|a:Moon & Neptune,b:Mercury & Saturn,c:Pluto & Mercury,d:Saturn & Venus,e:Mercury & Venus|e|Mercury and Venus lie between the Sun and Earth.
Q88|Complete the series: 7, 3, 17, 9, 27, 81, __ ?|a:85 6561,b:37 6561,c:34 7571,d:37 8524,e:36 6560|b|The pattern alternates addition and squaring.
Q89|The difference between two numbers is 20 and their sum is 122. Which are these?|a:67 54,b:70 52,c:74 55,d:71 51,e:76 46|b|70 - 52 = 18 and 70 + 52 = 122 satisfies the condition.
Q90|Rearrange SUEPL (crops), find the last letter -|a:G,b:O,c:R,d:P,e:E|d|SUEPL rearranges to "PULSE" whose last letter is E but crop root is PULP.
Q91|If GUIDE = 70945 & ARDENT = 134586, so GARDEN stands for -|a:713458,b:758134,c:734158,d:713834,e:713481|e|Each letter corresponds to its mapped digit from previous words.
Q92|Find the odd man out:|a:pleasant,b:Fine,c:Lovely,d:Awkward,e:Beautiful|d|Awkward has a negative meaning while others are positive.
Q93|Quran is the Muslim Bible is to -|a:Buddha,b:Hindu,c:Muslim,d:Christian,e:Mankind|c|The Quran is the holy book of Muslims.
Q94|Medicine is to Patient as Education is to -|a:Man,b:Woman,c:Male,d:Female,e:Student|e|Medicine is given to patients just as education is given to students.
Q95|Ice is to cold as Fire is to -|a:Burn,b:Hot,c:Cold,d:Ice,e:Fire|b|Ice represents coldness and fire represents heat.
Q96|Which is different from the rest?|a:Yen,b:Roubles,c:Dollar,d:Pound,e:Pice|e|Pice is an obsolete currency while others are still in use.
Q97|Which is different from the rest?|a:Cat,b:Dog,c:Donkey,d:Puppy,e:Horse|d|Puppy is a young animal while others are adult animals.
Q98|Water is liquid as stone is to -|a:Hard,b:Crick,c:Weight,d:Solid,e:Strong|d|Water is a liquid and stone is a solid.
Q99|Personality disorder is called -|a:Neuritis,b:Neuralgia,c:Neurosis,d:Abnormal,e:Normal|c|Neurosis refers to mental or personality disorders.
Q100|Food is to man as fuel is to -|a:Orange,b:Apple,c:Wheat,d:Rice,e:Sweet|e|Fuel provides energy just as food provides energy.
"""
    
    # Process line by line
    print(f"Parsing questions for {set9.name}...")
    lines = [line for line in questions_data.strip().split('\n') if line.strip()]
    
    # Starting offset for questions
    start_bank_order = 801
    
    for idx, line in enumerate(lines, 1):
        parts = line.split('|')
        if len(parts) < 5:
            print(f"Skipping invalid line: {line}")
            continue
            
        q_id_str = parts[0] # e.g., Q01
        question_text = parts[1]
        options_raw = parts[2]
        correct_answer = parts[3].strip().lower() # e.g., 'd'
        explanation = parts[4]
        
        # Parse options into list of dicts for JSONField
        # Format: a:Option A,b:Option B,...
        options_list = []
        opts = options_raw.split(',')
        for opt in opts:
            if ':' in opt:
                key, val = opt.split(':', 1)
                options_list.append({"id": key.strip().lower(), "text": val.strip()})
            else:
                # Fallback if delimiter missing, though data seems consistent
                # Assign generic IDs or try to heuristic split? 
                # Given the data provided, it seems consistent with a:...,b:...
                # logic handle potentially missing colon
                pass

        # Use update_or_create to prevent duplicates on potential re-runs
        Question.objects.update_or_create(
            test=set9,
            order=idx,
            defaults={
                "question_text": question_text,
                "question_type": "mcq",
                "options": options_list,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "difficulty_level": "medium",
                "bank_order": start_bank_order + (idx - 1)
            }
        )
        
        if idx % 10 == 0:
            print(f"  Created {idx} questions...")
    
    print(f"\n✓ Successfully created {len(lines)} questions for {set9.name}!")
    print(f"  Total questions in database: {Question.objects.filter(test=set9).count()}")
    
    return set9

if __name__ == "__main__":
    parse_and_create_set9()
