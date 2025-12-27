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
            # Q101 (Image 01)
            {
                "text": "Albert Nobel invented Penicillin.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "False. Penicillin was discovered by Alexander Fleming. Alfred Nobel is known for inventing dynamite and establishing the Nobel Prizes."
            },
            # Q102 (Image 02)
            {
                "text": "Drought is caused by excess rain.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "False. A drought is a deficiency of precipitation over an extended period."
            },
            # Q103 (Image 03)
            {
                "text": "Phnom Penh is the capital of Vietnam.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "False. Phnom Penh is the capital of Cambodia. The capital of Vietnam is Hanoi."
            },
            # Q104 (Image 04)
            {
                "text": "Rearrange LASIBMADA (Name of a Capital). What is the last letter?",
                "choices": [{"id": "a", "text": "D"}, {"id": "b", "text": "A"}, {"id": "c", "text": "M"}, {"id": "d", "text": "B"}, {"id": "e", "text": "L"}],
                "answer": "a",
                "explanation": "The word is ISLAMABAD (the capital of Pakistan). The last letter is D."
            },
            # Q105 (Image 05)
            {
                "text": "Rearrange BMUSRAENI (related to water). What is the middle letter?",
                "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}, {"id": "c", "text": "E"}, {"id": "d", "text": "I"}, {"id": "e", "text": "R"}],
                "answer": "a",
                "explanation": "The word is SUBMARINE. The middle letter is A (S-U-B-M-A-R-I-N-E)."
            },
            # Q106 (Image 06)
            {
                "text": "Rearrange LOGDRIAM (Name of a Flower). What is the 4th letter?",
                "choices": [{"id": "a", "text": "R"}, {"id": "b", "text": "I"}, {"id": "c", "text": "G"}, {"id": "d", "text": "O"}, {"id": "e", "text": "L"}],
                "answer": "b",
                "explanation": "The word is MARIGOLD. The 4th letter is I (M-A-R-I-G-O-L-D)."
            },
            # Q107 (Image 07)
            {
                "text": "Complete the series: 64, 16, 4, 1, ...",
                "choices": [{"id": "a", "text": "1/4, 1/8"}, {"id": "b", "text": "1/4, 1/16"}, {"id": "c", "text": "1/8, 1/4"}, {"id": "d", "text": "1/16, 1/8"}, {"id": "e", "text": "1/2, 1/4"}],
                "answer": "b",
                "explanation": "The series follows a pattern of dividing by 4: 1 / 4 = 1/4, and 1/4 / 4 = 1/16."
            },
            # Q108 (Image 08)
            {
                "text": "Complete the series: 54, 27, 30, 15, 12, ...",
                "choices": [{"id": "a", "text": "6, 9"}, {"id": "b", "text": "9, 6"}, {"id": "c", "text": "24, 9"}, {"id": "d", "text": "15, 7.5"}, {"id": "e", "text": "15, 30"}],
                "answer": "a",
                "explanation": "The pattern is: Divide by 2, then add 3. 54/2=27, 27+3=30, 30/2=15, 15-3 (Wait, 15-3=12), 12/2=6, 6+3=9."
            },
            # Q109 (Image 09)
            {
                "text": "Complete the series: 61, 62, 60, 61, 59, 60, ...",
                "choices": [{"id": "a", "text": "58, 59"}, {"id": "b", "text": "59, 58"}, {"id": "c", "text": "60, 61"}, {"id": "d", "text": "62, 63"}, {"id": "e", "text": "57, 58"}],
                "answer": "a",
                "explanation": "The pattern is: Add 1, then subtract 2. 60+1=61, 61-2=59, 59+1=60, 60-2=58, 58+1=59."
            },
            # Q110 (Image 10)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Hawk"}, {"id": "b", "text": "Dove"}, {"id": "c", "text": "Pigeon"}, {"id": "d", "text": "Crow"}, {"id": "e", "text": "Doel"}],
                "answer": "a",
                "explanation": "The Hawk is the only bird of prey in the list."
            },
            # Q111 (Image 11)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Hut"}, {"id": "b", "text": "Palace"}, {"id": "c", "text": "Room"}, {"id": "d", "text": "Building"}, {"id": "e", "text": "House"}],
                "answer": "c",
                "explanation": "A Room is an internal part of a structure, while the others refer to entire structures."
            },
            # Q112 (Image 12)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Gather"}, {"id": "b", "text": "Scatter"}, {"id": "c", "text": "Amuse"}, {"id": "d", "text": "Accumulate"}],
                "answer": "c",
                "explanation": "Amuse refers to an emotion or entertainment, while the others describe physical distribution or collection."
            },
            # Q113 (Image 13)
            {
                "text": "A is 8km South of B. C is 6km West of A. What is the distance between B and C?",
                "choices": [{"id": "a", "text": "10km"}, {"id": "b", "text": "12km"}, {"id": "c", "text": "8km"}, {"id": "d", "text": "14km"}],
                "answer": "a",
                "explanation": "Using Pythagorean theorem: sqrt(8^2 + 6^2) = sqrt(64 + 36) = sqrt(100) = 10km."
            },
            # Q114 (Image 14)
            {
                "text": "Stone is to solid, as liquid is to?",
                "choices": [{"id": "a", "text": "Solid"}, {"id": "b", "text": "Water"}, {"id": "c", "text": "Wine"}, {"id": "d", "text": "Gas"}],
                "answer": "b",
                "explanation": "Stone is an example of a solid; water is a common example of a liquid."
            },
            # Q115 (Image 15)
            {
                "text": "Dark is to dusk, as day is to?",
                "choices": [{"id": "a", "text": "Morning"}, {"id": "b", "text": "Night"}, {"id": "c", "text": "Light"}, {"id": "d", "text": "Bright"}],
                "answer": "a",
                "explanation": "Dusk marks the transition to darkness, similar to how morning marks the transition to light/day."
            },
            # Q116 (Image 16)
            {
                "text": "As Oars are to boat, so Fins are to?",
                "choices": [{"id": "a", "text": "Fish"}, {"id": "b", "text": "Frog"}, {"id": "c", "text": "Crocodile"}, {"id": "d", "text": "Ass"}],
                "answer": "a",
                "explanation": "Oars are used to propel a boat; fins are used to propel a fish."
            },
            # Q117 (Image 17)
            {
                "text": "Rearrange OTOPAT (a vegetable). What is the last letter?",
                "choices": [{"id": "a", "text": "O"}, {"id": "b", "text": "T"}, {"id": "c", "text": "P"}, {"id": "d", "text": "A"}],
                "answer": "a",
                "explanation": "The word is POTATO. The last letter is O."
            },
            # Q118 (Image 18)
            {
                "text": "Rearrange COHEKY (a game). What is the 3rd Letter?",
                "choices": [{"id": "a", "text": "Y"}, {"id": "b", "text": "O"}, {"id": "c", "text": "C"}, {"id": "d", "text": "K"}],
                "answer": "c",
                "explanation": "The word is HOCKEY. The 3rd letter is C (H-O-C-K-E-Y)."
            },
            # Q119 (Image 19)
            {
                "text": "Rearrange SAURTAIL (a continent). What is the middle letter?",
                "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "S"}, {"id": "c", "text": "R"}, {"id": "d", "text": "T"}],
                "answer": "c",
                "explanation": "The word is AUSTRALIA (9 letters). The middle letter is R (A-U-S-T-R-A-L-I-A)."
            },
            # Q120 (Image 20)
            {
                "text": "Complete the series: 11, 17, 13, 15, 15, 13, ...",
                "choices": [{"id": "a", "text": "17, 11"}, {"id": "b", "text": "17, 11"}, {"id": "c", "text": "15, 13"}, {"id": "d", "text": "15, 17"}],
                "answer": "a",
                "explanation": "Two alternating series: (11, 13, 15, 17) and (17, 15, 13, 11). Next terms are 17, 11."
            },
            # Q121 (Image 21)
            {
                "text": "(0.03 + 0.003) / 0.03 = ?",
                "choices": [{"id": "a", "text": "0.006"}, {"id": "b", "text": "0.003"}, {"id": "c", "text": "1.1"}, {"id": "d", "text": "2.2"}],
                "answer": "c",
                "explanation": "0.033 / 0.03 = 1.1."
            },
            # Q122 (Image 22) - Duplicate of 20
            {
                "text": "Complete the series: 11, 17, 13, 15, 15, 13, ...",
                "choices": [{"id": "a", "text": "17, 11"}, {"id": "b", "text": "18, 10"}, {"id": "c", "text": "16, 12"}],
                "answer": "a",
                "explanation": "Two alternating series: (11, 13, 15) and (17, 15, 13). Next terms are 17 and 11."
            },
            # Q123 (Image 23)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Radio"}, {"id": "b", "text": "Television"}, {"id": "c", "text": "Computer"}, {"id": "d", "text": "Video Player"}, {"id": "e", "text": "Laptop"}],
                "answer": "a",
                "explanation": "A Radio is the only audio-only device; the others provide visual output."
            },
            # Q124 (Image 24)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Australia"}, {"id": "b", "text": "Spain"}, {"id": "c", "text": "Italy"}, {"id": "d", "text": "Austria"}, {"id": "e", "text": "Bangladesh"}],
                "answer": "e",
                "explanation": "Bangladesh is located in Asia, whereas the others are in Europe or Oceania."
            },
            # Q125 (Image 25)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Copper"}, {"id": "b", "text": "Brass"}, {"id": "c", "text": "Nickel"}, {"id": "d", "text": "Iron"}],
                "answer": "b",
                "explanation": "Brass is an alloy (mixture), while the others are pure chemical elements."
            },
            # Q126 (Image 26)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Harmonium"}, {"id": "b", "text": "Pen"}, {"id": "c", "text": "Pencil"}, {"id": "d", "text": "Paper"}, {"id": "e", "text": "Book"}],
                "answer": "a",
                "explanation": "A Harmonium is a musical instrument, while the others are stationery/educational items."
            },
            # Q127 (Image 27)
            {
                "text": "Serpents change their skin once a year.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "True. Most snakes shed their skin multiple times a year as they grow."
            },
            # Q128 (Image 28)
            {
                "text": "Horses can run fast because they have wings.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "False. Real horses do not have wings."
            },
            # Q129 (Image 29)
            {
                "text": "Police become thieves at night.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "False. The professional role of police is to protect society, not to steal."
            },
            # Q130 (Image 30)
            {
                "text": "Cox's Bazar is the largest sea beach in the world.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "True. It is known as the longest natural sandy sea beach in the world."
            },
            # Q131 (Image 31)
            {
                "text": "Add all numbers: [3,4,7,6,5,19,8,2] then divide by the total count. Is the result less than 8?",
                "choices": [{"id": "a", "text": "Yes (a)"}, {"id": "b", "text": "No (b)"}],
                "answer": "a",
                "explanation": "Sum = 54. Count = 8. 54 / 8 = 6.75, which is less than 8."
            },
            # Q132 (Image 32)
            {
                "text": "A brother is 6 years old. His sister is half his age. In 6 years, how old will the sister be?",
                "choices": [{"id": "a", "text": "20"}, {"id": "b", "text": "18"}, {"id": "c", "text": "9"}, {"id": "d", "text": "12"}],
                "answer": "c",
                "explanation": "Sister starts at 3 (half of 6). In 6 years, she will be 3+6=9."
            },
            # Q133 (Image 33)
            {
                "text": "Complete the series: 2459, 4592, 5924, 9245, ...",
                "choices": [{"id": "a", "text": "4925"}, {"id": "b", "text": "5924"}, {"id": "c", "text": "4592"}, {"id": "d", "text": "2459"}],
                "answer": "d",
                "explanation": "The series rotates the first digit to the end. After 4 rotations, it returns to 2459."
            },
            # Q134 (Image 34)
            {
                "text": "Complete the series: 5, 4, 15, 14, 45, 44, ...",
                "choices": [{"id": "a", "text": "55, 54"}, {"id": "b", "text": "90, 91"}, {"id": "c", "text": "95, 94"}, {"id": "d", "text": "135, 134"}],
                "answer": "d",
                "explanation": "The pattern is multiplying by 3 for each pair: (5, 15, 45 -> 135) and (4, 14, 44 -> 134)."
            },
            # Q135 (Image 35)
            {
                "text": "Complete the series: 4, 5, 10, 11, 22, 23, ...",
                "choices": [{"id": "a", "text": "48, 47"}, {"id": "b", "text": "43, 44"}, {"id": "c", "text": "46, 47"}, {"id": "d", "text": "45, 46"}],
                "answer": "c",
                "explanation": "The pattern is (+1, *2): 4+1=5, 5*2=10, 10+1=11, 11*2=22, 22+1=23, 23*2=46, 46+1=47."
            },
            # Q136 (Image 36)
            {
                "text": "Rearrange MOEDABOI (Name of a country). What is the 4th letter?",
                "choices": [{"id": "a", "text": "M"}, {"id": "b", "text": "B"}, {"id": "c", "text": "O"}, {"id": "d", "text": "A"}],
                "answer": "b",
                "explanation": "The word is CAMBODIA. The 4th letter is B (C-A-M-B-O-D-I-A)."
            },
            # Q137 (Image 37)
            {
                "text": "Rearrange GKNISIFREH (Name of a Bird). What is the 6th letter?",
                "choices": [{"id": "a", "text": "I"}, {"id": "b", "text": "F"}, {"id": "c", "text": "G"}, {"id": "d", "text": "N"}],
                "answer": "a",
                "explanation": "The word is KINGFISHER. The 6th letter is I (K-I-N-G-F-I-S-H-E-R)."
            },
            # Q138 (Image 38)
            {
                "text": "Rearrange EEHCRLFU (Means happiness). What is the 2nd letter?",
                "choices": [{"id": "a", "text": "H"}, {"id": "b", "text": "E"}, {"id": "c", "text": "C"}, {"id": "d", "text": "R"}],
                "answer": "a",
                "explanation": "The word is CHEERFUL. The 2nd letter is H (C-H-E-E-R-F-U-L)."
            },
            # Q139 (Image 39)
            {
                "text": "If BIRD is 2-9-18-4, then 6-9-19-20 is?",
                "choices": [{"id": "a", "text": "FISH"}, {"id": "b", "text": "FIST"}, {"id": "c", "text": "FITS"}, {"id": "d", "text": "FIZZ"}],
                "answer": "b",
                "explanation": "Based on alphabetical position: F=6, I=9, S=19, T=20. So 6-9-19-20 is FIST."
            },
            # Q140 (Image 40)
            {
                "text": "ADF is to ZWU, so SRG is to?",
                "choices": [{"id": "a", "text": "STT"}, {"id": "b", "text": "HII"}, {"id": "c", "text": "SIT"}, {"id": "d", "text": "TIH"}, {"id": "e", "text": "HIT"}],
                "answer": "e",
                "explanation": "Based on mirrored alphabetical position (A=1/Z=26): S(19)->H(8), R(18)->I(9), G(7)->T(20). So HIT."
            },
            # Q141 (Image 41)
            {
                "text": "Always is to rarely, as fluently is to?",
                "choices": [{"id": "a", "text": "Everyday"}, {"id": "b", "text": "All-time"}, {"id": "c", "text": "Influently"}, {"id": "d", "text": "Haltingly"}],
                "answer": "d",
                "explanation": "Always/Rarely are opposites. Fluently's opposite is Haltingly (speaking with pauses/stutters)."
            },
            # Q142 (Image 42)
            {
                "text": "Sin is to confess, as fault is to?",
                "choices": [{"id": "a", "text": "Closed"}, {"id": "b", "text": "Absent"}, {"id": "c", "text": "Admit"}, {"id": "d", "text": "Open"}],
                "answer": "c",
                "explanation": "You confess a sin; you admit a fault."
            },
            # Q143 (Image 43)
            {
                "text": "Right is to wrong, as bee is to?",
                "choices": [{"id": "a", "text": "Kiss"}, {"id": "b", "text": "Drone"}, {"id": "c", "text": "Honey"}, {"id": "d", "text": "Milk"}],
                "answer": "b",
                "explanation": "Right and wrong are opposites/complements. A Drone is the male counterpart to a worker bee."
            },
            # Q144 (Image 44)
            {
                "text": "March is to January, as September is to?",
                "choices": [{"id": "a", "text": "October"}, {"id": "b", "text": "July"}, {"id": "c", "text": "August"}, {"id": "d", "text": "April"}],
                "answer": "b",
                "explanation": "January is two months before March. July is two months before September."
            },
            # Q145 (Image 45)
            {
                "text": "Man is to woman, as ram is to?",
                "choices": [{"id": "a", "text": "Cock"}, {"id": "b", "text": "Hen"}, {"id": "c", "text": "Horse"}, {"id": "d", "text": "Ewe"}],
                "answer": "d",
                "explanation": "Ram is the male sheep; Ewe is the female sheep."
            },
            # Q146 (Image 46)
            {
                "text": "The more you read the more you learn.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "True. Reading is a primary method for acquiring knowledge."
            },
            # Q147 (Image 47)
            {
                "text": "Leaders are always born.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "False. Many leaders develop through experience and training."
            },
            # Q148 (Image 48)
            {
                "text": "Necessity is the mother of all invention.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "True. A common proverb meaning that a need often drives creative solutions."
            },
            # Q149 (Image 49)
            {
                "text": "Rearrange RTNASTIOSR (Electronic Device). What is the last letter?",
                "choices": [{"id": "a", "text": "R"}, {"id": "b", "text": "S"}, {"id": "c", "text": "N"}, {"id": "d", "text": "A"}],
                "answer": "a",
                "explanation": "The word is TRANSISTOR. The last letter is R."
            },
            # Q150 (Image 50)
            {
                "text": "Rearrange AANRNAYNAJG (Name of a District). What is the 5th letter?",
                "choices": [{"id": "a", "text": "R"}, {"id": "b", "text": "A"}, {"id": "c", "text": "Y"}, {"id": "d", "text": "G"}],
                "answer": "c",
                "explanation": "The word is NARAYANGANJ. The 5th letter is Y (N-A-R-A-Y)."
            },
            
            # START IMAGE 1 (51-100)
            # Q151 (Image 51)
            {
                "text": "Rearrange RBAEVYR (one kind of virtue). What is the 7th letter?",
                "choices": [{"id": "a", "text": "V"}, {"id": "b", "text": "E"}, {"id": "c", "text": "R"}, {"id": "d", "text": "B"}, {"id": "e", "text": "Y"}],
                "answer": "e",
                "explanation": "The word is BRAVERY. The 7th letter is Y."
            },
            # Q152 (Image 52)
            {
                "text": "Rearrange SSSIORSC (used to cut). What is the 6th letter?",
                "choices": [{"id": "a", "text": "C"}, {"id": "b", "text": "I"}, {"id": "c", "text": "O"}, {"id": "d", "text": "S"}, {"id": "e", "text": "R"}],
                "answer": "c",
                "explanation": "The word is SCISSORS. The 6th letter is O (S-C-I-S-S-O-R-S)."
            },
            # Q153 (Image 53)
            {
                "text": "Rearrange WSTIEZLRNAD (Name of a country). What is the last letter?",
                "choices": [{"id": "a", "text": "S"}, {"id": "b", "text": "W"}, {"id": "c", "text": "L"}, {"id": "d", "text": "A"}, {"id": "e", "text": "D"}],
                "answer": "e",
                "explanation": "The word is SWITZERLAND. The last letter is D."
            },
            # Q154 (Image 54)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Stalin"}, {"id": "b", "text": "Hitler"}, {"id": "c", "text": "Roosevelt"}, {"id": "d", "text": "Plato"}, {"id": "e", "text": "Mussolini"}],
                "answer": "d",
                "explanation": "Plato was a philosopher; the others were major political/war leaders."
            },
            # Q155 (Image 55)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Bangla"}, {"id": "b", "text": "Markin"}, {"id": "c", "text": "English"}, {"id": "d", "text": "Hindi"}, {"id": "e", "text": "Arabic"}],
                "answer": "b",
                "explanation": "Markin refers to Americans/Nationality or cloth, while others are specific languages."
            },
            # Q156 (Image 56)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Hockey"}, {"id": "b", "text": "Chess"}, {"id": "c", "text": "Tennis"}, {"id": "d", "text": "Football"}, {"id": "e", "text": "Cricket"}],
                "answer": "b",
                "explanation": "Chess is an indoor board game, while the others are outdoor field sports."
            },
            # Q157 (Image 57)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "M. Rahman"}, {"id": "b", "text": "A. Rouf"}, {"id": "c", "text": "M. Zaman"}, {"id": "d", "text": "N. M. Sheik"}],
                "answer": "c",
                "explanation": "M. Zaman is not among the seven Bir Sreshtho awardees of Bangladesh."
            },
            # Q158 (Image 58)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Shoulder"}, {"id": "b", "text": "Chest"}, {"id": "c", "text": "Grapes"}, {"id": "d", "text": "Head"}, {"id": "e", "text": "Arm"}],
                "answer": "c",
                "explanation": "Grapes is a fruit, whereas the others are parts of the human body."
            },
            # Q159 (Image 59)
            {
                "text": "Rearrange HWTAC (Name of a useful thing). What is the 4th letter?",
                "choices": [{"id": "a", "text": "C"}, {"id": "b", "text": "H"}, {"id": "c", "text": "W"}, {"id": "d", "text": "T"}],
                "answer": "a",
                "explanation": "The word is WATCH. The 4th letter is C (W-A-T-C-H)."
            },
            # Q160 (Image 60)
            {
                "text": "Rearrange UMBRIDEGRBA (Name of an obstacle). What is the 2nd letter?",
                "choices": [{"id": "a", "text": "E"}, {"id": "b", "text": "U"}, {"id": "c", "text": "R"}, {"id": "d", "text": "A"}],
                "answer": "c",
                "explanation": "The word rearranged is BRIDGE (partially). Actually, B-R-I-D-G-E is an obstacle/structure. 2nd letter is R."
            },
            # Q161 (Image 61)
            {
                "text": "Rearrange ECILNP (Name of a useful thing). What is the 5th letter?",
                "choices": [{"id": "a", "text": "E"}, {"id": "b", "text": "I"}, {"id": "c", "text": "N"}, {"id": "d", "text": "P"}],
                "answer": "b",
                "explanation": "The word is PENCIL. The 5th letter is I (P-E-N-C-I-L)."
            },
            # Q162 (Image 62)
            {
                "text": "Rearrange SMWOCO (Name of a capital city). What is the last letter?",
                "choices": [{"id": "a", "text": "M"}, {"id": "b", "text": "S"}, {"id": "c", "text": "C"}, {"id": "d", "text": "O"}, {"id": "e", "text": "W"}],
                "answer": "e",
                "explanation": "The word is MOSCOW. The last letter is W."
            },
            # Q163 (Image 63)
            {
                "text": "Rearrange GNAFLJO (A place of recreation). What is the last letter?",
                "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "J"}, {"id": "c", "text": "G"}, {"id": "d", "text": "N"}, {"id": "e", "text": "F"}],
                "answer": "c",
                "explanation": "The word is JAFLONG (a tourist spot in Bangladesh). The last letter is G."
            },
            # Q164 (Image 64)
            {
                "text": "If 2x2=8, 3x3=18, then 5x5=?",
                "choices": [{"id": "a", "text": "25"}, {"id": "b", "text": "100"}, {"id": "c", "text": "125"}, {"id": "d", "text": "10"}, {"id": "e", "text": "50"}],
                "answer": "e",
                "explanation": "The pattern is (nxn) x 2. So (5x5) x 2 = 50."
            },
            # Q165 (Image 65)
            {
                "text": "Complete the series: 7, 2, 10, 4, 13, 8, ...",
                "choices": [{"id": "a", "text": "10, 13"}, {"id": "b", "text": "16, 13"}, {"id": "c", "text": "13, 16"}, {"id": "d", "text": "16, 16"}, {"id": "e", "text": "13, 13"}],
                "answer": "d",
                "explanation": "Two series: (7, 10, 13 -> 16) and (2, 4, 8 -> 16). So 16, 16."
            },
            # Q166 (Image 66)
            {
                "text": "Complete the series: 216, 125, 64, 27, 8, ...",
                "choices": [{"id": "a", "text": "1, 0"}, {"id": "b", "text": "0, 1"}, {"id": "c", "text": "2, 0"}, {"id": "d", "text": "2, 1"}],
                "answer": "a",
                "explanation": "The series follows descending cubes: 6^3, 5^3, 4^3, 3^3, 2^3, 1^3=1, 0^3=0."
            },
            # Q167 (Image 67)
            {
                "text": "Complete the series: 1, 1/2, 1/4, ...",
                "choices": [{"id": "a", "text": "1/8, 1/16"}, {"id": "b", "text": "1/16, 1/8"}, {"id": "c", "text": "1/6, 1/8"}, {"id": "d", "text": "1/8, 1/12"}],
                "answer": "a",
                "explanation": "The pattern is dividing by 2 each time."
            },
            # Q168 (Image 68)
            {
                "text": "Complete the series: 2, 4, 5, 10, 11, 22, ...",
                "choices": [{"id": "a", "text": "45, 44"}, {"id": "b", "text": "44, 45"}, {"id": "c", "text": "46, 47"}, {"id": "d", "text": "46, 23"}, {"id": "e", "text": "23, 46"}],
                "answer": "e",
                "explanation": "The pattern is (*2, +1): 22+1=23, 23*2=46."
            },
            # Q169 (Image 69)
            {
                "text": "Complete the series: 48, 24, 72, 36, 108, 54, ...",
                "choices": [{"id": "a", "text": "81, 163"}, {"id": "b", "text": "162, 81"}, {"id": "c", "text": "81, 162"}, {"id": "d", "text": "162, 80"}],
                "answer": "b",
                "explanation": "The pattern is (/2, *3): 54*3=162, 162/2=81."
            },
            # Q170 (Image 70)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Milk"}, {"id": "b", "text": "Salad"}, {"id": "c", "text": "Coffee"}, {"id": "d", "text": "Tea"}, {"id": "e", "text": "Rum"}],
                "answer": "b",
                "explanation": "Salad is a solid food, whereas the others are liquid beverages."
            },
            # Q171 (Image 71)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Interlocution"}, {"id": "b", "text": "Dialogue"}, {"id": "c", "text": "Duologue"}, {"id": "d", "text": "Monologue"}],
                "answer": "d",
                "explanation": "A monologue is for one person, while the others involve two or more people."
            },
            # Q172 (Image 72)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Gynecologist"}, {"id": "b", "text": "Psychologist"}, {"id": "c", "text": "Doctor"}, {"id": "d", "text": "Obstetrician"}],
                "answer": "b",
                "explanation": "A Psychologist studies the mind/behavior, while the others are medical doctors focused on the physical body."
            },
            # Q173 (Image 73)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Yen"}, {"id": "b", "text": "Ngultrum"}, {"id": "c", "text": "Ruble"}, {"id": "d", "text": "Peso"}, {"id": "e", "text": "Pice"}],
                "answer": "e",
                "explanation": "Pice is a subunit of currency (like a cent), whereas the others are main currency units."
            },
            # Q174 (Image 74)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Waterman"}, {"id": "b", "text": "Shakespeare"}, {"id": "c", "text": "Nazrul"}, {"id": "d", "text": "Tagore"}],
                "answer": "a",
                "explanation": "Waterman is a generic profession/name, while the others are globally famous literature figures."
            },
            # Q175 (Image 75)
            {
                "text": "Doctor is to medicine, as teacher is to?",
                "choices": [{"id": "a", "text": "Power"}, {"id": "b", "text": "Hit"}, {"id": "c", "text": "School"}, {"id": "d", "text": "Love"}, {"id": "e", "text": "Teach"}],
                "answer": "e",
                "explanation": "A doctor's primary function is medicine; a teacher's primary function is teaching."
            },
            # Q176 (Image 76)
            {
                "text": "Dog is to barking, as cat is to?",
                "choices": [{"id": "a", "text": "Loving"}, {"id": "b", "text": "Heating"}, {"id": "c", "text": "Mewing"}, {"id": "d", "text": "Kissing"}],
                "answer": "c",
                "explanation": "These are the sounds produced by these animals."
            },
            # Q177 (Image 77)
            {
                "text": "Ocean is to deep, as sky is to?",
                "choices": [{"id": "a", "text": "High"}, {"id": "b", "text": "Blue"}, {"id": "c", "text": "Akashi"}, {"id": "d", "text": "Bird"}],
                "answer": "a",
                "explanation": "Ocean is characterized by depth; sky is characterized by height."
            },
            # Q178 (Image 78)
            {
                "text": "Food is to growth, as knowledge is to?",
                "choices": [{"id": "a", "text": "Wise"}, {"id": "b", "text": "Bold"}, {"id": "c", "text": "Energy"}, {"id": "d", "text": "Rich"}],
                "answer": "a",
                "explanation": "Food enables physical growth; knowledge enables intellectual wisdom."
            },
            # Q179 (Image 79)
            {
                "text": "Infantry is to walk, as cavalry is to?",
                "choices": [{"id": "a", "text": "Army"}, {"id": "b", "text": "Ass"}, {"id": "c", "text": "Cow"}, {"id": "d", "text": "Horse"}],
                "answer": "d",
                "explanation": "Infantry soldiers move by walking; cavalry soldiers move on horses."
            },
            # Q180 (Image 80)
            {
                "text": "If CFIL = NQTQ, then ADGU = ?",
                "choices": [{"id": "a", "text": "LQRF"}, {"id": "b", "text": "LPRF"}, {"id": "c", "text": "LORG"}, {"id": "d", "text": "LORE"}, {"id": "e", "text": "LORF"}],
                "answer": "e",
                "explanation": "Pattern: +11 positions. A+11=L, D+11=O, G+11=R, U+11=F."
            },
            # Q181 (Image 81)
            {
                "text": "If EML = JRQ, then CEI = ?",
                "choices": [{"id": "a", "text": "HJN"}, {"id": "b", "text": "HHN"}, {"id": "c", "text": "HIN"}, {"id": "d", "text": "HJM"}],
                "answer": "a",
                "explanation": "Pattern: +5 positions. C+5=H, E+5=J, I+5=N."
            },
            # Q182 (Image 82)
            {
                "text": "If VZT = QUO, then PSW = ?",
                "choices": [{"id": "a", "text": "KKU"}, {"id": "b", "text": "KNR"}, {"id": "c", "text": "KNP"}, {"id": "d", "text": "KMR"}],
                "answer": "b",
                "explanation": "Pattern: -5 positions. P-5=K, S-5=N, W-5=R."
            },
            # Q183 (Image 83)
            {
                "text": "If DAG = PMS, then GDI = ?",
                "choices": [{"id": "a", "text": "TSU"}, {"id": "b", "text": "SPW"}, {"id": "c", "text": "SPU"}, {"id": "d", "text": "SRU"}],
                "answer": "c",
                "explanation": "Pattern: +12 positions. G+12=S, D+12=P, I+12=U."
            },
            # Q184 (Image 84)
            {
                "text": "If BBC = YYX, then DDI = ?",
                "choices": [{"id": "a", "text": "WMR"}, {"id": "b", "text": "WUR"}, {"id": "c", "text": "WWP"}, {"id": "d", "text": "WWR"}, {"id": "e", "text": "VVR"}],
                "answer": "d",
                "explanation": "Pattern is mirrored positioning (A=1/Z=26). D=4 -> W=23. I=9 -> R=18."
            },
            # Q185 (Image 85)
            {
                "text": "WHO (World Health Organization) was established in 1945.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "False. WHO was established on April 7, 1948."
            },
            # Q186 (Image 86)
            {
                "text": "A good liar needs a good memory.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "True. To maintain consistency, a liar must remember all previously told lies."
            },
            # Q187 (Image 87)
            {
                "text": "It is impossible for a man to cross the English Channel.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "b",
                "explanation": "False. Thousands of people have swam across or crossed the English Channel."
            },
            # Q188 (Image 88)
            {
                "text": "A liar trusts nobody.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "True. This is a common psychological observation regarding projection."
            },
            # Q189 (Image 89)
            {
                "text": "Every man is the architect of his own fortune.",
                "choices": [{"id": "a", "text": "True"}, {"id": "b", "text": "False"}],
                "answer": "a",
                "explanation": "True. A famous quote emphasizing personal responsibility for success."
            },
            # Q190 (Image 90)
            {
                "text": "Rearrange ABNIRRAATHND (Name of a famous poet). What is the 10th letter?",
                "choices": [{"id": "a", "text": "B"}, {"id": "b", "text": "A"}, {"id": "c", "text": "N"}, {"id": "d", "text": "T"}],
                "answer": "b",
                "explanation": "The word is RABINDRANATH. The 10th letter is A."
            },
            # Q191 (Image 91)
            {
                "text": "Rearrange PTTAOO (A vegetable). What is the last letter?",
                "choices": [{"id": "a", "text": "O"}, {"id": "b", "text": "P"}, {"id": "c", "text": "T"}, {"id": "d", "text": "A"}],
                "answer": "a",
                "explanation": "The word is POTATO. The last letter is O."
            },
            # Q192 (Image 92)
            {
                "text": "Rearrange IANCENF (Related to money). What is the 4th letter?",
                "choices": [{"id": "a", "text": "I"}, {"id": "b", "text": "B"}, {"id": "c", "text": "A"}, {"id": "d", "text": "N"}, {"id": "e", "text": "F"}],
                "answer": "c",
                "explanation": "The word is FINANCE. The 4th letter is A (F-I-N-A-N-C-E)."
            },
            # Q193 (Image 93)
            {
                "text": "Rearrange EQLAPDR (An animal/best). What is the 4th letter?",
                "choices": [{"id": "a", "text": "L"}, {"id": "b", "text": "D"}, {"id": "c", "text": "P"}, {"id": "d", "text": "A"}],
                "answer": "c",
                "explanation": "The word is LEOPARD. The 4th letter is P (L-E-O-P-A-R-D)."
            },
            # Q194 (Image 94)
            {
                "text": "Rearrange RATAIHC (A part of the body). What is the 3rd letter?",
                "choices": [{"id": "a", "text": "H"}, {"id": "b", "text": "I"}, {"id": "c", "text": "R"}, {"id": "d", "text": "A"}],
                "answer": "d",
                "explanation": "The word is TRACHIA (windpipe). The 3rd letter is A (T-R-A-C-H-I-A)."
            },
            # Q195 (Image 95)
            {
                "text": "Rokon and Jumi caught 15 frogs. Rokon caught 4 times fewer than Jumi. How many did Rokon catch?",
                "choices": [{"id": "a", "text": "6"}, {"id": "b", "text": "7"}, {"id": "c", "text": "3"}, {"id": "d", "text": "5"}],
                "answer": "c",
                "explanation": "Let Rokon = x. Jumi = 4x. x + 4x = 15. 5x = 15. x = 3."
            },
            # Q196 (Image 96)
            {
                "text": "How many times does the digit 5 appear in the numbers from 1 to 100?",
                "choices": [{"id": "a", "text": "10"}, {"id": "b", "text": "11"}, {"id": "c", "text": "20"}, {"id": "d", "text": "19"}],
                "answer": "c",
                "explanation": "5 appears in [5, 15, 25, 35, 45, 50, 51, 52, 53, 54, 55 (twice), 56, 57, 58, 59, 65, 75, 85, 95] = 20 times."
            },
            # Q197 (Image 97)
            {
                "text": "Complete the series: 5, 24, 61, 122, ...",
                "choices": [{"id": "a", "text": "180"}, {"id": "b", "text": "213"}, {"id": "c", "text": "210"}, {"id": "d", "text": "200"}],
                "answer": "b",
                "explanation": "The pattern is (n^3 - 3). 2^3-3=5, 3^3-3=24, 4^3-3=61, 5^3-3=122, 6^3-3=213."
            },
            # Q198 (Image 98)
            {
                "text": "Which one is odd?",
                "choices": [{"id": "a", "text": "Read"}, {"id": "b", "text": "Black"}, {"id": "c", "text": "Green"}, {"id": "d", "text": "Violet"}, {"id": "e", "text": "Yellow"}],
                "answer": "a",
                "explanation": "Read is a verb; the others are colors."
            },
            # Q199 (Image 99)
            {
                "text": "If TIE=34 and FOOL=48, then FUN=?",
                "choices": [{"id": "a", "text": "45"}, {"id": "b", "text": "34"}, {"id": "c", "text": "41"}, {"id": "d", "text": "55"}],
                "answer": "c",
                "explanation": "Sum of alphabetical positions: F(6)+U(21)+N(14) = 41."
            },
            # Q200 (Image 100)
            {
                "text": "Rearrange LPAEDOR (An animal). What is the last letter?",
                "choices": [{"id": "a", "text": "E"}, {"id": "b", "text": "P"}, {"id": "c", "text": "R"}, {"id": "d", "text": "D"}],
                "answer": "d",
                "explanation": "The word is LEOPARD. The last letter is D."
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
                
        print(f"Successfully added 100 new questions to the bank (101-200).")
        
    except Exception as e:
        print(f"Error seeding bank: {e}")

if __name__ == "__main__":
    seed_bank_batch2()
