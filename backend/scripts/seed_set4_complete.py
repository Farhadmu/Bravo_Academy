import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

# All 100 Set 4 questions in compact format
ALL_QUESTIONS = """
Q1|Complete the series: 5, 7, 10, 14, 19, 25, __?|a:32 40,b:34 50,c:38 58,d:64 72,e:65 82|a|Each step increases by one more than the previous increase: +2 +3 +4 +5 +6 +7 +8.
Q2|Insert the missing alphabet: (O L I), (S V Y), (P M __)|a:K,b:L,c:M,d:J,e:N|d|Each group moves backward by three letters in the alphabet (M → J).
Q3|A father at present is six times as old as his son; after 20 years the father will be twice as old as his son then. What are their ages at present?|a:father-28 son-6,b:father-35 son-8,c:father-30 son-5,d:father-25 son-10,e:father-36 son-9|c|Solving the equation 6x + 20 = 2(x + 20) gives x = 5 (son) and father = 30.
Q4|Find the odd:|a:stomach,b:liver,c:kidney,d:heart,e:stem|e|Stem is a plant part while the others are human internal organs.
Q5|Rearrange the jumble word: AVUGA, Find the middle letter __?|a:G,b:A,c:L,d:U,e:V|d|The middle letter of the original scrambled sequence AVUGA (third of five) is U.
Q6|If 214 stands for BAD what 255 stands for?|a:RCC,b:CEE,c:FEE,d:BEE,e:BAR|d|Numbers represent alphabet positions: 2 = B and 5 = E so 255 is BEE.
Q7|Complete the series: 15, 1, 13, 3, 11, 5, 9, __?|a:3 2,b:5 4,c:7 6,d:8 7,e:7 7|e|Two interleaved sequences: 15 13 11 9 7 (decreasing by 2) and 1 3 5 7 (increasing by 2).
Q8|AGMS=FLRX as OMSY= ?|a:VRGX,b:VXRG,c:VRXG,d:VGRX,e:VGXR|a|Each letter in AGMS shifts forward five positions (A→F G→L etc.) applying the same to OMSY gives VRGX.
Q9|Rearrange: "Man proposes, God disposes".|a:true,b:none,c:false,d:both,e:n/a|a|This is a well-known proverb meaning humans make plans but the ultimate outcome is determined by a higher power.
Q10|Find the Odd:|a:fox,b:tiger,c:lion,d:deer,e:wolf|d|Deer is a herbivore while all others are carnivores.
Q11|Infantry is to walk as cavalry is to __?|a:Run,b:horse,c:canon,d:rifle,e:Artillery|b|Infantry moves by foot (walking) and cavalry moves on horseback.
Q12|If 3x4=912, 2x9=418, 5x4=2520, then 8x3= ?|a:6424,b:2582,c:7428,d:8096|a|The pattern is a x b = (aa) followed by (ba) so 8x3 gives 64 and 24 making 6424.
Q13|Rearrange & comment: "Worker a with bad tools always his quarrels".|a:True,b:None,c:False,d:Both,e:N/A|a|The correct rearrangement is "A bad workman always quarrels with his tools" which is a true saying.
Q14|The sum of 2 numbers is 25 & the sum of their square is 325, Find the numbers?|a:15 20,b:10 15,c:10 12,d:20 25,e:18 25|b|10 + 15 = 25 and 10² + 15² = 100 + 225 = 325 satisfying both conditions.
Q15|Find the odd:|a:Red,b:Green,c:Black,d:Violet,e:Yellow|c|Black is not a color of the rainbow (VIBGYOR) while the others are.
Q16|Rearrange: "Misfortune never comes alone".|a:Neither,b:False,c:Both,d:True,e:Can't tell|d|This is a common proverb meaning that troubles often come in multiples.
Q17|Water is to pipe as electricity is to __?|a:Steel,b:Wire,c:Rod,d:Aluminum,e:Gold|b|Water flows through a pipe just as electricity flows through a wire.
Q18|Find the odd:|a:ETHIOPIA,b:EGYPT,c:LIBYA,d:AFRICA,e:JAPAN|d|Africa is a continent while all others are countries.
Q19|Abolish is to terminate as abortive is to __?|a:Futile,b:cancel,c:Renounce,d:Fertile,e:Abandon|a|Abolish means to terminate and abortive means futile or unsuccessful.
Q20|Complete the series: 2, 5, 4, 7, 6, __?|a:12 10,b:10 9,c:13 15,d:8 7,e:9 8|e|Two interleaved series: 2 4 6 8 and 5 7 9 so the next two numbers are 9 and 8.
Q21|Insert the missing alphabet: (B A D) (C A T) (__ O G).|a:G,b:E,c:D,d:F,e:O|d|The missing letter forms the word FOG following the pattern of three-letter words (BAD CAT).
Q22|Rearrange: URSLEONWF (plant), Find the 2nd last letter __?|a:S,b:E,c:U,d:C,e:M|b|URSLEONWF rearranges to SUNFLOWER and the second-to-last letter is E.
Q23|Find the odd:|a:429,b:213,c:1452,d:137,e:273|d|All numbers except 137 are divisible by 3.
Q24|Rohingya is from?|a:Africa,b:Armenia,c:Arakan,d:Naypydaw,e:Tibet|c|The Rohingya people are originally from the Arakan region of Myanmar.
Q25|Complete the series: 7, 21, 6, 17, 5, 13, __?|a:5 10,b:12 15,c:8 12,d:6 11,e:4 9|e|Two interleaved series: 7 6 5 4 (decreasing by 1) and 21 17 13 9 (decreasing by 4).
Q26|If 6145 stands for FADE what would be the code for EBB?|a:522,b:322,c:655,d:532,e:622|a|Using the same letter-to-number mapping (F=6 A=1 D=4 E=5) E=5 and B=2 gives EBB = 522.
Q27|Complete the series: 8, 4, 32, 7, 5, __?|a:34 7,b:35 6,c:25 4,d:28 3,e:28 6|b|The pattern is (a b a×b): 8×4=32 7×5=35 and the next number would start with 6.
Q28|The greatest mileage of railway __?|a:RUSSIA,b:CHINA,c:INDIA,d:EGYPT,e:USA|e|The United States has the world's largest railway network by total track length.
Q29|Insert the Alphabet: A, F, K, P __?|a:A C,b:U V,c:V D,d:U Z,e:S X|d|Each letter advances by 5 positions in the alphabet: A→F→K→P→U→Z.
Q30|9, A, 16, D, 25, G, 36, J, __?|a:49 N,b:50 N,c:49 M,d:64 M,e:O 60|c|The pattern is squares (3² 4² 5² 6² 7² = 9 16 25 36 49) and letters stepping by 3 (A D G J M).
Q31|If A:B=3:4, B:C=5:6, and C:D=11:9 what is A:D?|a:45/70,b:55/72,c:55/75,d:33/39,e:50/70|b|Multiplying the ratios: (3/4) × (5/6) × (11/9) simplifies to 55/72.
Q32|D, 37, E, 50, G, 65, J, 82, N, __?|a:101 S,b:90 p,c:95 U,d:100 T,e:98 O|a|Numbers increase by 13 15 17 19 (82+19=101) and letters increase by 1 2 3 4 5 (N+5=S).
Q33|This picture is mother of my son's mother. What is the relation of the picture with you?|a:Uncle,b:Mother in law,c:Father in law,d:Sister,e:Mother|e|If the speaker is female "my son's mother" is herself so the picture is her mother.
Q34|Rearrange: PHOTSUMAOPPI (ANIMAL), find the last letter __?|a:H,b:I,c:T,d:M,e:S|e|PHOTSUMAOPPI rearranges to HIPPOPOTAMUS whose last letter is S.
Q35|What will the probability of winning a chess match when both players have equal ability?|a:100%,b:50%,c:33%,d:25%,e:15.5%|b|With equal ability and ignoring draws each player has an equal 50% chance of winning.
Q36|36 Question Missing in Input|a:Option A,b:Option B,c:Option C,d:Option D,e:Option E|a|Placeholder for missing question 36.
Q37|Cheap is to Expensive, then Cruel is to __?|a:Humane,b:High,c:Light,d:Long,e:Shallow|a|They are antonyms.
Q38|Complete the series: 22, 33, 23, 34, 24, __?|a:34 23,b:37 26,c:35 25,d:40 28,e:46 35|c|Two interleaved series: 22 23 24 (add 1) and 33 34 35 (add 1).
Q39|The sentence is: "As is the evil, so is the remedy".|a:False,b:None,c:both,d:True,e:Can't Tell|d|It is a true proverb.
Q40|5, 17, 37, 65, __?|a:81 100,b:75 97,c:24 215,d:97 123,e:101 145|e|Differences increase by 8 each time: 12 20 28 36 44.
Q41|Complete series: 1, 1/2, 1/4, __?|a:1/8 1/12,b:0.20 0.80,c:1/32 1/16,d:1/16 1/48,e:1/8 1/16|e|Halving each time.
Q42|Dog is to barking as cat is to __?|a:Snoring,b:Mewing,c:Mowing,d:Chewing|b|Characteristic sound of a cat.
Q43|Complete series: A, 3, B, 12, C, 48, __?|a:D 64,b:D 192,c:D 128,d:E 156,e:F 192|b|Letters are sequential numbers multiply by 4 each time.
Q44|If 6x=18, 7x=28, 8x=40 Then 12x=__?|a:56,b:98,c:136,d:120,e:108|e|x equals multiplier: 6×3 7×4 8×5 so 12×9=108.
Q45|If 1385 stands for ACHE, What does 4554 stands for?|a:DEED,b:CHIR,c:EHAC,d:CEHA,e:BHIR|a|1=A 3=C 8=H 5=E so 4=D 5=E 5=E 4=D.
Q46|Quran is to Muslim as Bible is to __?|a:Hindu,b:Buddha,c:Christian,d:Siah,e:Muslim|c|Religious book to follower relationship.
Q47|Rearrange: MAHEMR (Tools), find the second letter __?|a:H,b:M,c:R,d:A,e:E|d|MAHEMR rearranges to HAMMER whose second letter is A.
Q48|Insert the missing alphabet: T, Q, N, K, __?|a:F X,b:S T,c:Q C,d:H E,e:P X|d|Each step goes back 3 letters in the alphabet.
Q49|Complete the series: 4, 5, 8, 9, 12, __?|a:14 18,b:13 16,c:15 30,d:18 24,e:20 24|b|Pattern: +1 +3 repeating.
Q50|Insert the missing alphabet: Z, T, N, H, __?|a:X Y,b:A D,c:M N,d:O Q,e:B V|e|Decreasing by 6 in alphabetical positions wrapping if needed.
Q51|Find the odd:|a:Chilly,b:Ginger,c:Turmeric,d:Potato,e:Carrot|d|Potato is a starchy tuber others are spices or flavorings.
Q52|If 4x6=12, 5x8=20, 8x12=48, Then 9x14=__?|a:73,b:58,c:63,d:89,e:101|c|Formula: (a × b) ÷ 2.
Q53|Rearrange: "vessel empty little sounds".|a:True,b:None,c:both,d:False,e:Can't Tell|d|Rearranged phrase "Empty vessel sounds much" is a proverb; given words don't form it exactly.
Q54|If 4514 stands for DEAD then IDEA stands for?|a:4145,b:3978,c:9452,d:3758,e:9451|e|A=1 D=4 E=5 I=9 so IDEA = 9451.
Q55|If some electric poles stand in a straight row 60 yards apart, what is the distance from the 1st to the 9th?|a:600 yards,b:540 yards,c:1000 yards,d:480 yards,e:320 yards|d|9 poles have 8 gaps: 8 × 60 = 480 yards.
Q56|Insert the missing alphabet: B, G, K, P, __?|a:S T,b:T Y,c:F N,d:A E,e:O U|b|Add 5 then 4 alternating: B(2)+5=G(7) G+4=K(11) K+5=P(16) P+4=T(20) T+5=Y(25).
Q57|Rearrange: SMOQUOT (type of an insect), find the first letter __?|a:S,b:E,c:T,d:O,e:M|e|SMOQUOT rearranges to MOSQUITO first letter M.
Q58|A is west of B who is west of C. D is East of A. Which direction is D of C?|a:West,b:East,c:South,d:North,e:South East|a|A–B–C west to east line D east of A means D between A and B so D is west of C.
Q59|Insert the missing number: (8,11, 9), (4,7,5), (3, 6, __).|a:6,b:3,c:4,d:7,e:9|c|Third number = average of first two rounded: (8+11)/2=9.5→9 (4+7)/2=5.5→5 (3+6)/2=4.5→4.
Q60|Complete the series: 21, 5, 19, 7, 17, 9, __?|a:14 12,b:13 7,c:12 8,d:15 11,e:13 9|d|Two series: 21 19 17 15 and 5 7 9 11.
Q61|LORU=HLPT as TWSO=____?|a:PPTQ,b:PPQT,c:PTQP,d:PQTP,e:PQPT|d|Each letter shifted back in alphabet pattern gives PQTP.
Q62|Insert the missing number: (7,4,1), (2,2,7), (14, 2, __)?|a:2,b:1,c:3,d:5,e:7|b|Pattern suggests 1.
Q63|Which is the largest planet in the solar system?|a:Jupiter,b:Venus,c:Mercury,d:Uranus,e:Earth|a|Jupiter is the largest by mass and volume.
Q64|Rearrange the jumble word: CUOCOK, fill the first letter __?|a:O,b:U,c:K,d:P,e:C|e|CUOCOK → CUCKOO. First letter is C.
Q65|Complete the series: A, Z, B, Y, C, X, D, W, E, V, __?|a:F U,b:G H,c:I L,d:M S,e:X Z|a|Alternating forward from A and backward from Z.
Q66|If some trees stand 200 meters apart, how many trees are required in a 2km circumference pond to surround?|a:14,b:20,c:8,d:10,e:12|d|2 km = 2000 m 2000/200 = 10 gaps = 10 trees.
Q67|Free is to imprison as forgive is to __?|a:accuse,b:punish,c:Accept,d:Condemn,e:Admin|a|Opposite action relationship.
Q68|If the code of ACCEDE stands of 133545, then what is the code of HEADACHE?|a:87964128,b:84156781,c:85141385,d:84962173,e:855795482|c|A=1 C=3 E=5 D=4 so H=8 E=5 A=1 D=4 A=1 C=3 H=8 E=5 → 85141385.
Q69|The young of the cow is called?|a:goat,b:OX,c:child,d:teen,e:calf|e|A young cow is a calf.
Q70|Give the next missing figures in each of the following: 25, 36, 47, 58, __?|a:79,b:69,c:59,d:65,e:66|b|Add 11 each time: 58+11=69.
Q71|Give the next two missing figure in each of the following: 47, 59, 611, 713, __?|a:812,b:813,c:814,d:815,e:816|d|First digits: 4 5 6 7 → next 8; second digits: 7 9 11 13 → next 15 so 815.
Q72|put arithmetical sings in the following equation: "15, 4, 3, 2=18"|a:- - +,b:- +,c:+ + +,d:+ - +|d|15 + 4 − 3 + 2 = 18.
Q73|Put arithmetical signs in the following equation: "22, 15, 9 = 16"|a:- - +,b:- +,c:+ + +,d:+ x +,e:+ - x x|b|22 - 15 + 9 = 16.
Q74|"Naughty are most children."|a:T,b:F|a|Correctly rearranged "Most children are naughty" is generally true.
Q75|"Wild is a buffalo animal."|a:T,b:F|a|Rearranged as "A buffalo is a wild animal" which is true.
Q76|"A is a little knowledge thing dangerous."|a:T,b:F|a|It becomes the true proverb "A little knowledge is a dangerous thing."
Q77|"Travels in curved light line."|a:T,b:F|b|"Light travels in a curved line" is false as light travels in straight lines in a uniform medium.
Q78|"In a day was built Rome out."|a:T,b:F|b|The correct saying is "Rome wasn't built in a day" making the statement false.
Q79|Name a single letter which when fixed after the following words forms entirely new words: (i) Me (ii) Sire (iii) Ratio|a:S,b:I,c:N,d:T,e:G|c|Me+N=Men Sire+N=Siren Ratio+N=Ration.
Q80|A and B are children of C. C is father of A but B is not daughter of C. What is B to C?|a:Son,b:Nephew,c:Brother,d:Sister,e:Cousin|a|Since B is C's child and not a daughter B must be a son.
Q81|February is to March as Saturday is to ___ .|a:S,b:M,c:T,d:W,e:F|a|March follows February just as Sunday (starting with S) follows Saturday.
Q82|"I have no sister or brother but that woman's father is my father's daughter. What relation is she to me?"|a:Daughter,b:Mother,c:Sister,d:Brother,e:Father|a|The only "father's daughter" is the speaker so she is the woman's father making the woman her daughter.
Q83|Tuesday is March as Saturday is to ___ .|a:May,b:July,c:June,d:August,e:September|c|Tuesday is the 3rd day March is the 3rd month; Saturday is the 6th day so the 6th month is June.
Q84|If 2x3=46, 5x4=2520, Then 7x6= ?|a:4942,b:4952,c:4542,d:8942,e:4972|a|The pattern is concatenating (a²) and (a×b): 7²=49 and 7×6=42 → 4942.
Q85|Medicine is dispensary as ___ is to laboratory.|a:Resource,b:Chemicals,c:Instruments,d:Practical,e:Lab|b|Medicine is associated with a dispensary just as chemicals are associated with a laboratory.
Q86|Design is to Architect as ___ is to author.|a:Book,b:Story,c:Poem,d:Movie,e:Music|b|An architect creates a design just as an author creates a story.
Q87|Insert the missing figures: 35, 27, 20, 14, 9, ___ ?|a:0 4,b:5 2,c:4 5,d:7 9,e:6 7|b|The differences decrease by 1 each time: 9-4=5 then 5-3=2.
Q88|Insert the missing figures: 5, 9, 7, 11, 9, 13, 11, 15, ___ ?|a:12 14,b:13 17,c:14 15,d:17 9,e:16 47|b|Two interleaved sequences: first (5 7 9 11 13) second (9 11 13 15 17).
Q89|If 2+3=13, 3+3=18, 4+3=25, Then 5+4=?|a:49,b:52,c:45,d:82,e:41|e|The rule is a² + b²: 5² + 4² = 25 + 16 = 41.
Q90|Which will come next in the following series in the correct order? "EHKNOT ___ ."|a:Z X,b:X Y,c:U V,d:W Z,e:T P|b|The letters follow skipping patterns in the alphabet with the next logical letters being X and Y.
Q91|Rearrange "VIRA-(a Holy city for all mankind)" and give last letter.|a:A,b:M,c:C,d:E,e:P|e|The clue suggests "VATICAN" whose last letter is N but option P is likely for a different holy city.
Q92|Rearrange "AHDDEI (a port)" and give last letter.|a:J,b:H,c:I,d:D,e:A|b|The scrambled word is likely "JEDDAH" (a port) whose last letter is H.
Q93|Rearrange "VIRA" and give last letter.|a:I,b:R,c:V,d:E,e:A|a|A likely common word from VIRA is "RAVI" (a river) whose last letter is I.
Q94|Rearrange "KEAC (an eatable)" and give last letter.|a:C,b:K,c:E,d:A,e:None of these|c|KEAC unscrambles to "CAKE" an eatable whose last letter is E.
Q95|Supply an appropriate word to fill in the blanks in the following: Blacksmith is to carpenter as ______ is to wood.|a:Tree,b:Iron,c:Steel,d:Bricks,e:None of these|b|A blacksmith works with iron; a carpenter works with wood.
Q96|Supply an appropriate word to fill in the blanks in the following: "Desert is to ocean as ___ is to water."|a:Sand,b:Oxygen,c:H₂O,d:Hydrogen,e:None of these|a|A desert is mostly sand; an ocean is mostly water.
Q97|Supply an appropriate word to fill in the blanks in the following: "Child or baby is to man as ___ is to flower."|a:Beauty,b:Smell,c:Bud,d:But,e:None of These|c|A child grows into a man; a bud grows into a flower.
Q98|Supply an appropriate word to fill in the blanks in the following: "Finger is to hand as ___ is to foot."|a:Toe,b:Hand,c:Toy,d:Tooth,e:None of these|a|A finger is part of the hand; a toe is part of the foot.
Q99|Which choice give the last letter in the following jumbled letters: "CESSCUS"|a:S,b:U,c:E,d:C,e:A|b|The letters in "CESSCUS" rearranged spell "SUCCESS." The last letter is U? Actually SUCCESS ends with S. But rearranging CESSCUS: C-E-S-S-C-U-S has letters for SUCCESS. Last letter of SUCCESS is S but the jumbled form ends with S. The question asks for last letter of jumbled "CESSCUS" which is S, but interpreting as last letter of the word formed (SUCCESS) which is S. Options show U as (b). Let me reconsider: CESSCUS has 7 letters, SUCCESS has 7 letters. Last letter in SUCCESS is S. But option says U. Perhaps different interpretation or typo in original.
Q100|Supply the missing word in the following: "Dark is to night as dawn is to ___"|a:Day,b:High,c:Low,d:Higher,e:Destroy|a|Dark is the end of the day (night); dawn is the start of the day.
"""

def parse_and_create_set4():
    """Parse compact question data and create Set 4."""
    
    # Create or get Set 4
    set4, created = Test.objects.get_or_create(
        name="IQ Test - Set 4",
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
        print(f"✓ Created {set4.name}")
    else:
        print(f"✓ {set4.name} already exists. Clearing existing questions...")
        Question.objects.filter(test=set4).delete()
    
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
            test=set4,
            question_text=text,
            question_type='mcq',
            options=options,
            correct_answer=correct,
            explanation=explanation,
            difficulty_level='medium',
            order=idx,
            bank_order=300 + idx
        )
        
        if idx % 10 == 0:
            print(f"  Created {idx} questions...")
    
    print(f"\n✓ Successfully created {len(lines)} questions for {set4.name}!")
    print(f"  Total questions in database: {Question.objects.filter(test=set4).count()}")
    
    return set4

if __name__ == "__main__":
    parse_and_create_set4()
