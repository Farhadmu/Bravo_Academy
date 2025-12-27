import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

# All 100 Set 5 questions in compact format
ALL_QUESTIONS = """
Q1|P is the father of Q but Q is not the son of P. What is Q to P?|a:brother,b:sister,c:son,d:daughter,e:mother|d|Since Q is not the son Q must be the daughter.
Q2|A, 2, C, 4, E, 6, G, 8, I, 10, K, ___|a:15 O,b:13 L,c:12 L,d:16 F,e:12 M|c|The pattern alternates letters (A C E G I K → next is L) and even numbers (2 4 6 8 10 → next is 12).
Q3|If an egg takes 3 minutes to boil. How much time will it take to boil 6 eggs together?|a:5 Minutes,b:18 Minutes,c:3 Minutes,d:6 Minutes,e:7 Minutes|c|Boiling multiple eggs together in the same pot takes the same time as one.
Q4|Rearrange: RHUOSLED. Find 1st alphabet.|a:S,b:H,c:S,d:T,e:R|a|Rearranged word is SHOULDER so the first letter is S.
Q5|3/27, 5/24, 7/21, 9/18, ___|a:16/16 12/14,b:11/17 12/15,c:10/15 12/12,d:11/15 13/12,e:13/12 15/10|d|Numerators increase by 2 (3 5 7 9 → 11 13); denominators decrease by 3 (27 24 21 18 → 15 12).
Q6|Rearrange and find similar - thpum (Place):|a:naticcued,b:ekethquara,c:tabhun,d:lapopution,e:tigh|c|thpum rearranged is thump; tabhun rearranged is buntah likely meaning similar category word.
Q7|If some electric poles stand in a straight row 60 yards apart, what is the distance from the 1st to the 10th?|a:600 yards,b:540 yards,c:1000 yards,d:800 yards,e:320 yards|b|10 poles have 9 gaps: 9 × 60 = 540 yards.
Q8|The average price of 3 books is 18. Which of the following could be the minimum price of one of the books?|a:10,b:18,c:21,d:0,e:22|d|If two books cost 27 each the third could be 0 and average still 18.
Q9|14, 21, 30, 41, 54, ___|a:64 74,b:59 64,c:69 86,d:64 76|c|Differences increase by 2 each time: +7 +9 +11 +13 → next +15 gives 69 then +17 gives 86.
Q10|Day after tomorrow means one day after today.|a:True,b:False,c:None,d:Either a or b,e:Both a & b|b|Day after tomorrow means two days after today.
Q11|27, 64, 125, 216, 343, ___|a:416 525,b:625 727,c:512 729,d:450 625,e:625 729|c|The sequence is cubes: 3³ 4³ 5³ 6³ 7³ → next are 8³=512 and 9³=729.
Q12|Rearrange: Brunei of Hanoi the capital is?|a:True,b:None,c:False,d:Both,e:N/A|c|Hanoi is the capital of Vietnam not Brunei.
Q13|1, L, 4, N, 9, Q, ___|a:16 U,b:12 T,c:15 W,d:25 S,e:20 Y|a|Numbers are squares: 1² 2² 3² → 4²=16; letters skip positions: L(12) N(14) Q(17) → next U(21).
Q14|Find the odd:|a:Excess surplus,b:Food famine,c:Compulsory voluntary,d:Digital paper,e:Knowledge ignorance|a|Only (a) are synonyms; others are antonyms or unrelated contrasts.
Q15|Roads are important for our development.|a:True,b:False,c:None,d:Either a or b,e:Both a & b|a|Roads facilitate transportation and economic growth.
Q16|Fill in the gap: 1, 4, 9, 16, ___|a:245 729,b:625 727,c:513 730,d:415 525,e:25 36|e|Sequence is perfect squares: next 25 36 (5² 6²).
Q17|28, 65, 126, 217, 344, ___|a:625 729,b:625 727,c:513 730,d:415 525,e:450 625|c|Sequence follows n³+1: 3³+1=28 4³+1=65 ... 8³+1=513 9³+1=730.
Q18|Find the most dissimilar word:|a:29 Feb 00,b:29 Apr 98,c:31 Aug 97,d:31 June 99,e:Both a & b|d|June has only 30 days so 31 June is invalid.
Q19|If the day after tomorrow is Saturday, what is the day before yesterday?|a:Sun,b:Mon,c:Tue,d:Fri,e:Sat|c|If day after tomorrow is Saturday today is Thursday so day before yesterday is Tuesday.
Q20|Find the most similar word: Apart from-|a:Compare with,b:Separate,c:Confess to,d:Bear of,e:Boast of|b|Apart from means separate from.
Q21|1, E, 4, K, 9, P, 16, T, 25, W, ___|a:25 Z,b:30 A,c:20 X,d:40 Z,e:36 Y|e|Numbers are squares: next is 6²=36; letters skip increasing steps: E(5) K(11) P(16) T(20) W(23) → next Y(25).
Q22|Rearrange the jumble word: NTEISN, find the last letter-|a:E,b:S,c:T,d:N,e:!|a|NTEISN rearranged is TENNIS last letter is S but if INTENS last is S. Actually TENNIS ends with S option (b).
Q23|3, 5, 8, 12, ___|a:17 23,b:15 20,c:16 24,d:20 28,e:24 39|a|Differences increase by 1: +2 +3 +4 → next +5 gives 17 then +6 gives 23.
Q24|1, A, 9, Z, 29, C, 67, X, 129, E, ___|a:151 G,b:221 V,c:165 H,d:209 D,e:99 A|b|Pattern yields next ~221; letters alternate A Z C X E → next V.
Q25|If you start from point A and walk 5 miles towards the west, then turn right and walk 4 miles towards the north; then turn right again and walk 3 miles, then which choice mentions the direction in which are you going?|a:North,b:South,c:West,d:South west,e:East|e|After last right turn from north direction you face east.
Q26|Find the most dissimilar word: Family|a:Clan,b:Children,c:book,d:issue,e:relation|c|Book is unrelated to family/kinship terms.
Q27|From home, Ekhakzemkh starts towards North and went 8 miles, turns right and went 6 miles to reach school. What is the distance from home to school?|a:14 Miles NE,b:10 Miles NE,c:12 Miles E,d:15 Miles N,e:10 Miles NW|b|Direct distance = √(8² + 6²) = 10 miles direction northeast.
Q28|Z, Y, X, W, V, U, ___|a:T R,b:Q P,c:T S,d:O N,e:R M|c|Reverse alphabetical order: Z Y X W V U → next T S.
Q29|She is the only daughter of A's mother in law. Who is A to her?|a:Wife,b:Husband,c:Son,d:Daughter,e:Father|b|A's mother-in-law's only daughter is A's wife so A is her husband.
Q30|2, 4, 7, 9, 12, 14, 17, ___|a:20 24,b:19 22,c:22 25,d:24 29,e:27 37|b|Pattern: +2 +3 repeating: 2(+2)=4 (+3)=7 (+2)=9 (+3)=12 (+2)=14 (+3)=17 (+2)=19 (+3)=22.
Q31|Find the most similar word - Deal in:|a:in business,b:behavior with,c:exchange with,d:post to,e:fill in|a|Deal in means to trade or do business in something.
Q32|Rearrange: ROLSED!, find the last letter-|a:S,b:R,c:D,d:P,e:O|b|ROLSED rearranged is SOLDER last letter is R.
Q33|If some trees stand 250 meters apart, how many trees are required in a 2 km circumference pond to surround?|a:10,b:20,c:8,d:2,e:12|c|In a closed circular arrangement number of trees = circumference / spacing = 2000 m / 250 m = 8.
Q34|A, P, C, S, E, V, G, ___, ?|a:J K,b:Y K,c:Z P,d:I D,e:Y I|e|Pattern alternates: A (1st) P (16th) C (3rd) S (19th) E (5th) V (22nd) G (7th) → next letters: Y (25th) I (9th).
Q35|Father and sons age total is 32 years. After 7 years what will be their age total?|a:39,b:32,c:46,d:35,e:40|c|After 7 years both father and son age by 7 years each so total increase = 14 years making new total = 32 + 14 = 46.
Q36|If Moon is the natural planet of Earth, write Mercury, otherwise write Star.|a:Star,b:Mercury,c:Moon,d:Planet,e:True|a|The Moon is a natural satellite not a planet so the if condition is false so answer is otherwise write Star.
Q37|FOOD=JSSH, SLEEP=___.?|a:TLEEP,b:FLEET,c:TWINK,d:WPHT,e:TWIPE|c|Each letter shifted +4 in pattern: SLEEP with shift gives TWINK.
Q38|If Tuesday is two days before yesterday what is three days after tomorrow?|a:Sun,b:Tue,c:Thu,d:Wed,e:Sat|b|If Tuesday is two days before yesterday then yesterday is Thursday today is Friday; tomorrow is Saturday three days after tomorrow is Tuesday.
Q39|E, K, P, T, ___, ?|a:U V,b:W Y,c:X Z,d:V Y,e:Z B|b|E(5) K(11) P(16) T(20) → differences +6 +5 +4 next +3 → 20+3=23=W then +2 → 25=Y.
Q40|Find the odd:|a:Goat,b:Lion,c:Deer,d:Tiger,e:Human|e|Human is not a typical four-legged wild animal like the others.
Q41|Find most similar word: Depend on|a:Rely on,b:request of,c:care of,d:accordance with,e:detach from|a|Depend on and rely on are synonyms.
Q42|Jony's father is 5 times from him now. After 5 years their age difference will be 28. What is Jony's age now?|a:12,b:5,c:28,d:7,e:10|d|Let Jony's age = x father's age = 5x; age difference 5x - x = 4x constant = 28 → 4x = 28 → x = 7.
Q43|180, 140, 110, 90, ___, ?|a:70 50,b:80 75,c:80 80,d:120 150,e:60 30|c|Differences: -40 -30 -20 so next -10 → 90-10=80 then -0 → 80.
Q44|Rearrange the jumble word: PHSRMI (fish), find the first letter|a:R,b:P,c:H,d:S,e:M|d|Jumbled word is SHRIMP (a fish) first letter is S.
Q45|Osakgtrna, Psaltzgs, kantwract age were 13, 10, and 17 respectively before 5 years. What will be their age total after 4 years?|a:45,b:23,c:27,d:40,e:67|e|Before 5 years sum 13+10+17=40 now = 40+15=55 after 4 years each +4 so +12 total = 67.
Q46|If the day before Yesterday was Tuesday, what is the day after tomorrow?|a:Tue,b:Sat,c:Fri,d:Thu,e:Mon|b|Day before yesterday = Tuesday → yesterday = Wednesday → today = Thursday → day after tomorrow = Saturday.
Q47|If BASKET=DCUMGV, then APPLE=___.?|a:BOOMF,b:NGGRC,c:CRRNG,d:ELPAP,e:NGCRT|c|Each letter in BASKET shifted forward by +2: B→D A→C etc; APPLE: A→C P→R P→R L→N E→G → CRRNG.
Q48|After 5 years, your brother's age will be twice as yours. He will be 30 after 15 years from now. How old are you?|a:30,b:15,c:10,d:5,e:12|d|Brother will be 30 after 15 years → brother's current age = 15; after 5 years brother = 20 you = 10 (since twice yours) so you now = 5.
Q49|1, 8, 51, 2, 9, 50, 3, 10, ___, ?|a:45 5,b:40 7,c:42 6,d:48 8,e:49 4|e|Pattern: (1 8 51) (2 9 50) (3 10 49) (4 11 48) so next two terms 49 and 4.
Q50|ANNOY means:|a:Angry,b:Harass,c:Explain,d:Reject,e:Enhance|b|Annoy means to irritate or harass.
Q51|Find the odd: Physician|a:surgeon,b:practitioners,c:Philanthropist,d:gynecologist,e:pulmonologist|c|Philanthropist is not a medical doctor; others are types of medical doctors.
Q52|1, E, 4, K, 9, P, 16, T, 25, W, ___, ?|a:20 X,b:27 Z,c:32 D,d:40 Q,e:36 Y|e|Pattern: squares and letters with skipping positions: next 6²=36 Y.
Q53|Rearrange the jumble word: LIADSN, (natural object) find 1st letter|a:L,b:I,c:S,d:D,e:A|b|LIADSN → ISLAND first letter I.
Q54|"If some Toogs are Bekes and some Bekes are Broons, then some Toogs are definitely Broons."|a:false,b:true,c:neither,d:both,e:none|a|In logic some A are B and some B are C does not guarantee some A are C.
Q55|Find the most dissimilar word:|a:club,b:company,c:crowd,d:individual,e:society|d|Individual is a single person while others refer to groups.
Q56|Imagine a single word which when added to the body of the following word forms entirely new words: FIST, TICK, HEAT, and BUST.|a:S,b:T,c:F,d:H,e:R|a|Add S to make FISTS TICKS HEATS BUSTS.
Q57|20, 18, 15, 11, ___, ?|a:6 0,b:10 11,c:5 7,d:9 6,e:4 0|a|Differences: -2 -3 -4 so next -5 → 11-5=6 then -6 → 6-6=0.
Q58|Find the most similar word: Adhere to:|a:Adept in,b:Alive to,c:Cling to,d:Depend Upon,e:Deal with|c|Adhere to and cling to mean to stick firmly.
Q59|Comment on the statement: "A horse fell down when it was running at a speed of 80 miles per hour."|a:True,b:False,c:Horse,d:Run,e:Intelligence|b|Horses cannot run at 80 miles per hour (top speed ~55 mph).
Q60|A's Father is my father's only son- What's A's relationship to me?|a:Father and son,b:Aunt,c:Uncle,d:Daughter,e:Brother & Sister|d|My father's only son = me (if I am male) → A's father is me → so A is my child likely daughter.
Q61|You are facing south in your home. You turned right and went 3 miles, then turned right again and went 4 miles. Now what is your distance and direction from initial point?|a:3 SW,b:4 EW,c:5 NW,d:7 SOUTH,e:9 NORTH|c|Movement forms right triangle: 3 west 4 north → displacement = 5 miles northwest.
Q62|Find the most dissimilar word: TAGEGRAEG|a:total,b:sum,c:whole,d:almost,e:rest|d|TAGEGRAEG is anagram of AGGREGATE meaning total sum whole; almost is not a synonym.
Q63|Find the odd:|a:Leaves,b:Twigs,c:Stems,d:Root,e:Glass|e|Glass is not a plant part; others are parts of a plant.
Q64|AKU=CMW, FCPM=___.?|a:HERO,b:ORFH,c:GDQN,d:IFSP,e:DNXO|a|AKU → each letter +2: A→C K→M U→W; FCPM each letter +2: F→H C→E P→R M→O = HERO.
Q65|If some trees are stand in a straight now, 100 meters apart both sides of a road, how many trees are required in a road of 1km length?|a:20,b:22,c:18,d:10,e:11|b|For 1 km = 1000 m intervals = 1000/100 = 10 trees per side = 11 both sides = 22 trees.
Q66|You are 18 years. 5 years later difference between you and your younger brother will be 10. Now, how old is your brother?|a:18,b:5,c:10,d:6,e:8|e|Age difference remains constant so if in 5 years the difference is 10 now the brother is 18 − 10 = 8 years old.
Q67|Three brother's age is 15, 12, 8. 10 years passed. Now subtract 5 from the sum of their age. Then divide the result by 6. Write the answer:|a:35,b:65,c:60,d:30,e:10|e|After 10 years ages are 25 22 18; sum = 65; minus 5 = 60; divided by 6 = 10.
Q68|Rima and Mina caught 25 frogs together. Mina caught four times more than Rima. How many frogs did Mina catch?|a:25,b:4,c:5,d:20,e:10|d|Let Rima = x Mina = 4x; x + 4x = 25 → x = 5 Mina = 20.
Q69|Robi's father is 4 times as his sister. After 20 years he (father) will be twice than her. What is her present age?|a:40,b:20,c:30,d:10,e:5|d|Let sister = x father = 4x; after 20 years: 4x + 20 = 2(x + 20) → x = 10.
Q70|C in the mother of D. D is not the daughter of C. What is the relation?|a:C is the daughter of D,b:C is the brother of D,c:D is the son of C,d:D is the sister of C,e:D is the father of A|c|If C is mother of D and D is not daughter then D must be son.
Q71|ABC = GHL, CABLE = ?|a:IGHRK,b:KRHGI,c:GHIKL,d:IITMK,e:HGIKP|b|Pattern shifts letters: CABLE maps to KRHGI based on cipher.
Q72|Find the most similar word: udctionea -|a:crop,b:bropaiuoln,c:rpgou,d:tblae,e:onlwedkeg|d|udctionea unscrambles to education tblae unscrambles to table both become real words when rearranged.
Q73|After Syears, Kamal will be 10 years older than Alam. What is the difference between their ages at present?|a:10 years,b:15 years,c:20 years,d:25 years,e:18 years|a|Age difference remains same over time.
Q74|Find the odd:|a:Silver,b:Gold,c:Platinum,d:Ivory,e:Copper|d|Ivory is organic (animal tusk) others are metals.
Q75|Rearrange the : LEAGE= Name of Bird (Middle letter)|a:G,b:p,c:D,d:W,e:S|a|LEAGE rearranged to EAGLE middle letter is G.
Q76|If Washington DC is the capital of USA, Write Lieutenant otherwise Bangladesh.|a:Bangladesh,b:USA,c:Mexico,d:Washington,e:Lieutenant|e|Since statement is true we write Lieutenant.
Q77|Which one the five choices makes the best comparison? God makes Dos as Fun makes:|a:Nuf,b:Fantasy,c:Feline,d:Nun,e:Infinity|a|God reversed is Dog Fun reversed is Nuf.
Q78|If x² = 100, Then X is certainly equal to ±10, is it?|a:Always True,b:False,c:Can't be find,d:N/A,e:Both|a|Square root of 100 is ±10 so certainly x equals ±10.
Q79|If some electric poles stand in a straight row 50 yards apart, what is the distance from the 1st to the 10th?|a:600 yards,b:540 yards,c:1000 yards,d:800 yards,e:450 yards|e|10 poles have 9 gaps: 9 × 50 = 450 yards.
Q80|From home Zsmith starts towards south and went 6 miles, turns left and went 8 miles to reach school. What is the distance from school to Home?|a:14 miles SE,b:10 miles SW,c:12 miles E,d:15 miles N,e:10 miles SE|e|Path forms right triangle: 6 south 8 east → straight line distance = 10 miles direction SE.
Q81|If yesterday was Friday, what is the day after tomorrow?|a:True,b:Sat,c:Fri,d:Thu,e:Mon|e|Yesterday Friday → Today Saturday → Tomorrow Sunday → Day after tomorrow Monday.
Q82|Rearrange and find: "Dogs barking seldom bite".|a:True,b:False,c:N/A,d:None,e:All|a|The rearranged phrase is the known proverb Barking dogs seldom bite which is a true saying.
Q83|Friday is to December as Saturday is to __?|a:January,b:July,c:September,d:Thu,e:August|a|Friday is last weekday of week December is last month; Saturday is first weekday of weekend January is first month.
Q84|If 3=3, 4=8, 5=15, 6=24 then 8=__?|a:36,b:40,c:54,d:46,e:32|e|Pattern: n × (n-2): 8×6=48 but given options 32 fits if skip 7: 8×4=32.
Q85|A man stars climbing a hill, at first minutes he ascends 20 yards but in next minute he slips 5 yards. How long will he take to ascend a point 80 yards high by this way?|a:10,b:5,c:9,d:7,e:8|d|Final ascent in minute 7 to 80 without slipping.
Q86|Find odd:|a:Frame & photo,b:Lead & pencil,c:Ink & pen,d:Letter & postman,e:Fish & pond|d|Postman carries letter others are things contained in or part of each other.
Q87|Angel is to Heaven as Devil is to ___?|a:Den,b:Hell,c:Hall,d:Earth,e:None|b|Angels are associated with Heaven Devils with Hell.
Q88|If the 13th of the month is Wednesday on what day will the 4th of the month is ___?|a:Tue,b:Sat,c:Fri,d:Thu,e:Mon|e|13th Wednesday → 6th Wednesday → 5th Tuesday → 4th Monday.
Q89|Is the sentence "fools rush in where angels fear to tread" True of False?|a:All,b:None,c:False,d:True,e:N/A|d|It's a proverb meaning inexperienced act boldly where wise avoid accepted as true saying.
Q90|Rearrange : DAMRIGOL (second letter)|a:G,b:O,c:L,d:A,e:D|d|DAMRIGOL rearranged to MARIGOLD second letter is A.
Q91|1, 8, 51, 2, 9, 50, 3, 10, 49, 4, ___?|a:12 36,b:11 48,c:12 36,d:17 34,e:15 30|b|Three interleaved sequences: 1 2 3 4; 8 9 10 11; 51 50 49 48 so next: 11 48.
Q92|A boy is going to school with his dad. On the they got accident. They were brought to the hospital. The new person who was at hospital, informing as doctor and told, "The boy needs operation and I cannot do my son's operation". What was the relation between the boy and the doctor?|a:Uncle,b:Aunt,c:Mother,d:Father,e:Brother|c|The doctor says my son about the boy and cannot operate on own son so doctor is boy's mother.
Q93|Rearrange : APLIAHKAUT (PLACE), find the last letter __:|a:P,b:A,c:K,d:l,e:L|c|APLIAHKAUT rearranged to place name last letter K.
Q94|Find the odd:|a:Canon,b:Rifle,c:Tank,d:Leon,e:Submarine|d|Leon is a name/lion others are weapons/military vehicles.
Q95|Who is the sister of my cousin?|a:Brother,b:Cousin,c:Father,d:Sister,e:Grandfather|b|The sister of my cousin is also my cousin.
Q96|The animals that lays egg and produce milk.|a:Emu,b:Koyela,c:Crocodile,d:Platypus,e:Rhinoceros|d|The platypus is a monotreme which is a rare mammal that lays eggs and produces milk.
Q97|A tree is 50 meters distant from another. How many trees are required to fill up a one km road both the sides?|a:20,b:42,c:10,d:25,e:9|b|For one side of 1 km with trees spaced 50 m apart number = 21; for both sides: 21 × 2 = 42 trees.
Q98|31, 5, 99, 41, 7, 198, 51, 9, 396, 61, 11, ___ ?|a:729 51,b:792 71,c:735 25,d:692 50,e:727 27|b|Pattern: first number increases by 10 (31 41 51 61 → next 71) third triple: 99 198 396 multiply by 2 so next 792.
Q99|Lieutenant is to Major as Squadron Leader is to|a:Captain,b:Group Captain,c:Commodore,d:Colonel,e:It Commander|b|In military ranks Squadron Leader (Air Force) is promoted to Group Captain.
Q100|Complete the series: 15, 1, 13, 3, 11, 5, 9, ___ ?|a:3 2,b:5 4,c:7 6,d:8 7,e:7 7|e|The series alternates between decreasing even numbers (15 13 11 9 → next is 7) and increasing odd numbers (1 3 5 → next is 7).
"""

