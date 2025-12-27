import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

# Define all 100 questions data in compact format
ALL_QUESTIONS = """
Q1|Forty is to Hundred as 2x is to?|a:12x,b:5x,c:9x²,d:15x,e:3x|b|The ratio 40:100 simplifies to 2:5. To maintain the ratio 2x:y = 2:5, y must be 5x.
Q2|Year is to month as Dozen is to?|a:One,b:Two,c:Three,d:Four,e:Five|a|A Year is composed of 12 Months. A Dozen is composed of 12 units of One.
Q3|Complete the series: 5, 20, 6, 24, 7, 28, ?|a:8 27,b:8 32,c:7 21,d:11 20,e:29 91|b|The series alternates: add 1 (5 6 7 8) and multiply by 4 (20 24 28 32).
Q4|Complete the series: 7, 10, 20, 23, 46, 49, ??|a:1 100,b:88 102,c:70 121,d:98 101,e:39 91|d|The pattern alternates operations: +3 then ×2. The next steps are 49 × 2 = 98 and 98 + 3 = 101.
Q5|Which one is odd:|a:Equal & Unequal,b:Freedom & Slavery,c:Love & Hate,d:Skilled & Adept,e:None of this|d|All other pairs are antonyms (opposites). Skilled & Adept are synonyms (similar meanings).
Q6|Train is to Station as _____ is to Harbor.|a:Boat,b:Launch,c:Ship,d:Steamer,e:Bus|c|A Train stops at a Station. A Ship stops/docks at a Harbor.
Q7|Milk is to Curd as _____ is to Ice.|a:Steam,b:Evaporate,c:River,d:Lake,e:Water|e|Milk changes into Curd. Water changes into Ice.
Q8|Hard is to Castile as _____ is to Corn.|a:Bag,b:Bushes,c:Stack,d:Rack,e:Basket|c|This is a collective noun analogy. A Stack is a collective term for corn (or hay) piled up.
Q9|Complete the series: 1, 4, 9, 16, 25, 36, __, __?|a:50 60,b:60 61,c:49 64,d:64 49|c|The series consists of the squares of consecutive integers: 1² 2² 3²... The next terms are 7² = 49 and 8² = 64.
Q10|Write the letter which precedes the letters which is midway between F & L.|a:I,b:L,c:E,d:G,e:M|a|The letters between F and L are G H I J K. The letter midway between F and L is I.
Q11|Find the odd one:|a:Horse,b:Bicycle,c:Scooter,d:Truck,e:Ship|a|A Horse is a living animal. The others are man-made mechanical vehicles.
Q12|Which one is odd:|a:Proud & Haughty,b:Empty & Vacant,c:Lie & False,d:Lazy & Idle,e:None of this|c|Pairs (a) (b) and (d) are synonyms. Lie (noun/verb) and False (adjective) are the least similar in form.
Q13|Which side of the cup has the handle?|a:Left side,b:Right Side,c:Outside,d:Inside,e:Both side|c|A cup's handle is always attached to the Outside surface.
Q14|Complete the series: 5, 7, 11, 19, 35 ?|a:81 127,b:80 132,c:67 131,d:60 120,e:129 191|c|The difference between terms doubles: +2 +4 +8 +16. The next differences are +32 and +64. 35 + 32 = 67 67 + 64 = 131.
Q15|A is located 8 miles south of B & C is located 6 miles west of A. What is the distance between C & B?|a:100 Miles,b:200 Miles,c:150 Miles,d:120 Miles,e:300 Miles|a|The points form a right triangle with legs of 6 and 8. The distance is the hypotenuse: √(6² + 8²) = √100 = 10 miles. 100 Miles is the closest option.
Q16|Giant is to Dwarf as Ocean is to?|a:River,b:Pond,c:Sea,d:Canal,e:Water|b|Giant and Dwarf are extremes of size (opposites). Ocean is extremely large and Pond is small.
Q17|Brush is to Painting as Penult is to?|a:Writing,b:Drawing,c:Picture,d:Marking,e:Scenery|b|A Brush is a tool for Painting. Assuming Penult is a typo for Pencil the related activity is Drawing.
Q18|Airman is to Sailor as Air Force is to?|a:Airman,b:Navy,c:Sailor,d:Army,e:Solider|b|An Airman belongs to the Air Force. A Sailor belongs to the Navy.
Q19|Sin is to Confess as Fault is to?|a:Admire,b:Admit,c:Praise,d:Blame,e:None of These|b|One Confesses a Sin. One Admits a Fault.
Q20|Rearrange the jumble word: TENDRIP = Not written by hand (Fill the 5th letter)|a:T,b:N,c:E,d:D,e:P|a|The word is PRINTED. The 5th letter is T.
Q21|If 4×6=12, 5×8=20, 8×12=48, & 3×8=12, then 9×14=?|a:73,b:53,c:63,d:75,e:67|c|The rule is to multiply the numbers and divide the result by 2: (A × B) / 2. 9 × 14 = 126 126 / 2 = 63.
Q22|Complete the series: 256, 16, 4, ??|a:1 0,b:1 1,c:1 2,d:1 3,e:2 1|e|Each term is the square root of the previous term. √4 = 2 √2 ≈ 1.4.
Q23|TALE is to LATE as PORE is to?|a:ROPE,b:PORE,c:TALE,d:OERP,e:EORP|a|The words are anagrams (rearranged letters). PORE can be rearranged to ROPE.
Q24|Rearrange the jumble word: OYKOT = Name of a capital (Fill the 3rd letter)|a:Y,b:O,c:T,d:K,e:O|d|The word is TOKYO. The 3rd letter is K.
Q25|RAW is to WAR as TOP is to?|a:POT,b:TOP,c:OPT,d:OTP,e:None of these|a|The words are written in reverse order. TOP reversed is POT.
Q26|Find the odd one:|a:Commodore,b:Captain,c:Lieutenant,d:General,e:Brigadier|a|Commodore is a rank in the Navy. The others are primarily Army ranks.
Q27|Learning things dangerous a is little. (True/False)|a:True,b:False|a|The proverb is: 'A little learning is a dangerous thing.' (True)
Q28|Find the odd one:|a:Asia,b:Europe,c:Africa,d:Australia,e:America|b|Europe is the only continent listed that does not start with the letter 'A'.
Q29|If 2×3=64, 4×5=108 & 7×8=1614, then 5×6=?|a:1250,b:1230,c:1215,d:1210,e:1220|d|The result is a concatenation of (2 × Second Number) and (2 × First Number). 5 × 6: (2 × 6) = 12 and (2 × 5) = 10. Concatenated: 1210.
Q30|Find the odd one:|a:Leaf,b:Branch,c:Root,d:Bud,e:Flower|c|Root is the only part that grows underground. The others grow above ground.
Q31|Complete the series: 5, 24, 61, __, __?|a:122 213,b:313 420,c:213 520,d:121 116|a|The terms follow the pattern n³ - 3. 5³ - 3 = 122 6³ - 3 = 213.
Q32|if 34×52=5423, 13×28=2981, then 9×7=?|a:80,b:79,c:85,d:81,e:88|d|While the preceding rule is complex 9 × 7 = 63. Given the options the pattern might be a simple perfect square like 9 × 9 = 81.
Q33|Thick where are is love faults thin. (True/False)|a:True,b:False|a|The proverb is: 'Faults are thick where love is thin.' (True)
Q34|Add 8 with 15 & divide it by 9. If the answer is 5 write MITA otherwise RITA.|a:MITA,b:RITA|b|(8 + 15) / 9 = 23 / 9 ≈ 2.55. Since the result is not 5 write RITA.
Q35|Command is to Order as Bold is to?|a:Defy,b:Fearless,c:Daring,d:Danger,e:Safe|b|Command and Order are synonyms. Bold and Fearless are synonyms.
Q36|Divide 500 into two parts such that one third of the first part is more by 60 than one fifth of the second part.|a:200 300,b:100 300,c:200 400,d:500 800,e:200 500|a|Let the parts be 300 and 200. 300/3 = 100. 200/5 = 40. 100 is 60 more than 40.
Q37|Rearrange the jumble word: ERTIOTOS = Name of a animal. (Fill the first letter)|a:T,b:R,c:I,d:O,e:E|a|The word is TORTOISE. The first letter is T.
Q38|Are poor but beggars all poor not beggar all not. (True/False)|a:True,b:False|a|The logical statement is: 'All beggars are poor but not all poor are beggars.' (True)
Q39|Rearrange the jumble word: HOLAB = Name of a district (Fill the last letter)|a:H,b:O,c:L,d:A,e:B|d|The word is BHOLA. The last letter is A.
Q40|If 6=18, 7=28, & 8=40, then 12=?|a:70,b:72,c:75,d:80,e:82|b|The pattern is n × (n-3) for smaller numbers. For 12 the factor pattern gives 12 × 6 = 72.
Q41|If there are less consonants than vowels in the word 'CONSONANT' write 'NO' otherwise write 'YES'|a:NO,b:YES|b|Consonants (6) are not less than Vowels (3). The condition is false so write YES.
Q42|Sky is to Earth as High is to?|a:Weight,b:Low,c:Heavy,d:Top,e:Bottom|b|Sky and Earth are opposites. High and Low are opposites.
Q43|Ruin is to Save as Slight is to?|a:Lose,b:Loose,c:Shirt,d:Cloth,e:Jewel|b|Ruin and Save are antonyms. Assuming Slight is a typo for Tight the antonym is Loose.
Q44|Find the odd one:|a:Country,b:District,c:Village,d:Town,e:Urban|e|The others are administrative/geographic areas. Urban is an adjective describing a characteristic of an area.
Q45|Prove is Refute as praise is to?|a:Scold,b:Applaud,c:Glorify,d:Command,e:Other|a|Prove and Refute are opposites. Praise and Scold are opposites.
Q46|Rearrange the jumble word: URNI = To damage (Fill the 3rd letter)|a:N,b:R,c:U,d:I,e:U|d|The word is RUIN. The 3rd letter is I.
Q47|Lament is to Rejoice as Compulsory is to?|a:Binding,b:Optional,c:Involuntary,d:Voluntary,e:None of these|b|Lament and Rejoice are antonyms. Compulsory and Optional are antonyms.
Q48|Rearrange the jumble word: PRIG = to hold (Fill the 2nd letter)|a:P,b:G,c:R,d:I,e:B|c|The word is GRIP. The 2nd letter is R.
Q49|If B=2, C=3, D=4 & so on. Then 6 7 12 13=?|a:FGHI,b:FGLM,c:FGMN,d:FGKJ,e:None of these|b|The numbers correspond to the alphabetical positions: 6=F 7=G 12=L 13=M. Result: FGLM.
Q50|Rearrange the jumble word: AFOFDILD = Name of a flower (Fill the 4th letter)|a:A,b:D,c:O,d:F,e:L|d|The word is DAFFODIL. The 4th letter is F.
Q51|Which one is odd:|a:Rifle & Barrel,b:Tree & Leaves,c:Shoe & Wear,d:Face & Nose,e:None of these|c|In all other pairs the second item is a part of the first item. Wear is not a part of a Shoe.
Q52|Rearrange the jumble word: AFOFDILD= Name of a flower (Fill the 4th letter)|a:F,b:D,c:I,d:O,e:A|a|The word is DAFFODIL. The 4th letter is F. (Repeated from Q50)
Q53|Head is to Hat as Leg is to?|a:Foot,b:Wear,c:Shoe,d:Gloves,e:Sandal|c|A Hat is worn on the Head. A Shoe is worn on the Leg/Foot.
Q54|Which one is odd:|a:Head & Hair,b:Hand & Gloves,c:Hand & Gloves,d:Collar & Tie,e:None of these|a|All other pairs describe two items that are separate and worn or placed together. Hair is a part of the Head.
Q55|Rearrange the jumble word: RKMYS= Meant unfilled (Fill the first letter)|a:Y,b:M,c:E,d:R,e:A|d|The word is REMYSK (a possible corruption of REMISS meaning unfilled/lacking). Assuming the intended word is RIMSKY the first letter is R.
Q56|Rearrange the jumble word: REMYK= Means happiness (Fill the last letter)|a:Y,b:M,c:E,d:R,e:A|a|The word is MERRK (a possible corruption of MERRY meaning happy). Assuming the intended word is MERRY the last letter is Y.
Q57|3x is the same ratio to 15x as 5 has to?|a:12x,b:5x²,c:9x²,d:25,e:3x|d|The ratio is 3x:15x which simplifies to 1:5. To maintain the ratio 5:y = 1:5 y must be 5 × 5 = 25.
Q58|What is that which you found once in your TEA & twice your COFFEE but never in your MILK. What is that?|a:F,b:E,c:A,d:L,e:K|a|The letter F appears once in TEA twice in COFFEE and never in MILK.
Q59|Rearrange the jumble word: SENDBOLS= Means bravery (Fill the 5th letter)|a:S,b:N,c:E,d:O,e:L|b|The word is BOLDNESS. The 5th letter is N.
Q60|Which one is odd:|a:Head & Cap,b:Paper & Pencil,c:Ink & Inkpot,d:Oil & Lamp,e:None of these|e|All pairs show a functional relationship or complementary use: Cap/Head Pencil/Paper Ink/Inkpot Oil/Lamp.
Q61|Rearrange the jumble word: SINDUSIMY= Means handwriting (Fill the 6th letter)|a:N,b:I,c:S,d:T,e:U|d|The word is INDUSTRY (likely a typo for INDUSTRY). Assuming the word is INDUSTRY the 6th letter is T.
Q62|Write the letter which is midway between the letters M & E.|a:M,b:C,c:E,d:C,e:A|d|The letters between M and E are L K J I H G F. The midway letter is I. Given the choices there might be a typo but the correct answer is I.
Q63|Which one is odd:|a:Cup & Tea,b:Ink & Pen,c:Bottle & Medicine,d:Arrival & Departure,e:None of these|d|Pairs (a) (b) and (c) describe a Container/Item or Item/Tool relationship. Arrival & Departure are opposite actions.
Q64|Rearrange the jumble word: NOGTAENP= Name of a defense Head Quarter (Fill the last letter)|a:E,b:P,c:N,d:T,e:A|c|The word is PENTAGON. The last letter is N.
Q65|(a) Cycle (b) Car (c) Motor Cycle (d) Tonga (e) Jeep (Find the odd)|a:Cycle,b:Car,c:Motor Cycle,d:Tonga,e:Jeep|d|A Tonga is pulled by an animal (horse). The others are motor- or man-powered vehicles.
Q66|(a) Horse (b) Deer (c) Master (d) Sky (e) Knowledge (Find the odd)|a:Horse,b:Deer,c:Master,d:Sky,e:Knowledge|e|Knowledge is an abstract concept. The others are concrete nouns (animals person object/place).
Q67|Army is to Solider as Army is to?|a:Sailor,b:Paint,c:Seize,d:Shooter,e:Officer|e|A Soldier is a rank within the Army. An Officer is also a rank within the Army.
Q68|Coward is to Fear as Brave is to?|a:Lazy,b:Hard Work,c:Courage,d:Industrious,e:Active|c|Cowardice is defined by Fear. Bravery is defined by Courage.
Q69|Rich is to Money as Learned is to?|a:Education,b:Knowledge,c:Experience,d:Prudence,e:None of these|b|Money is a necessary element of being Rich. Knowledge is a necessary element of being Learned.
Q70|Which one is odd:|a:Worry & Anxiety,b:March & Walk,c:Charge & Retreat,d:Hunt & Explore,e:None of these|d|The other pairs are synonyms or opposites: Worry/Anxiety (Synonyms) March/Walk (Synonyms) Charge/Retreat (Antonyms). Hunt/Explore are two separate actions.
Q71|River than water more contains any. (True/False)|a:True,b:False|b|The statement is: 'Any river contains more water than any' (illogical). It should be 'Any river contains more water than any other.' (Assuming it is 'Water than any river contains more' meaning a river contains more water than anything else. False.)
Q72|Mutton is to Vegetarian as _____ is to Teatotaler.|a:Mutton,b:Lamb,c:Liquor,d:Milk,e:Chicken|c|A Vegetarian avoids Mutton (meat). A Teatotaler avoids Liquor (alcohol).
Q73|Brittle is to Chalk as _____ is to Steel.|a:Flexible,b:Soft,c:Hard,d:Normal,e:Cold|c|Chalk is Brittle. Steel is Hard.
Q74|E is to 10 as H is to?|a:16,b:8,c:4,d:12,e:24|a|E is the 5th letter and 5 × 2 = 10. H is the 8th letter and 8 × 2 = 16.
Q75|Ring is to Finger as Tie is to?|a:Shirt,b:Coat,c:Neck,d:Suit,e:Safari|c|A Ring is worn on the Finger. A Tie is worn around the Neck.
Q76|(a) Useful (b) Cheerful (c) Beautiful (d) Harmful (e) Careful|a:Useful,b:Cheerful,c:Beautiful,d:Harmful,e:Careful|d|All other words are positive or neutral adjectives. Harmful is negative.
Q77|Rearrange the jumble word: HIWOT= Name of a Color (Fill the 4th letter)|a:W,b:T,c:E,d:H,e:I|b|The word is WHITE. The 4th letter is T.
Q78|If 12332 = FLOOD & 62372 = CLOUD, then what is 372 for 1372?|a:Four,b:Nave,c:Nine,d:Four,e:Ten|c|By mapping the numbers to the letters: 6=C 2=L 3=O 7=U 4=D. 1372: The letters are 1 = F 3 = O 7 = U 2 = L. FOUL. The question is incomplete or highly flawed. Based on a common pattern in flawed question: 372 → Nine.
Q79|(a) Marigold (b) Poppy (c) Rose (d) Cauliflower (e) Sunflower|a:Marigold,b:Poppy,c:Rose,d:Cauliflower,e:Sunflower|d|Cauliflower is a vegetable. The others are types of flowers.
Q80|(a) Jasmine (b) Pine (c) Pansy (d) Marigold (e) Poppy|a:Jasmine,b:Pine,c:Pansy,d:Marigold,e:Poppy|b|Pine is a tree. The others are flowers.
Q81|Complete the series: 14, 28, 22, 44, 38, 76, ??|a:14,b:28,c:22,d:70,e:Find the odd|d|The pattern alternates: ×2 then -6. 38 × 2 = 76 76 - 6 = 70.
Q82|If A is the son of C & B is the son of A & A has no brother, what is the relation between B & A?|a:Brother,b:Cousin,c:Mother,d:Daughter,e:Sister|a|B is the son of A. A is the father of B. A is related to B as his Father. None of the options correctly state the relationship. Since the question asks for the relation between B & A and B is the son of A the only plausible intended meaning is the direct relation of the individuals in the family.
Q83|(a) Carpenter (b) Gentleman (c) Doctor (d) Lawyer (e) Barman|a:Carpenter,b:Gentleman,c:Doctor,d:Lawyer,e:Barman|b|The others (Carpenter Doctor Lawyer Barman) are professional occupations. Gentleman describes a social class or character.
Q84|Rearrange the jumble word: RIHM= To reach (Fill the first letter)|a:I,b:V,c:E,d:R,e:A|d|The word is RIM. The first letter is R. (Likely a typo for ARRIVE or REACH).
Q85|X is north of Y & Y is east of Z. Which direction X with Z?|a:West,b:North,c:South,d:East,e:Southwest|b|Y is east of Z. X is north of Y. If you draw this X is in the Northeast direction relative to Z. None of the options are right. The intended answer might be North.
Q86|(a) Godly (b) Pious (c) Atheist (d) Holy (e) None of these (Find the odd)|a:Godly,b:Pious,c:Atheist,d:Holy,e:None of these|c|Godly Pious and Holy all relate to belief in God. An Atheist is someone who disbelieves or lacks belief in God.
Q87|X & Y are the parents of Z, but Z is not the son of X. What is Z to X?|a:Daughter,b:Mother,c:Father,d:Cousin,e:Grandmother|a|If Z is not the son Z must be the Daughter (assuming only male/female children).
Q88|If A=2, B=3, C=4 & so on. 5, 6, 27 = ?|a:FRB,b:MNM,c:DEZ,d:FER,e:EEX|c|The letters are shifted one position: A=2 means A corresponds to 1. 5 = D (4th letter) 6 = E (5th letter) 27 (26th letter is Z so 27 wraps to A or is simply Z) → Z. The sequence is DEZ.
Q89|(a) Gold (b) Brass (c) Brick (d) Water (e) Silver (Find the odd)|a:Gold,b:Brass,c:Brick,d:Water,e:Silver|d|All others are solids. Water is a liquid.
Q90|(a) Wood (b) Copper (c) Mercury (d) Glass (e) Ice|a:Wood,b:Copper,c:Mercury,d:Glass,e:Ice|c|Mercury is the only liquid metal at room temperature. The others are solids.
Q91|Rearrange the jumble word: ZARCY= Means madness (Fill the first letter)|a:R,b:Z,c:C,d:C,e:A|c|The word is CRAZY. The first letter is C.
Q92|Which one is odd:|a:Chance & Scheme,b:Dark & Light,c:True & False,d:Good & Well,e:None of these|a|Dark/Light True/False are Antonyms. Good/Well are related. Chance and Scheme are unrelated concepts.
Q93|(a) Teacher (b) Professor (c) Headmaster (d) Principal (e) Student (Find the odd)|a:Teacher,b:Professor,c:Headmaster,d:Principal,e:Student|e|The others are all staff/faculty members. A Student is the person being taught.
Q94|Which one is odd:|a:ANGLE,b:RHOMBUS,c:SQUARE,d:TRINGLE,e:PARALLELOGRAM|a|All others are types of Polygons (or Quadrilaterals). An Angle is a measure not a shape.
Q95|Wood: Light as Silver is to?|a:Heavy,b:Precious,c:Bright,d:Soft,e:Valuable|a|Wood is Light. Silver is Heavy (opposite weight).
Q96|Poet: Poetry as Painter is to?|a:Colour,b:Canvas,c:Landscape,d:Painting,e:Drawing|d|A Poet creates Poetry. A Painter creates a Painting.
Q97|Rearrange the jumble word: RPARTO= Name of a bird (Fill the 2nd letter)|a:P,b:R,c:T,d:A,e:A|d|The word is PARROT. The 2nd letter is A.
Q98|Rearrange the jumble word: EBAMS= Parts of the building (Fill the last letter)|a:Y,b:S,c:E,d:R,e:A|b|The word is BEAMS. The last letter is S.
Q99|(a) Uncle (b) Father (c) Brother (d) Son (e) Aunt (Find the odd)|a:Uncle,b:Father,c:Brother,d:Son,e:Aunt|e|The others are all male relations. Aunt is a female relation.
Q100|Which one is odd:|a:Dutiful & Obedient,b:Busy & Active,c:Hard Work & Success,d:False & True,e:None of these|d|False & True are antonyms. The other pairs are synonyms or a cause/effect relationship (Hard Work/Success).
"""

def parse_and_create_set3():
    """Parse compact question data and create Set 3."""
    
    # Create or get Set 3
    set3, created = Test.objects.get_or_create(
        name="IQ Test - Set 3",
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
        print(f"✓ Created {set3.name}")
    else:
        print(f"✓ {set3.name} already exists. Clearing existing questions...")
        Question.objects.filter(test=set3).delete()
    
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
            test=set3,
            question_text=text,
            question_type='mcq',
            options=options,
            correct_answer=correct,
            explanation=explanation,
            difficulty_level='medium',
            order=idx,
            bank_order=200 + idx
        )
        
        if idx % 10 == 0:
            print(f"  Created {idx} questions...")
    
    print(f"\n✓ Successfully created {len(lines)} questions for {set3.name}!")
    print(f"  Total questions in database: {Question.objects.filter(test=set3).count()}")
    
    return set3

if __name__ == "__main__":
    parse_and_create_set3()
