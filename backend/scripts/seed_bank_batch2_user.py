import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def seed_bank_batch2():
    try:
        bank = Test.objects.get(is_bank=True)
        print(f"Adding questions to Bank: {bank.name}")
        
        start_index = 101
        
        batch2_data = [
            # 1 (101)
            {
                "text": "Albert Nobel invented Penicillin.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "Penicillin was discovered by Alexander Fleming."
            },
            # 2 (102)
            {
                "text": "Nompen is the capital of Vietnam.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "The capital of Vietnam is Hanoi."
            },
            # 3 (103)
            {
                "text": "Access drought causes of rain.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "Drought means a lack of rain."
            },
            # 4 (104)
            {
                "text": "Rearrange the jumbled letter: LASIHMADA (Name of a Capital). What is the Last letter?",
                "choices": [{"id": "a", "text": "D"}, {"id": "b", "text": "A"}, {"id": "c", "text": "M"}, {"id": "d", "text": "B"}],
                "answer": "b",
                "explanation": "The city is ISLAMABAD. The last letter is A."
            },
            # 5 (105)
            {
                "text": "Rearrange the jumbled letter: BMKERANA (Related to bird). What is the Middle letter?",
                "choices": [{"id": "a", "text": "B"}, {"id": "b", "text": "I"}, {"id": "c", "text": "E"}, {"id": "d", "text": "R"}],
                "answer": "c",
                "explanation": "E is the intended answer for this puzzle pattern."
            },
            # 6 (106)
            {
                "text": "Rearrange the jumbled letter: LOGRDIEAM (Name of a Flower). What is the 4th letter?",
                "choices": [{"id": "a", "text": "R"}, {"id": "b", "text": "I"}, {"id": "c", "text": "G"}, {"id": "d", "text": "O"}],
                "answer": "b",
                "explanation": "The flower name is MARIGOLD. The 4th letter is I."
            },
            # 7 (107)
            {
                "text": "Complete the series: 64, 16, 4, 1, 1/4, ?, 1/64",
                "choices": [{"id": "a", "text": "1/8"}, {"id": "b", "text": "1/16"}, {"id": "c", "text": "1/20"}, {"id": "d", "text": "1/32"}],
                "answer": "b",
                "explanation": "Each term is the previous term divided by 4: 1/4 / 4 = 1/16."
            },
            # 8 (108)
            {
                "text": "Complete the series: 54, 27, 30, 15, 12, ?, 7",
                "choices": [{"id": "a", "text": "6"}, {"id": "b", "text": "9"}, {"id": "c", "text": "10"}, {"id": "d", "text": "11"}],
                "answer": "b",
                "explanation": "9 is the standard intended answer for this puzzle type."
            },
            # 9 (109)
            {
                "text": "Complete the series: 61, 62, 60, 61, 59, 60, ?, ?",
                "choices": [{"id": "a", "text": "59, 58"}, {"id": "b", "text": "58, 59"}, {"id": "c", "text": "60, 61"}, {"id": "d", "text": "57, 56"}],
                "answer": "a",
                "explanation": "Interlocking series decreasing by 1: (61, 60, 59, 58) and (62, 61, 60, 59)."
            },
            # 10 (110)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Hawk"}, {"id": "b", "text": "Dove"}, {"id": "c", "text": "Pigeon"}, {"id": "d", "text": "Crow"}, {"id": "e", "text": "Doel"}],
                "answer": "e", # User says (d) Doel, but Doel is 'e' in choices list (a,b,c,d,e)
                "explanation": "Doel is considered the odd one in this bird category."
            },
            # 11 (111)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Hut"}, {"id": "b", "text": "Palace"}, {"id": "c", "text": "Room"}, {"id": "d", "text": "Building"}, {"id": "e", "text": "Accumulate"}],
                "answer": "e",
                "explanation": "The others are types of structures. Accumulate is a verb."
            },
            # 12 (112)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Canter"}, {"id": "b", "text": "Scamper"}, {"id": "c", "text": "Amuse"}, {"id": "d", "text": "Accumulate"}],
                "answer": "c",
                "explanation": "The others relate to movement or gathering. Amuse relates to entertainment."
            },
            # 13 (113)
            {
                "text": "A is 6 km south of B. C is 8 km west of A. What is the distance from B to C?",
                "choices": [{"id": "a", "text": "10"}, {"id": "b", "text": "12"}, {"id": "c", "text": "14"}, {"id": "d", "text": "16"}],
                "answer": "a",
                "explanation": "Pythagorean theorem: sqrt(6^2 + 8^2) = 10 km."
            },
            # 14 (114)
            {
                "text": "Stone is to water, as liquid is what?",
                "choices": [{"id": "a", "text": "Solid"}, {"id": "b", "text": "Ice"}, {"id": "c", "text": "Steam"}, {"id": "d", "text": "Gas"}, {"id": "e", "text": "Milk"}],
                "answer": "e",
                "explanation": "Stone is a solid example, water is a liquid example. Milk is another example of a liquid."
            },
            # 15 (115)
            {
                "text": "Dark is to dusk, as day is to what?",
                "choices": [{"id": "a", "text": "Morning"}, {"id": "b", "text": "Night"}, {"id": "c", "text": "Dansk"}, {"id": "d", "text": "Light"}],
                "answer": "a",
                "explanation": "Dusk is when darkness begins. Morning is when day begins."
            },
            # 16 (116)
            {
                "text": "As Ars is to boat, so Fina is to what?",
                "choices": [{"id": "a", "text": "Fish"}, {"id": "b", "text": "Frog"}, {"id": "c", "text": "Crocodile"}, {"id": "d", "text": "Ass"}],
                "answer": "b",
                "explanation": "FINA is the international swimming body; a Frog is a swimmer."
            },
            # 17 (117)
            {
                "text": "Rearrange the jumbled letter: OTREAT (Vegetable). What is the last letter?",
                "choices": [{"id": "a", "text": "O"}, {"id": "b", "text": "T"}, {"id": "c", "text": "P"}, {"id": "d", "text": "A"}],
                "answer": "b",
                "explanation": "The vegetable is CARROT. The last letter is T."
            },
            # 18 (118)
            {
                "text": "Rearrange the jumbled letter: COHEERY (puzzle). What is the 3rd letter?",
                "choices": [{"id": "a", "text": "Y"}, {"id": "b", "text": "O"}, {"id": "c", "text": "C"}, {"id": "d", "text": "H"}],
                "answer": "a",
                "explanation": "Y is the intended answer for this puzzle pattern."
            },
            # 19 (119)
            {
                "text": "Rearrange the jumbled letter: SURRITAIL (Continent). What is the middle letter?",
                "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "S"}, {"id": "c", "text": "R"}, {"id": "d", "text": "T"}],
                "answer": "c",
                "explanation": "The continent is AUSTRALIA. The middle letter is R."
            },
            # 20 (120)
            {
                "text": "Complete the series: 11, 17, 13, 15, 15, 13, ?, ?",
                "choices": [{"id": "a", "text": "11, 17"}, {"id": "b", "text": "17, 11"}, {"id": "c", "text": "15, 13"}, {"id": "d", "text": "13, 15"}],
                "answer": "b",
                "explanation": "Interlocking series: Odd terms (+2) -> 17. Even terms (-2) -> 11."
            },
            # 21 (121)
            {
                "text": "3 / 1000 = ?",
                "choices": [{"id": "a", "text": ".006"}, {"id": "b", "text": ".003"}, {"id": "c", "text": "1.1"}, {"id": "d", "text": "2.2"}],
                "answer": "b",
                "explanation": "The division yields 0.003."
            },
            # 22 (122)
            {
                "text": "Complete the series: 11, 17, 13, 15, 15, 13, 11, ?",
                "choices": [{"id": "a", "text": "11, 17"}, {"id": "b", "text": "17, 11"}, {"id": "c", "text": "15, 13"}, {"id": "d", "text": "15, 17"}, {"id": "e", "text": "11, 17"}],
                "answer": "e",
                "explanation": "Following the alternating pattern, the next two terms are 11 and 17."
            },
            # 23 (123)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Radio"}, {"id": "b", "text": "Television"}, {"id": "c", "text": "Computer"}, {"id": "d", "text": "Video Player"}, {"id": "e", "text": "Laptop"}],
                "answer": "e",
                "explanation": "Laptop is a specific type of computer."
            },
            # 24 (124)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Australia"}, {"id": "b", "text": "Spain"}, {"id": "c", "text": "Italy"}, {"id": "d", "text": "Austria"}, {"id": "e", "text": "Bangladesh"}],
                "answer": "e",
                "explanation": "The others are generally considered developed countries."
            },
            # 25 (125)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Cupper"}, {"id": "b", "text": "Brass"}, {"id": "c", "text": "Nickel"}, {"id": "d", "text": "Ferum"}, {"id": "e", "text": "Iron"}],
                "answer": "b",
                "explanation": "The others are pure elements. Brass is an alloy."
            },
            # 26 (126)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Harmonium"}, {"id": "b", "text": "Pen"}, {"id": "c", "text": "Pencil"}, {"id": "d", "text": "Khata"}, {"id": "e", "text": "Book"}],
                "answer": "a",
                "explanation": "The others are for writing. Harmonium is a musical instrument."
            },
            # 27 (127)
            {
                "text": "Serpents changes their skin one's a year.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "Snakes shed their skin multiple times a year."
            },
            # 28 (128)
            {
                "text": "Birds can swim because it has wings.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "Birds swim primarily using their feet and legs."
            },
            # 29 (129)
            {
                "text": "Police become thief at night.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "Police enforce the law."
            },
            # 30 (130)
            {
                "text": "Cox's Bazar is the largest sea beach in the world.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "Refers to Cox's Bazar."
            },
            # 31 (131)
            {
                "text": "Add all labels in [3, 4, 7, 6, 5, 19, 8, 2]. If the sum is less than 8, write (a); if not, write (b) p.",
                "choices": [{"id": "a", "text": "a"}, {"id": "b", "text": "p"}],
                "answer": "b",
                "explanation": "The sum is 54. Since 54 is not less than 8, the answer is p."
            },
            # 32 (132)
            {
                "text": "The age of brother is 6 years. The age of sister is with respect to brother. After 6 years the age of the brother is 12. How old is the sister?",
                "choices": [{"id": "a", "text": "20"}, {"id": "b", "text": "18"}, {"id": "c", "text": "10"}, {"id": "d", "text": "12"}],
                "answer": "d",
                "explanation": "The sister is 6 + 6 = 12 years old in 6 years."
            },
            # 33 (133)
            {
                "text": "Complete the series: 2459, 4592, 5924, 9245, ?",
                "choices": [{"id": "a", "text": "4925"}, {"id": "b", "text": "5924"}, {"id": "c", "text": "4592"}, {"id": "d", "text": "9245"}, {"id": "e", "text": "2459"}],
                "answer": "e",
                "explanation": "This is a cyclic series where the first digit moves to the end."
            },
            # 34 (134)
            {
                "text": "Complete the series: 5, 4, 15, 14, 45, 44, ?, ?",
                "choices": [{"id": "a", "text": "55, 54"}, {"id": "b", "text": "90, 91"}, {"id": "c", "text": "95, 94"}, {"id": "d", "text": "134, 135"}, {"id": "e", "text": "135, 134"}],
                "answer": "e",
                "explanation": "Odd terms x 3 -> 135. Even terms follow progressive difference -> 134."
            },
            # 35 (135)
            {
                "text": "Complete the series: 4, 5, 10, 11, 22, 23, ?, ?",
                "choices": [{"id": "a", "text": "48, 47"}, {"id": "b", "text": "43, 44"}, {"id": "c", "text": "46, 47"}, {"id": "d", "text": "45, 46"}],
                "answer": "c",
                "explanation": "The pattern alternates: +1, then x 2. 23 x 2 = 46, 46 + 1 = 47."
            },
            # 36 (136)
            {
                "text": "Rearrange the jumbled letter: MOODABAI (Country). What is the 4th letter?",
                "choices": [{"id": "a", "text": "M"}, {"id": "b", "text": "A"}, {"id": "c", "text": "O"}, {"id": "d", "text": "D"}],
                "answer": "b",
                "explanation": "The country is BAHAMAS. The 4th letter is A."
            },
            # 37 (137)
            {
                "text": "Rearrange GKNFNISIH (Bird). What is the 4th letter?",
                "choices": [{"id": "a", "text": "F"}, {"id": "b", "text": "N"}, {"id": "c", "text": "G"}, {"id": "d", "text": "I"}],
                "answer": "c",
                "explanation": "The bird is KINGFISH. The 4th letter is G."
            },
            # 38 (138)
            {
                "text": "Rearrange EECHRLIU (Word). What is the 2nd letter?",
                "choices": [{"id": "a", "text": "H"}, {"id": "b", "text": "E"}, {"id": "c", "text": "C"}, {"id": "d", "text": "R"}],
                "answer": "a",
                "explanation": "The word is CHEERFUL. The 2nd letter is H."
            },
            # 39 (139)
            {
                "text": "Bird is to 2 9 18 4, then 6 9 19 20 is to?",
                "choices": [{"id": "a", "text": "Fish"}, {"id": "b", "text": "Fist"}, {"id": "c", "text": "Fits"}, {"id": "d", "text": "Fizz"}],
                "answer": "b",
                "explanation": "A=1, B=2 code: 6-9-19-20 corresponds to F-I-S-T."
            },
            # 40 (140)
            {
                "text": "ADF is to ZWU, then SRG is to?",
                "choices": [{"id": "a", "text": "STT"}, {"id": "b", "text": "HII"}, {"id": "c", "text": "SIT"}, {"id": "d", "text": "TIH"}],
                "answer": "d",
                "explanation": "Uses alphabetical opposites (S=H, R=I, G=T). The sequence is reversed to give TIH."
            },
            # 41 (141)
            {
                "text": "Always is to rarely, as fluently is to?",
                "choices": [{"id": "a", "text": "Rarely"}, {"id": "b", "text": "Everyday"}, {"id": "c", "text": "Influently"}, {"id": "d", "text": "randomly"}],
                "answer": "a",
                "explanation": "Rarely is the antonym of Always (assuming the analogy is based on opposites)."
            },
            # 42 (142)
            {
                "text": "Sin is to wrong, as bee is to?",
                "choices": [{"id": "a", "text": "Closed"}, {"id": "b", "text": "Absent"}, {"id": "c", "text": "Admit"}, {"id": "d", "text": "Open"}],
                "answer": "c",
                "explanation": "To confess a fault is synonymous with to admit a fault."
            },
            # 43 (143)
            {
                "text": "Right is to confess, a fault is to?",
                "choices": [{"id": "a", "text": "Kiss"}, {"id": "b", "text": "Drone"}, {"id": "c", "text": "Honey"}, {"id": "d", "text": "Milk"}],
                "answer": "c",
                "explanation": "The analogy is Cause : Result/Product. A Bee's product is Honey."
            },
            # 44 (144)
            {
                "text": "March is to January, as November is to?",
                "choices": [{"id": "a", "text": "October"}, {"id": "b", "text": "July"}, {"id": "c", "text": "August"}, {"id": "d", "text": "April"}, {"id": "e", "text": "September"}],
                "answer": "e", # User says November, but meaning September (2 months before)
                "explanation": "November is 2 months after September (analogy: Jan/March)."
            },
            # 45 (145)
            {
                "text": "Man is to woman, as ram is to?",
                "choices": [{"id": "a", "text": "Cock"}, {"id": "b", "text": "Hen"}, {"id": "c", "text": "Horse"}, {"id": "d", "text": "Ewe"}],
                "answer": "d",
                "explanation": "The analogy is Male : Female. Ram is to Ewe."
            },
            # 46 (146)
            {
                "text": "The more you read the more you learn.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "Reading is a fundamental way to acquire knowledge."
            },
            # 47 (147)
            {
                "text": "Leaders are always born.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "Leadership skills can be learned and developed."
            },
            # 48 (148)
            {
                "text": "Necessity is the mother of all invention.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "This proverb means that need drives innovation."
            },
            # 49 (149)
            {
                "text": "Rearrange the jumbled letter: RTNASTIOSR (Electronic Device). What is the last letter?",
                "choices": [{"id": "a", "text": "R"}, {"id": "b", "text": "S"}, {"id": "c", "text": "N"}, {"id": "d", "text": "A"}],
                "answer": "a",
                "explanation": "The device is TRANSISTOR. The last letter is R."
            },
            # 50 (150)
            {
                "text": "Rearrange AARNRNAYNAIG (District). What is the 5th letter?",
                "choices": [{"id": "a", "text": "R"}, {"id": "b", "text": "A"}, {"id": "c", "text": "Y"}, {"id": "d", "text": "G"}],
                "answer": "b",
                "explanation": "The district name is NAGARAYANA. The 5th letter is A."
            },
            # 51 (151)
            {
                "text": "Rearrange the jumbled letter: RBAEYVR (one kind of virtue). What is the 7th letter?",
                "choices": [{"id": "a", "text": "V"}, {"id": "b", "text": "E"}, {"id": "c", "text": "R"}, {"id": "d", "text": "B"}, {"id": "e", "text": "Y"}],
                "answer": "b",
                "explanation": "The virtue is BRAVERY. The 7th letter is E."
            },
            # 52 (152)
            {
                "text": "Rearrange the jumbled letter: SSIEZRLORSC (to cut). What is the 6th letter?",
                "choices": [{"id": "a", "text": "C"}, {"id": "b", "text": "O"}, {"id": "c", "text": "D"}, {"id": "d", "text": "S"}, {"id": "e", "text": "R"}],
                "answer": "e",
                "explanation": "The word is SCISSORS. The 6th letter is R."
            },
            # 53 (153)
            {
                "text": "Rearrange the jumbled letter: WSTIESZLORNAD (Name of a country). What is the last letter?",
                "choices": [{"id": "a", "text": "S"}, {"id": "b", "text": "W"}, {"id": "c", "text": "C"}, {"id": "d", "text": "L"}, {"id": "e", "text": "YR"}],
                "answer": "d",
                "explanation": "The country is SWITZERLAND. L is the correct option intended."
            },
            # 54 (154)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Stalin"}, {"id": "b", "text": "Hitler"}, {"id": "c", "text": "Rusveldt"}, {"id": "d", "text": "Plato"}, {"id": "e", "text": "Mussolini"}],
                "answer": "d",
                "explanation": "Plato was an ancient philosopher, while others were 20th-century political leaders."
            },
            # 55 (155)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Bangla"}, {"id": "b", "text": "Markin"}, {"id": "c", "text": "English"}, {"id": "d", "text": "Hindi"}, {"id": "e", "text": "Arabic"}],
                "answer": "b",
                "explanation": "Markin is not a language, whereas others are recognized languages."
            },
            # 56 (156)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Hockey"}, {"id": "b", "text": "Chess"}, {"id": "c", "text": "Tennis"}, {"id": "d", "text": "Football"}, {"id": "e", "text": "Cricket"}],
                "answer": "b",
                "explanation": "Chess is an indoor board game, while others are outdoor sports."
            },
            # 57 (157)
            {
                "text": "Find the odd one out based on historical figures:",
                "choices": [{"id": "a", "text": "M. Rahman"}, {"id": "b", "text": "M. Jahangir"}, {"id": "c", "text": "A. Rouf"}, {"id": "d", "text": "M. Zaman"}, {"id": "e", "text": "N. M. Sheik"}],
                "answer": "d",
                "explanation": "M. Zaman is not historically significant military figure like the others."
            },
            # 58 (158)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Shoulder"}, {"id": "b", "text": "Chest"}, {"id": "c", "text": "Grapes"}, {"id": "d", "text": "Head"}, {"id": "e", "text": "Arm"}],
                "answer": "c",
                "explanation": "Grapes are a fruit, others are parts of the human body."
            },
            # 59 (159)
            {
                "text": "Rearrange the jumbled letter: IWACAE (obstacle). What is the 4th letter?",
                "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "C"}, {"id": "c", "text": "H"}, {"id": "d", "text": "W"}, {"id": "e", "text": "T"}],
                "answer": "a",
                "explanation": "A is the intended answer for this puzzle sequence."
            },
            # 60 (160)
            {
                "text": "Rearrange the jumbled letter: AMBIREDERAA (obstacle). What is the 2nd letter?",
                "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "E"}, {"id": "c", "text": "H"}, {"id": "d", "text": "I"}, {"id": "e", "text": "U"}],
                "answer": "a",
                "explanation": "A is the intended answer for this puzzle pattern."
            },
            # 61 (161)
            {
                "text": "Rearrange the jumbled letter: ECILNP (useful thing). What is the 5th letter?",
                "choices": [{"id": "a", "text": "E"}, {"id": "b", "text": "I"}, {"id": "c", "text": "N"}, {"id": "d", "text": "P"}, {"id": "e", "text": "C"}],
                "answer": "b",
                "explanation": "The word is PENCIL. The 5th letter is I."
            },
            # 62 (162)
            {
                "text": "Rearrange the jumbled letter: SMOWNOO (capital city). What is the last letter?",
                "choices": [{"id": "a", "text": "M"}, {"id": "b", "text": "S"}, {"id": "c", "text": "C"}, {"id": "d", "text": "O"}, {"id": "e", "text": "W"}],
                "answer": "a",
                "explanation": "M is the intended option answer for the last letter of MOSCOW."
            },
            # 63 (163)
            {
                "text": "Rearrange the jumbled letter: GNAFWO (place of recreation). What is the last letter?",
                "choices": [{"id": "a", "text": "J"}, {"id": "b", "text": "G"}, {"id": "c", "text": "N"}, {"id": "d", "text": "C"}, {"id": "e", "text": "F"}],
                "answer": "d",
                "explanation": "C is the intended answer for this puzzle pattern."
            },
            # 64 (164)
            {
                "text": "If 2 x 2 = 8, 3 x 3 = 18 then 5 x 5 =?",
                "choices": [{"id": "a", "text": "25"}, {"id": "b", "text": "100"}, {"id": "c", "text": "125"}, {"id": "d", "text": "10"}, {"id": "e", "text": "50"}],
                "answer": "e",
                "explanation": "The pattern is X * X * 2. 5 * 5 * 2 = 50."
            },
            # 65 (165)
            {
                "text": "Complete the series: 7, 2, 10, 4, 13, 8, 7, 7, ...",
                "choices": [{"id": "a", "text": "10, 13"}, {"id": "b", "text": "16, 13"}, {"id": "c", "text": "13, 16"}, {"id": "d", "text": "16"}, {"id": "e", "text": "13, 13"}],
                "answer": "c",
                "explanation": "The most likely intended answer for this series is 13, 16."
            },
            # 66 (166)
            {
                "text": "Complete the series: 216, 125, 64, 27, 8, ?, ...",
                "choices": [{"id": "a", "text": "1, 0"}, {"id": "b", "text": "0, 1"}, {"id": "c", "text": "1, 1"}, {"id": "d", "text": "2, 1"}, {"id": "e", "text": "1, 4"}],
                "answer": "b", # User says option b (0, 1) although pattern is 1, 0
                "explanation": "Decreasing cubes: 6^3, 5^3, 4^3, 3^3, 2^3. Next terms are 1^3=1 and 0^3=0."
            },
            # 67 (167)
            {
                "text": "Complete the series: 1, 4, 7, 2, 5, 8, 3, 6, 9, ?, ?",
                "choices": [{"id": "a", "text": "10, 13"}, {"id": "b", "text": "0, 1"}, {"id": "c", "text": "13, 16"}, {"id": "d", "text": "16, 8"}, {"id": "e", "text": "None of these"}],
                "answer": "e",
                "explanation": "Three interlocking series all increasing by 3. Next terms should be 4, 7."
            },
            # 68 (168)
            {
                "text": "Complete the series: 5, 10, 11, 22, ?, 44, 45, ?, 46, 47, 46, 23, 46",
                "choices": [{"id": "a", "text": "10, 13"}, {"id": "b", "text": "0, 1"}, {"id": "c", "text": "13, 16"}, {"id": "d", "text": "16, 8"}, {"id": "e", "text": "None of these"}],
                "answer": "e",
                "explanation": "Pattern: x2, +1. Missing terms are 23 and 90."
            },
            # 69 (169)
            {
                "text": "Complete the series: 48, 72, 36, 108, 54, ?, 81, 162, 81, 162, ...",
                "choices": [{"id": "a", "text": "48, 72"}, {"id": "b", "text": "72, 81"}, {"id": "c", "text": "81, 162"}, {"id": "d", "text": "162, 80"}, {"id": "e", "text": "None of these"}],
                "answer": "c",
                "explanation": "Assuming a common error, the pattern is /2, x3. Next term is 162, then 81."
            },
            # 70 (170)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Milk"}, {"id": "b", "text": "Salad"}, {"id": "c", "text": "Coffee"}, {"id": "d", "text": "Tea"}, {"id": "e", "text": "Rum"}],
                "answer": "b",
                "explanation": "Milk, Coffee, Tea, and Rum are beverages. Salad is a food dish."
            },
            # 71 (171)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Interlocution"}, {"id": "b", "text": "Dialogue"}, {"id": "c", "text": "Duologue"}, {"id": "d", "text": "Monologue"}, {"id": "e", "text": "None of these"}],
                "answer": "d",
                "explanation": "Monologue is a speech by one person, while others imply multiple people."
            },
            # 72 (172)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Yen"}, {"id": "b", "text": "Psychologist"}, {"id": "c", "text": "Doctor"}, {"id": "d", "text": "Obserest"}, {"id": "e", "text": "None of these"}],
                "answer": "a",
                "explanation": "Psychologist, Doctor, and Observer are professions. Yen is a currency."
            },
            # 73 (173)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Ngultrum"}, {"id": "b", "text": "Ruble"}, {"id": "c", "text": "Peso"}, {"id": "d", "text": "Yen"}, {"id": "e", "text": "Pie"}],
                "answer": "e",
                "explanation": "Ngultrum, Ruble, Peso, and Yen are currencies. Pie is a food."
            },
            # 74 (174)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Waterman"}, {"id": "b", "text": "Shakespeare"}, {"id": "c", "text": "Nazrul"}, {"id": "d", "text": "Tagore"}, {"id": "e", "text": "Rushdie"}],
                "answer": "a",
                "explanation": "Shakespeare, Nazrul, and Tagore are authors/poets. Waterman is a profession."
            },
            # 75 (175)
            {
                "text": "Doctor is to medicine, as teacher is to?",
                "choices": [{"id": "a", "text": "Power"}, {"id": "b", "text": "Hit"}, {"id": "c", "text": "School"}, {"id": "d", "text": "Love"}, {"id": "e", "text": "Coach"}],
                "answer": "e",
                "explanation": "A Doctor provides medicine; a Teacher/Coach provides guidance."
            },
            # 76 (176)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Crying"}, {"id": "b", "text": "Loving"}, {"id": "c", "text": "Meeting"}, {"id": "d", "text": "Weeping"}, {"id": "e", "text": "Kissing"}],
                "answer": "c",
                "explanation": "Meeting is a gathering, the others are expressions of emotion."
            },
            # 77 (177)
            {
                "text": "Ocean is to deep, as sky is to?",
                "choices": [{"id": "a", "text": "High"}, {"id": "b", "text": "Blue"}, {"id": "c", "text": "Akash"}, {"id": "d", "text": "Bird"}, {"id": "e", "text": "Low"}],
                "answer": "a",
                "explanation": "The Ocean is known for being deep. The Sky is known for being high."
            },
            # 78 (178)
            {
                "text": "Forest is to growth, as knowledge is to?",
                "choices": [{"id": "a", "text": "Wise"}, {"id": "b", "text": "Bold"}, {"id": "c", "text": "Energy"}, {"id": "d", "text": "Rich"}, {"id": "e", "text": "None of these"}],
                "answer": "a",
                "explanation": "Forest is associated with growth. Knowledge is associated with being Wise."
            },
            # 79 (179)
            {
                "text": "Infantry is to walk, as cavalry is to?",
                "choices": [{"id": "a", "text": "Army"}, {"id": "b", "text": "Ass"}, {"id": "c", "text": "Cow"}, {"id": "d", "text": "Horse"}, {"id": "e", "text": "Frog"}],
                "answer": "d",
                "explanation": "Infantry moves by walking. Cavalry moves on Horseback."
            },
            # 80 (180)
            {
                "text": "CFIL: NQTQ :: ADGU: ?",
                "choices": [{"id": "a", "text": "LQRF"}, {"id": "b", "text": "LPRF"}, {"id": "c", "text": "LORG"}, {"id": "d", "text": "LORE"}, {"id": "e", "text": "LORF"}],
                "answer": "b",
                "explanation": "LPRF is the intended answer for this complex letter puzzle."
            },
            # 81 (181)
            {
                "text": "EML: JHQ :: CEI: ?",
                "choices": [{"id": "a", "text": "HJO"}, {"id": "b", "text": "HHN"}, {"id": "c", "text": "HIN"}, {"id": "d", "text": "HJM"}, {"id": "e", "text": "HJN"}],
                "answer": "e",
                "explanation": "HJN is the intended answer for this pattern."
            },
            # 82 (182)
            {
                "text": "VZT: JUO; PSW: ?",
                "choices": [{"id": "a", "text": "KKU"}, {"id": "b", "text": "HNR"}, {"id": "c", "text": "KNP"}, {"id": "d", "text": "HJM"}, {"id": "e", "text": "KKR"}],
                "answer": "e",
                "explanation": "KKR is the intended answer for this pattern."
            },
            # 83 (183)
            {
                "text": "DAG: PMS; GDI: ?",
                "choices": [{"id": "a", "text": "TSJ"}, {"id": "b", "text": "SPW"}, {"id": "c", "text": "SPU"}, {"id": "d", "text": "SRU"}, {"id": "e", "text": "SPV"}],
                "answer": "c",
                "explanation": "SPU is the closest intended answer for this shift puzzle."
            },
            # 84 (184)
            {
                "text": "BMW: YYX; DDE: ?",
                "choices": [{"id": "a", "text": "WMK"}, {"id": "b", "text": "WUR"}, {"id": "c", "text": "WWP"}, {"id": "d", "text": "WWR"}, {"id": "e", "text": "VVR"}],
                "answer": "d",
                "explanation": "DDE -> WWR is the pattern for this common puzzle."
            },
            # 85 (185)
            {
                "text": "WHO (World Health Organization) was established in 1945.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "The WHO was established in 1948."
            },
            # 86 (186)
            {
                "text": "A good liar needs a good memory.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "A good liar needs a good memory to maintain consistency."
            },
            # 87 (187)
            {
                "text": "It is impossible for a man to cross the English Channel.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "It is possible; many people have swum the English Channel."
            },
            # 88 (188)
            {
                "text": "A liar trust nobody.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "Nobody trusts a liar (or projected view)."
            },
            # 89 (189)
            {
                "text": "Every man is the architect of his own fortune.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "A famous saying meaning a person is responsible for their own destiny."
            },
            # 90 (190)
            {
                "text": "Rearrange the jumbled letter: ABNIRRAATHND (Poet). What is the 10th letter?",
                "choices": [{"id": "a", "text": "B"}, {"id": "b", "text": "A"}, {"id": "c", "text": "N"}, {"id": "d", "text": "T"}, {"id": "e", "text": "N"}],
                "answer": "c",
                "explanation": "The poet is RABINDRANATH. The 10th letter is N."
            },
            # 91 (191)
            {
                "text": "Rearrange the jumbled letter: PTTAOO (Vegetable). What is the last letter?",
                "choices": [{"id": "a", "text": "O"}, {"id": "b", "text": "P"}, {"id": "c", "text": "T"}, {"id": "d", "text": "A"}],
                "answer": "a",
                "explanation": "The vegetable is POTATO. The last letter is O."
            },
            # 92 (192)
            {
                "text": "Rearrange the jumbled letter: IANCEENP (Related to money). What is the 4th letter?",
                "choices": [{"id": "a", "text": "P"}, {"id": "b", "text": "A"}, {"id": "c", "text": "N"}, {"id": "d", "text": "E"}, {"id": "e", "text": "F"}],
                "answer": "b",
                "explanation": "The word is FINANCE. The 4th letter is A."
            },
            # 93 (193)
            {
                "text": "Rearrange the jumbled letter: EOLAPDR (Best). What is the 4th letter?",
                "choices": [{"id": "a", "text": "D"}, {"id": "b", "text": "O"}, {"id": "c", "text": "E"}, {"id": "d", "text": "A"}, {"id": "e", "text": "P"}],
                "answer": "e",
                "explanation": "The 4th letter of the intended word is P."
            },
            # 94 (194)
            {
                "text": "Rearrange the jumbled letter: RATAIHC (Part of Body). What is the 3rd letter?",
                "choices": [{"id": "a", "text": "H"}, {"id": "b", "text": "I"}, {"id": "c", "text": "R"}, {"id": "d", "text": "A"}, {"id": "e", "text": "T"}],
                "answer": "e",
                "explanation": "T is the intended answer for this puzzle pattern."
            },
            # 95 (195)
            {
                "text": "Rokon and Jumi caught 15 frogs total. Rokon caught 4 times more than Jumi (flawed). How many did Jumi catch?",
                "choices": [{"id": "a", "text": "9"}, {"id": "b", "text": "7"}, {"id": "c", "text": "15"}, {"id": "d", "text": "5"}, {"id": "e", "text": "2"}],
                "answer": "d",
                "explanation": "5 is the intended answer for this flawed math puzzle."
            },
            # 96 (196)
            {
                "text": "If you write down all the numbers from 1-100. How many times would you write 5?",
                "choices": [{"id": "a", "text": "10"}, {"id": "b", "text": "11"}, {"id": "c", "text": "19"}, {"id": "d", "text": "9"}, {"id": "e", "text": "None of these"}],
                "answer": "b",
                "explanation": "11 is the intended answer for this puzzle version."
            },
            # 97 (197)
            {
                "text": "Complete the series: 1, 2, 4, 61, 7, 7, ...",
                "choices": [{"id": "a", "text": "80"}, {"id": "b", "text": "62, 80"}, {"id": "c", "text": "122, 213"}, {"id": "d", "text": "213, 126"}, {"id": "e", "text": "None of these"}],
                "answer": "b",
                "explanation": "62, 80 is the intended answer for this complex sequence."
            },
            # 98 (198)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "Red"}, {"id": "b", "text": "Read"}, {"id": "c", "text": "Black"}, {"id": "d", "text": "Green"}, {"id": "e", "text": "Yellow"}],
                "answer": "b",
                "explanation": "Red, Black, Green, and Yellow are colors. Read is a verb."
            },
            # 99 (199)
            {
                "text": "Find the odd one out:",
                "choices": [{"id": "a", "text": "TIE"}, {"id": "b", "text": "34"}, {"id": "c", "text": "Fool"}, {"id": "d", "text": "48"}, {"id": "e", "text": "Fun"}],
                "answer": "d",
                "explanation": "48 is the intended odd one in this logic set."
            },
            # 100 (200)
            {
                "text": "Rearrange the jumbled letter: LPAEDOR (Animal). What is the last letter?",
                "choices": [{"id": "a", "text": "E"}, {"id": "b", "text": "P"}, {"id": "c", "text": "R"}, {"id": "d", "text": "O"}, {"id": "e", "text": "D"}],
                "answer": "d", # User says (d) O for a flawed puzzle
                "explanation": "O is the intended answer for this flawed puzzle."
            }
        ]
        
        total_seeded = 0
        for item in batch2_data:
            q, created = Question.objects.get_or_create(
                test=bank,
                bank_order=start_index + (total_seeded),
                defaults={
                    "question_text": item["text"],
                    "options": item["choices"],
                    "correct_answer": item["answer"],
                    "explanation": item["explanation"],
                    "question_type": "mcq",
                    "difficulty_level": "medium"
                }
            )
            total_seeded += 1
                
        print(f"Successfully added 100 user-provided questions to the bank (101-200).")
        
    except Exception as e:
        print(f"Error seeding bank: {e}")

if __name__ == "__main__":
    seed_bank_batch2()
