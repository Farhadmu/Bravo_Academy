import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

# Set 6 questions in compact format (note: some question numbers missing in original data)
ALL_QUESTIONS = """
Q1|Find the odd:|a:insects,b:Rock,c:Stone,d:Mountain,e:Hill|a|Insects are living things while all others are non-living geological features.
Q2|Complete the series: 2, 4, 5, 10, 11, 22, __?|a:20 42,b:22 44,c:21 41,d:23 46,e:22 42|d|The pattern is multiply by 2 then add 1 repeating: 2×2=4 4+1=5 5×2=10 10+1=11 11×2=22 22+1=23 23×2=46.
Q3|Find the odd:|a:Cock,b:Bull,c:Tiger,d:Lion,e:Vixen|e|Vixen is a female fox while all others refer to male animals.
Q4|Rearrange: NOLDEG (color), first letter __?|a:G,b:N,c:L,d:D,e:E|a|NOLDEG rearranges to GOLDEN and the first letter is G.
Q5|Find the odd:|a:Bulb,b:Candle,c:Torch,d:Lamp,e:Fan|e|Fan moves air while all others are sources of light.
Q6|Which one is odd:|a:Tea & Cup,b:Pencil & Lead,c:Aeroplane & Postman,d:Photo & Frame|c|The postman is not an essential part of an aeroplane unlike the other pairs.
Q7|What is the opposite word of VIRTUE?|a:Vice,b:Vich,c:Vate,d:Pro,e:Ace|a|Vice is the direct antonym of virtue.
Q8|If 7-2=52, 9-3=63, 6-2=42 then 6-3=__?|a:36,b:33,c:28,d:31,e:9|b|Pattern gives 6-3 = 33.
Q9|If 2x3=49, 5x3=259 & 7x1=491, Then 4x8=__?|a:1614,b:1466,c:1646,d:1664,e:4661|d|Pattern: a x b = (a²)(b²): 2²=4 3²=9 → 49; 4²=16 8²=64 → 1664.
Q10|Care is Scare as Hare is to __?|a:Ghare,b:Hares,c:Jiff,d:Sphere,e:There|e|It is a rhyming analogy: Care→Scare Hare→There.
Q11|Mail is to Mail As __ is to Hall.|a:Abyss,b:Hire,c:Hall,d:Sphere,e:Share|c|Mail pairs with itself Hall pairs with itself (different meanings same spelling).
Q12|3 7 9 5 2 6 4 8 3 7 2 9 6 1 8: what is the sum of all the odd numbers minus the sum of all the even numbers?|a:8,b:10,c:12,d:14,e:6|a|Odds: 3+7+9+5+3+7+9+1=44; Evens: 2+6+4+8+2+6+8=36; 44-36=8.
Q13|Which one is odd:|a:Dhaka,b:Calcutta,c:New York,d:Karachi,e:Kabul|c|New York is in America while others are capital or major cities in South Asia.
Q14|Jibon will be Atime as old after 30 years as he is now. How old is Jibon now?|a:10,b:15,c:6,d:9,e:23|b|If he is x years old now after 30 years he is x+30 which is 3 times as old as now then x+30=3x → 2x=30 → x=15.
Q15|If 2x2=8, 3x3=18, Then 4x4=__?|a:12,b:16,c:34,d:144,e:32|e|Pattern: a x a = 2×(a×a): 2×4=8 2×9=18 so 4×4=16 2×16=32.
Q16|Sand is to Desert as __ to cloud.|a:Sky,b:Atmosphere,c:Water,d:Cloud,e:Ice|c|Sand is the main component of a desert just as water is the main component of a cloud.
Q17|Rearrange: CATARINCAT, related to:|a:flower,b:transport,c:continent,d:tools,e:ocean|c|CATARINCAT rearranges to ANTARCTICA which is a continent.
Q18|At the end of a banquet 7 people shake hands with each other. How many handshakes?|a:1,b:21,c:20,d:25,e:15|b|Number of handshakes = n(n-1)/2 = 7×6/2 = 21.
Q19|High is to low as want is to __?|a:like,b:Poor,c:Need,d:Poverty,e:Plenty|e|High and low are opposites in quantity/degree just as want (lack) and plenty (abundance) are opposites.
Q20|Rearrange: TBCHERU, (Profession) Second Last letter __?|a:B,b:E,c:E,d:H,e:R|e|TBCHERU rearranges to BUTCHER; the second last letter is R.
Q21|Rearrange: DAPES (tools), find middle letter __?|a:S,b:D,c:E,d:A,e:P|e|DAPES rearranges to SPADE; the middle letter is A.
Q22|Drop is to Ocean as __ is to Star?|a:Sun,b:Blue,c:Earth,d:Sky,e:Planet|a|A drop is a small part of an ocean just as the Sun is a star.
Q23|Which one is odd:|a:Agree & Reject,b:Control & Open,c:Well & Woe,d:Jump & Obstacle,e:Well & Decent|d|In all other pairs the two words are antonyms; Jump and Obstacle are not antonyms.
Q24|If 4x6=12, 5x8=20 & 16x5=40, Then 24x4=__?|a:44,b:48,c:84,d:69,e:96|b|Pattern: a x b = (a×b)/2: 4×6=24/2=12; 24×4=96/2=48.
Q25|Sunday is to Tuesday as Saturday is to __?|a:Fri,b:Thu,c:Wed,d:Mon,e:Sun|d|Sunday and Tuesday are two days apart; similarly Saturday and Monday are two days apart.
Q26|March is to August as June is to __?|a:July,b:April,c:November,d:May,e:March|c|March and August are 5 months apart; similarly June and November are 5 months apart.
Q27|Find odd:|a:Student & Teacher,b:Science & Robot,c:Book & Page,d:Tailor & Gentle,e:Car & Driver|d|Tailor and Gentle are not directly related by function or part.
Q28|Complete the series 2, 4, 7, 9, 12, 14, 17, __?|a:19 22,b:18 22,c:19 25,d:22 18,e:24 19|a|Pattern: +2 +3 repeating: 2+2=4 4+3=7 7+2=9 9+3=12 12+2=14 14+3=17 17+2=19 19+3=22.
Q29|Rearrange: MNISALE = Name of a flower (Middle Letter):|a:A,b:F,c:M,d:S,e:J|d|MNISALE rearranges to JASMINE; the middle letter is S.
Q30|Complete the series 1, 4, 2, 5, 3, 6, 4, 7, __?|a:3 6,b:5 8,c:8 6,d:5 7,e:6 8|b|Pattern: Two interleaved sequences: 1 2 3 4 5 and 4 5 6 7 8 → next are 5 and 8.
Q31|BAD=YZW & FIGHT=URTSG, then HIGH=__?|a:SSRT,b:SRST,c:RSTS,d:TRSS,e:SRTS|b|Each letter is replaced by its opposite in the alphabet: H↔S I↔R G↔T H↔S → SRST.
Q32|Write down the fifth letter after the tenth letter of the alphabet:|a:S,b:N,c:R,d:O,e:K|d|The tenth letter is J; the fifth letter after J is O.
Q33|Which one is odd:|a:Medicine,b:Failure,c:Examination,d:Hard Work,e:Student|b|Failure is a negative outcome while the others are associated with education or success.
Q34|F, 125, I, 64, L, 27, O, __?|a:8 5,b:10 R,c:9 5,d:12 Q,e:8 R|e|Pattern: Letters increase by 3 (F→I→L→O→R) numbers are cubes descending: 5³=125 4³=64 3³=27 next 2³=8 so 8 and next letter R.
Q35|Which one odd:|a:Hot & Cold,b:Short & Long,c:Hard & Soft,d:West & South,e:Love & Hate|d|West and South are both directions (not opposites) while the other pairs are direct antonyms.
Q36|Time for tide and none waits (T & F):|a:True,b:False,c:N/A,d:None,e:All|a|The proverb Time and tide wait for none is a true statement.
Q37|Rearrange: RUNUSA = Planet (Fill the 2nd last letter):|a:A,b:U,c:R,d:E,e:N|e|RUNUSA rearranges to URANUS; the second last letter is N.
Q38|Monday is Sunday as Friday is ___?|a:Tue,b:Fri,c:Mon,d:Wed,e:Thu|e|Monday follows Sunday so Friday follows Thursday.
Q39|Complete the Series: 1, 8, 4, 27, 9, 64, 16, __?|a:125 25,b:45 125,c:25 45,d:65 73,e:75 25|a|The series alternates between a square (1 4 9 16) and a cube (8 27 64) so next are 125 (5³) and 25 (5²).
Q40|ZFT = YES as JHXBZ = ___?|a:HHWAY,b:HGHWAY,c:HIGHWAY,d:HIGHWAY,e:NONE|c|Each letter shifted one backward: JHXBZ gives HIGHWAY.
Q41|Complete the series: 14, 3, 12, 3, 10, 3, __?|a:5 5,b:5 8,c:7 3,d:8 3,e:8 6|d|The even positions are all 3 and odd positions decrease by 2 (14 12 10 8).
Q42|Write two vowels which come before the four last alphabets:|a:O U,b:D,c:A M,d:M D,e:R|a|The four last alphabets are W X Y Z and the vowels before them are O and U.
Q43|Complete the series: 1, 2, 3, 5, 8, __?|a:13 22,b:12 21,c:13 21,d:13 24,e:25 13|c|This is the Fibonacci sequence: 1+2=3 2+3=5 3+5=8 5+8=13 8+13=21.
Q44|Find odd:|a:Sparrow,b:Crow,c:Pigeon,d:Woodpecker,e:Bat|e|Bat is a mammal while all others are birds.
Q45|Food is to Growth as knowledge is to ___?|a:Wish,b:Light,c:Intelligent,d:Clever,e:Jay|c|Food leads to growth just as knowledge leads to intelligence.
Q46|Cheap is to expensive, then Cruel is to ___?|a:Humane,b:High,c:Light,d:Long,e:Shallow|a|Cheap and expensive are antonyms so cruel's opposite is humane.
Q47|Find odd:|a:Gynecologist,b:Doctor,c:Obstetrician,d:Dermatologist,e:Pulmonologist|b|Doctor is a general term while the others are specialists.
Q48|Find odd:|a:Lion,b:Sheep,c:Eagle,d:Elephant,e:Tiger|b|Sheep is a herbivore while others are carnivores or predators.
Q49|Thermometer is to Temperature as Speedometer is to ___?|a:Speed,b:Pressure,c:Velocity,d:Distance|a|A thermometer measures temperature just as a speedometer measures speed.
Q50|Which one is odd:|a:Daytime & Nightly,b:Instant & Swift,c:Exact & Incorrect,d:North & South,e:Freedom & Bondage|c|Exact and Incorrect are antonyms but the others are either synonyms or related pairs.
Q51|Complete the series: 2, 2, A, 4, 3, C, 6, E, 8, 8, 6, 10, __?|a:13 1,b:L 13,c:14 1,d:13 L,e:14 H|d|Pattern alternates between numbers and letters: next 13 L.
Q52|One morning A and B were talking face to face at a crossing. If B's shadow was exactly to the left of A, which direction was A facing?|a:East,b:West,c:North,d:South,e:North west|c|Morning shadows fall west so if B's shadow is to A's left A must be facing north.
Q53|Find next: D, 8, F, 27, I, 64, __, R?|a:125 M,b:97 M,c:N 144,d:M 125,e:87 0|d|Letters skip (D→F→I→M) numbers are cubes (2³ 3³ 4³ 5³=125).
Q54|Find odd:|a:Well & Woe,b:Disloyal & Treacherous,c:Extravagant & Loutish,d:Happy & Glad,e:Want & Need|c|Extravagant and Loutish are not synonyms while other pairs are.
Q55|By dividing a number by 6 & then adding 13, we get 19. What is the number?|a:56,b:36,c:63,d:75,e:65|b|Solve (x/6) + 13 = 19 → x/6 = 6 → x = 36.
Q56|If Iron is to Wood, then ___ is to Carpenter.|a:Goldsmith,b:Beggar,c:Ornaments,d:Blacksmith,e:Both a & b|d|Iron is to Blacksmith as Wood is to Carpenter.
Q57|If electric poles stand 1.25 km apart, what is the distance from 1st to the 10th?|a:1125 meters,b:1000 meters,c:11250,d:10125 meters,e:11 Km|c|Distance = (10-1) × 1.25 km = 11.25 km = 11250 meters.
Q58|Doctors advised to take a pill every after an hour. How much time requires taking 10 pills?|a:8 Hours,b:9 Hours,c:10 Hours,d:11 Hours,e:not any one|b|First pill at time 0 then one each hour so 10 pills take 9 intervals of 1 hour.
Q59|Find odd:|a:Mathematics & algebra,b:Petals & flowers,c:Pages & book,d:Water & wind,e:Jute & gunny bag|d|Water and wind are not part-whole like the others.
Q60|Complete the series 5, 20, 6, 24, 7, 28, __?|a:32 10,b:28 32,c:8 32,d:8 36,e:10 32|c|Pattern: multiply by 4 (5×4=20) then next +1 and multiply by 4 (8×4=32).
Q61|Find the odd:|a:Tank,b:Canon,c:Machinegun,d:Rifle,e:Submarine|e|Submarine is naval while others are land/army weapons.
Q62|Complete the series: 7, 10, 20, 23, 46, __?|a:49 98,b:48 98,c:49 96,d:45 95,e:95 45|a|Pattern: +3 ×2 (7→10→20→23→46→49→98).
Q63|If 03 days before Yesterday was Sunday, what is the day tomorrow?|a:Mon,b:Sun,c:Tue,d:Fri,e:Sat|d|3 days before yesterday = 4 days before today was Sunday so today is Thursday tomorrow is Friday.
Q64|Complete: B/V, C/K, D/W, E/V, F/U, M/__/Z|a:T A,b:N C,c:P B,d:N A,e:F/Z|d|First letters: B C D E F M N; second coded pattern gives N A.
Q65|Rearrange and tell: "Divided we united stand we fail"|a:True,b:False,c:N/A,d:None,e:All|a|Correct: United we stand divided we fail which is a true statement.
Q66|Attraction is to Repulsion as Confidence is to ___?|a:Bravery,b:Resilient,c:Doubt,d:Strong,e:Coward|c|Attraction and repulsion are opposites just as confidence's opposite is doubt.
Q67|2, 5, 10, 17, 26, __?|a:30 39,b:32 40,c:40 55,d:35 45,e:37 50|e|Differences increase by 2: +3 +5 +7 +9 +11 +13 → 26+11=37 37+13=50.
Q68|A race always have ___?|a:Viewers,b:Track,c:Umpire,d:Competitor,e:Win|d|A race must have at least one competitor.
Q69|Rearrange: NAKEBBOC, find the 2nd letter ___?|a:A,b:K,c:C,d:B,e:N|d|Rearranges to BACKBONE second letter is B.
Q70|Lion is to cub as Dog is to ___?|a:Calf,b:Kitten,c:Puppy,d:Chicken,e:Pig|c|The young of a dog is called a puppy.
Q71|Rearrange: HPOROTRAGAHPE(profession), Fill the last letter|a:H,b:R,c:R,d:T,e:G|b|Rearranged to PHOTOGRAPHER last letter is R.
Q72|Proud is to satisfied as Abundance is to ___?|a:Rich,b:Poor,c:Plenty,d:Scarcity,e:Shortage|c|Abundance is a synonym of plenty.
Q73|Pain is to Relief as Invent is to ___?|a:Agony,b:Destroy,c:Discover,d:Design,e:Monotonous|b|Relief is opposite of pain and destroy is opposite of invent.
Q74|Complete the series: 2, 4, 7, 9, 12, 14, 17, ___, ___|a:19 24,b:24 19,c:18 22,d:15 25,e:19 22|e|Pattern: +2 +3 repeating so 17+2=19 19+3=22.
Q75|Time is to watch as Blood Pressure is to ___?|a:Speedometer,b:Barometer,c:Thermometer,d:Sphygmomanometer,e:Kilometer|d|A sphygmomanometer measures blood pressure.
Q76|Complete the series: 1, 4, 2, 5, 3, 6, 4, 7, ___, ___|a:5 8,b:4 8,c:7 9,d:4 9,e:5 4|a|Two interleaved series: 1 2 3 4 5 and 4 5 6 7 8.
Q77|GORGEOUS is to ATTRACTIVE as ___ is to REFUSAL.|a:Worried,b:Exercise,c:Addiction,d:Accept,e:Repulsion|e|Repulsion is a synonym of refusal.
Q78|If ZEST=0987 & BEAST=29487, So BZEAST=___|a:204987,b:208497,c:908417,d:209487|d|Using codes: Z=0 E=9 S=8 T=7 B=2 A=4 so BZEAST = 209487.
Q79|Right is to wrong as Ruin is to ___?|a:Terminate,b:Destroy,c:Rescue,d:Crush,e:Invent|c|Rescue is opposite of ruin.
Q80|Complete the series: 7, 9, 18, 20, 40, 42, ___, ___|a:84 86,b:86 84,c:54 86,d:84 86,e:90 86|a|Pattern: +2 ×2 repeating so 42×2=84 84+2=86.
Q81|Find the odd:|a:Yen,b:Dollar,c:Rubie,d:Pound,e:Palsa|e|Palsa is not a currency.
Q82|Complete the series: 51, 60, 52, 59, 53, ___, ___|a:50 54,b:58 56,c:54 59,d:58 54,e:104 25|d|Two interleaved: 51 52 53 54 and 60 59 58.
Q83|Pleased is to depressed as Straight is to ___?|a:Line,b:Curved,c:Vertical,d:Horizontal,e:Smooth|b|Curved is opposite of straight.
Q84|I, X, 4, V, 9, T, 16, R, ___, ___|a:P 24,b:28 Q,c:25 P,d:27 S,e:24 R|c|Pattern with squares and letters: next 25 P.
Q85|Candle is to sun as ___ is to Ocean.|a:Fish,b:Boat,c:Pond,d:Sea,e:River|c|Candle is small light vs sun; pond is small water vs ocean.
Q86|Which pair has no relation?|a:Petrol & Diesel,b:Legs & Wheel,c:Diesel & Cart,d:Smoke & CO2,e:Tree & wood|c|Diesel and Cart are not source-product.
Q87|A tuber is the thickened part of an underground stem of a plant|a:Sweet Potato,b:Arum,c:Dahlia,d:Both B&C,e:Both A&C|e|Sweet potato and dahlia are tubers.
Q88|Cow is to milk as Tree is to ___?|a:Leaves,b:Root,c:Wood,d:Fruits,e:Branches|d|A cow produces milk; a tree produces fruits.
Q89|Diligence is the mother of good luck. The statement is True or false.|a:True,b:False,c:N/A,d:None,e:ALL|a|It is a proverb meaning hard work leads to success.
Q90|Example is better than law, ___?|a:True,b:False,c:N/A,d:None,e:ALL|a|Leading by example is more effective than rules.
Q91|Good wine needs no bush. The statement is True or false?|a:True,b:False,c:N/A,d:None|a|It is a proverb meaning quality needs no advertising.
Q92|Male is to Mall as Hale is to ___?|a:Hat,b:Bella,c:Tell,d:Hell,e:Hall|e|Male → Mall changes last letter; Hale → Hall.
Q93|Complete the series 15, 26, 20, 30, 25, 35, ___, ___|a:30 41,b:30 42,c:32 41,d:42 30,e:25 41|a|Two interleaved: 15 20 25 30 and 26 30 35 41.
Q94|Seed is to Speed as send is to ___?|a:Dense,b:Stend,c:Spand,d:Spend,e:Sand|d|Adding p to seed makes speed; adding p to send makes spend.
Q95|Complete the series: 81, 69, 58, 48, 39, ___, ___|a:28 35,b:31 24,c:31 23,d:23 33,e:32 24|b|Subtract decreasing: -12 -11 -10 -9 so next -8 = 31 then -7 = 24.
"""

def parse_and_create_set6():
    """Parse compact question data and create Set 6."""
    
    # Create or get Set 6
    set6, created = Test.objects.get_or_create(
        name="IQ Test - Set 6",
        defaults={
            "duration_minutes": 30,
            "total_questions": 95,  # Actual count from provided data
            "price": 0.00,
            "is_free_sample": False,
            "is_bank": False,
            "is_active": True
        }
    )
    
    if created:
        print(f"✓ Created {set6.name}")
    else:
        print(f"✓ {set6.name} already exists. Clearing existing questions...")
        Question.objects.filter(test=set6).delete()
    
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
            test=set6,
            question_text=text,
            question_type='mcq',
            options=options,
            correct_answer=correct,
            explanation=explanation,
            difficulty_level='medium',
            order=idx,
            bank_order=500 + idx
        )
        
        if idx % 10 == 0:
            print(f"  Created {idx} questions...")
    
    # Update total_questions to actual count
    set6.total_questions = len(lines)
    set6.save()
    
    print(f"\n✓ Successfully created {len(lines)} questions for {set6.name}!")
    print(f"  Total questions in database: {Question.objects.filter(test=set6).count()}")
    
    return set6

if __name__ == "__main__":
    parse_and_create_set6()
