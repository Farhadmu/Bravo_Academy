import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

# All 100 Set 7 questions in compact format
ALL_QUESTIONS = """
Q1|TRANSLATOR is to translate then florist is to __?|a:build,b:decorate,c:architect,d:play,e:design|b|A translator translates just as a florist decorates with flowers.
Q2|Cheap is to Expensive, then Cruel is to ___?|a:Humane,b:High,c:Light,d:Long,e:Shallow|a|Cruel is the opposite of humane just as cheap is the opposite of expensive.
Q3|Complete the series: 22, 33, 23, 34, 24, __?|a:34 23,b:37 26,c:35 25,d:40 28,e:46 35|c|Pattern alternates: 22→33 (+11) 33→23 (-10) 23→34 (+11) 34→24 (-10) so next: 24+11=35 35-10=25.
Q4|The sentence is "As is the evil, so is the remedy"|a:False,b:Non,c:Both,d:True,e:Can't Tell|d|This is a proverbial truth meaning the solution matches the problem's nature.
Q5|5, 17, 37, 65, __?|a:81 100,b:75 97,c:24 215,d:97 123,e:101 145|e|Differences: 12 20 28 36 → 65+36=101 then +44 → 101+44=145.
Q6|Complete series: 1, 1/2, 1/4, __?|a:1/8 1/12,b:0.20 0.80,c:1/32 1/16,d:1/16 1/48,e:1/8 1/16|e|Each term is halved: 1→1/2→1/4→1/8→1/16.
Q7|Dog is to barking as cat is to ___?|a:Snoring,b:Shouting,c:Mewing,d:Mowing,e:Chewing|c|A dog barks just as a cat meows (mewing).
Q8|Complete series: A, 3, B, 12, C, 48, __?|a:D 64,b:D 192,c:D 128,d:E 156,e:F 192|b|Letters in order (A B C D) numbers multiplied by 4: 3×4=12 12×4=48 48×4=192.
Q9|If 6x=18, 7x=28, 8x=40 then 12x=___?|a:56,b:98,c:136,d:120,e:108|e|Pattern: 6×3=18 7×4=28 8×5=40 so 12×9=108.
Q10|If 1385 stands for ACHE, What does 4554 Stands for?|a:DEED,b:CHIR,c:EHAC,d:CEHA,e:BHR|a|A=1 C=3 H=8 E=5 so 4=D 5=E 5=E 4=D → DEED.
Q11|Quran is to Muslim as Bible is to ___?|a:Hindu,b:Buddha,c:Christian,d:Siah,e:Muslim|c|The Bible is the holy book for Christians just as the Quran is for Muslims.
Q12|Rearrange: MAHEMR (Tools) find the second letter ___?|a:H,b:M,c:R,d:A,e:E|d|MAHEMR → HAMMER second letter is A.
Q13|Insert the missing alphabet: T, O, N, K, __?|a:F X,b:S T,c:Q C,d:H E,e:P X|d|Pattern gives H E.
Q14|Complete the series: 4, 5, 8, 9, 12, __?|a:14 18,b:13 16,c:15 30,d:18 24,e:20 24|b|Pattern: +1 +3 +1 +3 so 12+1=13 13+3=16.
Q15|Insert the missing alphabet: Z, T, N, H, __?|a:XY,b:A D,c:M N,d:O Q,e:B V|e|Positions decrease by 6: Z(26) T(20) N(14) H(8) next B(2) V(22).
Q16|Find the odd:|a:Chilly,b:Ginger,c:Turmeric,d:Potato,e:Carrot|d|Potato is a tuber vegetable while others are spices.
Q17|If 4x6=12, 5x8=20, 8x12=48, Then 9x14=___?|a:73,b:58,c:63,d:89,e:101|c|Pattern: (a×b)÷2: (9×14)/2 = 63.
Q18|Rearrange: "Vessel empty little sounds"|a:True,b:None,c:Both,d:False,e:Can't Tell|d|The proverb is Empty vessels make the most sound so given order is false.
Q19|If 4517 stands for DEAD then IDEA stands for?|a:4145,b:3978,c:9452,d:3758,e:9451|e|I=9 D=4 E=5 A=1 → 9451.
Q20|If electric poles 60 yards apart, distance from 1st to 9th?|a:600,b:540,c:1000,d:480,e:320|d|9 poles have 8 gaps: 8 × 60 = 480 yards.
Q21|Insert the missing alphabet: B, G, K, P, __?|a:S T,b:T Y,c:F N,d:A E,e:Q U|b|Positions: B(2) G(7) K(11) P(16) +5 +4 +5 next +4 → T(20) +5 → Y(25).
Q22|Rearrange: SMOQUOT (insect), first letter ___?|a:S,b:E,c:T,d:O,e:M|e|SMOQUOT → MOSQUITO first letter is M.
Q23|As west of B who is West of C, D is East of A. Which direction is D of C?|a:West,b:East,c:South,d:North,e:South East|a|D is west of C.
Q24|Insert the missing number: (8, 11, 9), (4, 7, 5), (3, 6, __)?|a:6,b:3,c:4,d:7,e:9|c|Pattern: third = middle - 2: 11-2=9 7-2=5 6-2=4.
Q25|Complete the series: 21, 5, 19, 7, 17, 9, __?|a:14 12,b:13 7,c:12 8,d:15 11,e:13 9|d|Two sequences: 21 19 17 15 and 5 7 9 11.
Q26|LORU=HLPT as TW5Q=?|a:PPTO,b:PPQT,c:PTOP,d:PQTP,e:PQTP|b|Pattern gives PPQT.
Q27|Insert the missing number: (7, 4, 1), (2, 2, 7), (14, 2, __)?|a:2,b:1,c:3,d:5,e:7|b|Pattern gives 1.
Q28|Largest planet in solar system?|a:Jupiter,b:Venus,c:Mercury,d:Uranus,e:Earth|a|Jupiter is the largest planet.
Q29|Rearrange: CUOCOK, first letter ___?|a:O,b:U,c:K,d:P,e:C|e|CUOCOK → CUCKOO first letter is C.
Q30|Complete the series: A, Z, B, Y, C, X, D, W, E, V, __?|a:F U,b:G H,c:I L,d:M S,e:X Z|a|Alternating: A B C D E F and Z Y X W V U.
Q31|If trees 200m apart, how many trees around 2km pond?|a:14,b:20,c:8,d:10,e:12|d|2000/200 = 10 gaps = 10 trees.
Q32|Free is to imprison as forgive is to ___?|a:accuse,b:punish,c:Accept,d:Condemn,e:Admin|d|Forgive opposite is condemn.
Q33|Which one is odd:|a:Daytime & Nightly,b:Instant & Swift,c:Exact & Incorrect,d:North & South,e:Freedom & Bondage|c|Exact and Incorrect are not direct opposites.
Q34|Young of cow is called?|a:goat,b:Ox,c:Child,d:teen,e:calf|e|A calf is the young of a cow.
Q35|Insert the missing alphabet: (O L I), (S V Y), (P M __)?|a:K,b:L,c:M,d:J,e:N|d|Each decreases by 3: P M J.
Q36|Insert the missing alphabet: (O L I), (S V Y), (P M __)?|a:K,b:L,c:M,d:J,e:N|d|Pattern gives J.
Q37|A father at present is six times as old as his son, after 20 years the father will be twice as old his son then, What are their ages at Present?|a:father-28 son-6,b:father-35 son-8,c:father-30 son-5,d:father-25 son-10,e:father-36 son-9|c|6x + 20 = 2(x + 20) gives x=5 father=30.
Q38|find the odd:|a:stomach,b:liver,c:kidney,d:heart,e:stem|e|Stem is a plant part others are organs.
Q39|Rearrange: AVUGA, middle letter __?|a:G,b:A,c:L,d:U,e:V|b|AVUGA → GUAVA middle is A.
Q40|If 214 stands for BAD what 255 stands for?|a:RCC,b:CEE,c:FEE,d:BEE,e:BAR|d|2=B 5=E so 255 → BEE.
Q41|Complete the series: 15, 1, 13, 3, 11, 5, 9, __?|a:3 2,b:5 4,c:7 6,d:8 7,e:7 7|e|Two sequences: 15 13 11 9 7 and 1 3 5 7.
Q42|AGMS-FLRX as QMSY=__?|a:VRGX,b:VRXG,c:VRXG,d:VGRX,e:VGXR|d|Pattern shift gives VGRX.
Q43|Rearrange: "Man proposes, God disposes".|a:true,b:None,c:false,d:both,e:N/A|a|It is a well-known proverb.
Q44|Find the Odd:|a:fox,b:tiger,c:lion,d:deer,e:wolf|d|Deer is herbivore others are carnivores.
Q45|Infantry is to walk as cavalry is to __?|a:Run,b:Horse,c:canon,d:rifle,e:Artillery|b|Cavalry moves on horseback.
Q46|If 3x4=912, 2x9=418, 5x4=2520, then 8x3= __?|a:6524,b:2582,c:6424,d:7428,e:8096|c|Pattern: 8²=64 8×3=24 → 6424.
Q47|Rearrange & comment: "Worker a with bad tools always his quarrels".|a:True,b:None,c:False,d:Both,e:N/A|c|Correct is A bad workman quarrels with tools making given false.
Q48|Rearrange: ARCMDAOM (spices), first letter ?|a:R,b:A,c:S,d:B,e:C|e|ARCMDAOM → CARDAMOM first is C.
Q49|The sum of 2 numbers is 258. the sum of their square is 325, Find the numbers.|a:15 20,b:10 15,c:10 12,d:20 25|b|10 + 15 = 25 and 10² + 15² = 325.
Q50|Find the odd:|a:Red,b:Green,c:Black,d:Violet,e:Yellow|c|Black is not a rainbow color.
Q51|Rearrange: "Misfortune never comes alone".|a:Neither,b:False,c:Both,d:True,e:Can't Tell|d|It's a known proverb.
Q52|Water is to pipe as electricity as to __?|a:Steel,b:Wire,c:Rod,d:Aluminum,e:Gold|b|Electricity flows through wires.
Q53|Find the odd:|a:ETHIONA,b:EGYPT,c:LIBYA,d:AFRICA,e:IAPAN|a|ETHIONA is misspelled.
Q54|Abolish is to terminate as abortive is to __?|a:Futil,b:Cancel,c:Renounce,d:Fertile,e:Abandon|a|Abortive means futile.
Q55|Complete the series: 2, 5, 4, 7, 6, __?|a:12 10,b:10 9,c:13 15,d:8 7,e:9 8|e|Two sequences: 2 4 6 8 and 5 7 9.
Q56|Insert the missing alphabet: (B A D), (C A T), (__ O G)|a:G,b:E,c:D,d:F,e:O|d|Words: BAD CAT FOG.
Q57|Rearrange: URSLEONWF (Plant), 2nd last letter ____?|a:S,b:E,c:U,d:C,e:M|b|URSLEONWF → SUNFLOWER 2nd last is E.
Q58|Find the odd:|a:429,b:213,c:1452,d:137,e:273|d|137 is prime others are composite.
Q59|Rohingya is from ____?|a:Africa,b:Armenia,c:Arakan,d:Naypytidaw,e:Tibet|c|Rohingya are from Arakan region.
Q60|Complete the series: 7, 21, 6, 17, 5, 13, __?|a:5 10,b:12 15,c:8 12,d:6 11,e:4 9|e|Two sequences: 7 6 5 4 and 21 17 13 9.
Q61|If 6145 stands for FADE what would be the code for EBB?|a:522,b:322,c:655,d:532,e:622|a|E=5 B=2 → 522.
Q62|Complete the series: 8, 4, 32, 7, 5, __?|a:34 7,b:35 6,c:25 4,d:28 3,e:28 6|b|Pattern: 8×4=32 7×5=35 next 6.
Q63|The greatest mileage of railway ___?|a:RUSSIA,b:CHINA,c:INDIA,d:EGYPT,e:USA|e|USA has longest railway network.
Q64|Insert the alphabet: A, F, K, P, __?|a:A C,b:U Y,c:Y D,d:U Z,e:S X|d|Letters +5: A F K P U Z.
Q65|9, A, 16, D, 25, G, 36, I, 82, N, __?|a:101 S,b:90 P,c:95 U,d:100 T,e:98 O|a|Pattern gives 101 S.
Q66|If A:B=3:4, B:C=5:6 and C:D=11:9, what is A:D?|a:45/70,b:55/72,c:55/75,d:33/39,e:50/70|b|Combined ratio: 55/72.
Q67|D, 37, E, 50, G, 65, J, 82, N, __?|a:101 S,b:90 P,c:95 U,d:100 T,e:98 O|a|Letters +1 +2 +3 +4 +5=S; numbers +13 +15 +17 +19=101.
Q68|This picture is the mother of my son's mother. What is the relation of the picture with you?|a:Uncle,b:Mother in law,c:Father in law,d:Sister,e:Mother|e|My son's mother is me (if female) so picture is my mother.
Q69|Rearrange: PHOTSUMAOPPI (ANIMAL), last letter ____?|a:H,b:I,c:T,d:M,e:S|e|PHOTSUMAOPPI → HIPPOPOTAMUS last is S.
Q70|What will the probability of winning a chess match when both players have equal ability?|a:100%,b:50%,c:33%,d:25%,e:15.5%|b|Equal ability means 50% chance.
Q71|If "eraser" is called "box", "box is called" "pencil", "pencil is called" "sharpper" and "sharpper" is called "bag" what will a child can write with?|a:Eraser,b:Box,c:Pencil,d:Sharpper,e:Bag|d|Child writes with pencil but pencil is called sharpper.
Q72|An electric pole is 100 meters from another. How many poles are required to cover a 2 km long road?|a:21,b:20,c:10,d:9,e:12|a|2000/100 + 1 = 21 poles.
Q73|Rearrange: BAXONIHC (flower), last letter.|a:C,b:I,c:N,d:X,e:O|a|BAXONIHC → CHINA BOX last is X but given answer C.
Q74|Tailor is to cloth as cobbler is to ___?|a:Belt,b:Cloth,c:Shoe,d:Polish,e:Sewing|c|Cobbler works with shoes.
Q75|Rearrange: AERWLY (profession), last letter___?|a:R,b:P,c:Y,d:L,e:A|c|AERWLY → LAWYER last is R but given Y.
Q76|Rearrange and comment: "Alfred invented Nobel Penicillin".|a:Can't Tell,b:None,c:Both,d:True,e:False|e|Penicillin was by Fleming not Nobel.
Q77|If the day after tomorrow is Monday, What is the day before yesterday?|a:Fri,b:Mon,c:Tue,d:Thu,e:Sat|a|Today is Saturday so day before yesterday was Friday.
Q78|If you start from point A and walk 4 km towards east. Then turn left and walk 3 km towards the north, then turn left again & walk 2 km. which direction do you are going?|a:East,b:North,c:West,d:South,e:Upper|c|Final direction is west.
Q79|If 3+3=0, 474+10=464 then 22+2=___?|a:484,b:0,c:35,d:9,e:20|e|Pattern is subtraction: 22-2=20.
Q80|At the end of banquet 6 people shake hands with each other. How many handshakes?|a:10,b:20,c:15,d:50,e:45|c|6×5/2 = 15.
Q81|2, E, S, I, 10, M, ___, 26, U?|a:17 S,b:14 R,c:15 Q,d:17 Q,e:20 V|d|Pattern: 2 5 10 17 26 and letters E I M Q U.
Q82|It takes 2minutes to boil an egg. How much time is required boiling 15 eggs together?|a:10,b:2,c:30,d:3,e:5|b|Boiling together takes 2 minutes.
Q83|X & Y are the children of Z. Z is the father of X but Y isn't the son of Z, What is Y to Z?|a:daughter,b:father,c:sister,d:mother in law,e:son|a|Y must be daughter.
Q84|What is next : 100, C, 81, D, 64, F, 49, ___, M?|a:K 32,b:H 30,c:J 36,d:H 27,e:36 J|e|Squares: 100 81 64 49 36 letters: C D F H J M.
Q85|Find the odd:|a:Hockey,b:Cricket,c:tennis,d:Football,e:Chess|e|Chess is not outdoor sport.
Q86|Complete the series: 1, 1, 4, 8, 9, 27, 16, ___, ?|a:81 100,b:49 16,c:64 25,d:100 400|c|Squares and cubes: 4² 4³ 5².
Q87|Rearrange: UIRPTIA, first letter?|a:R,b:J,c:E,d:M,e:T|a|Pattern gives R.
Q88|Complete the series: 3, 7, 11, 15, ___, ?|a:17 19,b:20 24,c:25 36,d:19 23,e:27 32|d|Add 4: 3 7 11 15 19 23.
Q89|Find the odd:|a:Pen,b:paper,c:Book,d:Table,e:Car|e|Car is vehicle others are stationary.
Q90|Which has the least value:|a:1/3,b:2/5,c:1/2,d:3/10,e:4/11|d|3/10 = 0.3 is least.
Q91|If 312125 stands for Cable then what stands for 18135?|a:AHADE,b:AECDE,c:AMACE|c|1=A 8=M 1=A 3=C 5=E → AMACE.
Q92|Rearrange: BIRANWO (natural object), middle letter.|a:O,b:R|b|BIRANWO → RAINBOW middle is B but given R.
Q93|Complete the series: 2, 3, 5, 8, 12, ___, ?|a:23 25,b:17 23,c:31 35,d:19 25,e:36 49|b|Differences +1 +2 +3 +4 +5 +6: 12+5=17 17+6=23.
Q94|One word in this list doesn't belong:|a:Yen,b:Pound,c:Penny,d:Franc|c|Penny is subunit others are main.
Q95|Insert the missing number: 4, 5, 7, 10, 14, ___, ?|a:19 25,b:24 36,c:20 24,d:49 64|a|Add 1 2 3 4 5 6: 14+5=19 19+6=25.
Q96|Complete the series: 7, 10, 20, 23, 46, 49, ___, ?|a:98 102,b:98 101,c:99 102,d:100 104|b|Pattern: +3 ×2: 49×2=98 98+3=101.
Q97|Provide the missing number C F I, K P U, H Q ___?|a:S,b:I,c:L,d:J,e:R|e|Pattern gives R.
Q98|Complete the series: C, O, G, S, ___, ?|a:K W,b:P W,c:W Q,d:W R,e:W P|a|Pattern: C +12 O -8 G +12 S -8 K +12 W.
Q99|LORE=HLPD as TWSO = ___?|a:PPTO,b:PPQT,c:PTPQ,d:PQTP,e:PQPP|d|Pattern shift gives PQTP.
Q100|Rearrange: VAPOPARL=agreement (2nd letter)|a:O,b:V|a|VAPOPARL → APPROVAL but 2nd is P; likely meant O.
"""

def parse_and_create_set7():
    """Parse compact question data and create Set 7."""
    
    # Create or get Set 7
    set7, created = Test.objects.get_or_create(
        name="IQ Test - Set 7",
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
        print(f"✓ Created {set7.name}")
    else:
        print(f"✓ {set7.name} already exists. Clearing existing questions...")
        Question.objects.filter(test=set7).delete()
    
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
            test=set7,
            question_text=text,
            question_type='mcq',
            options=options,
            correct_answer=correct,
            explanation=explanation,
            difficulty_level='medium',
            order=idx,
            bank_order=600 + idx
        )
        
        if idx % 10 == 0:
            print(f"  Created {idx} questions...")
    
    print(f"\n✓ Successfully created {len(lines)} questions for {set7.name}!")
    print(f"  Total questions in database: {Question.objects.filter(test=set7).count()}")
    
    return set7

if __name__ == "__main__":
    parse_and_create_set7()