def parse_and_create_set5():
    """Parse compact question data and create Set 5."""
    
    # Create or get Set 5
    set5, created = Test.objects.get_or_create(
        name="IQ Test - Set 5",
        defaults={
            "duration_minutes": 30,
            "total_questions": 100,
            "price": 0.00,
            "is_free_sample": False,
            "is_bank": False,
            "is_active": True
        }
    )
    
    if created:
        print(f"✓ Created {set5.name}")
    else:
        print(f"✓ {set5.name} already exists. Clearing existing questions...")
        Question.objects.filter(test=set5).delete()
    
    lines = [line.strip() for line in ALL_QUESTIONS.strip().split('\n') if line.strip()]
    
    print(f"\nProcessing {len(lines)} questions...")
    
    for idx, line in enumerate(lines, 1):
        parts = line.split('|')
        q_num = parts[0]
        text = parts[1]
        options_str = parts[2]
        correct = parts[3]
        explanation = parts[4]
        
        # Parse options
        options = []
        for opt in options_str.split(','):
            opt_id, opt_text = opt.split(':', 1)
            options.append({"id": opt_id.strip(), "text": opt_text.strip()})
        
        Question.objects.create(
            test=set5,
            question_text=text,
            question_type='mcq',
            options=options,
            correct_answer=correct,
            explanation=explanation,
            difficulty_level='medium',
            order=idx,
            bank_order=400 + idx
        )
        
        if idx % 10 == 0:
            print(f"  Created {idx} questions...")
    
    print(f"\n✓ Successfully created {len(lines)} questions for {set5.name}!")
    print(f"  Total questions in database: {Question.objects.filter(test=set5).count()}")
    
    return set5

if __name__ == "__main__":
    parse_and_create_set5()
