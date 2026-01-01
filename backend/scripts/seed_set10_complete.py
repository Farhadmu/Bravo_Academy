import os
import django
import sys
import re

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def parse_and_create_set10():
    print("Creating 'IQ Test - Set 10'...")
    
    # Create or get the test
    set10, created = Test.objects.get_or_create(
        name="IQ Test - Set 10",
        defaults={
            "description": "Tenth set of IQ evaluation questions",
            "duration_minutes": 30,
            "price": 0.00,
            "is_active": True
        }
    )
    
    if created:
        print(f"Created new test: {set10.name}")
    else:
        print(f"Found existing test: {set10.name}")

    # Raw content of the questions provided by user
    questions_raw = """
Question 01

Question: You are 18 years. 5 years later the difference between you and your younger brother will be 10. How old is your brother now?
Options: (a) 8 (b) 20 (c) 9 (d) 16
Answer: (a) 8
Explanation: Age difference is constant, so brother is 10 years younger than you now.

Question 02

Question: Monday is to Friday as Wednesday is to –
Options: (a) Monday (b) Friday (c) Saturday (d) Sunday
Answer: (b) Friday
Explanation: The gap from Monday to Friday is 4 days, same from Wednesday to Friday.

Question 03

Question: Facing south, you go right 3 miles, then right again 4 miles. What is the distance from the initial point?
Options: (a) 5 (b) 6 (c) 4 (d) 10
Answer: (a) 5
Explanation: Movement forms a right triangle with sides 3 and 4.

Question 04

Question: Go north 6 miles, right 3 miles, then south 6 miles. Which direction are you from start?
Options: (a) North (b) South (c) West (d) East
Answer: (d) East
Explanation: North and south movements cancel leaving eastward movement.

Question 05

Question: What is the relation between me and sister’s husband’s daughter?
Options: (a) Brother (b) Sister (c) Sister-in-law (d) Niece (e) Nephew
Answer: (d) Niece
Explanation: Sister’s husband’s daughter is your niece.

Question 06

Question: A girl loves a boy who is her father’s sister’s nephew. Who is the boy?
Options: (a) Lover (b) Cousin (c) Friend (d) Brother (e) Classmate
Answer: (b) Cousin
Explanation: Father’s sister’s nephew refers to her cousin.

Question 07

Question: She is the only daughter of A’s mother-in-law. Who is A to her?
Options: (a) Wife (b) Husband (c) Son (d) Daughter (e) Father
Answer: (b) Husband
Explanation: Mother-in-law’s daughter is A’s wife.

Question 08

Question: C is mother of D. D is not daughter of C. What is the relation?
Options: (a) C is daughter (b) C is brother (c) D is son of C (d) D is sister (e) D is father of A
Answer: (c) D is son of C
Explanation: If D is not a daughter, D must be a son.

Question 09

Question: My father married your father’s mother. Who am I to you?
Options: (a) Son (b) Aunt (c) Brother (d) Sister (e) Cousin
Answer: (c) Brother
Explanation: Both share the same grandmother, making them siblings.

Question 10

Question: Ant, Cockroach, Lizard, Fly, Grasshopper – find the odd.
Options: (a) Ant (b) Cockroach (c) Lizard (d) Fly (e) Grasshopper
Answer: (c) Lizard
Explanation: Lizard is a reptile while others are insects.

Question 11

Question: “As is the evil, so is the remedy.” The sentence is –
Options: (a) False (b) None (c) Both (d) True (e) Can’t tell
Answer: (d) True
Explanation: The proverb conveys a valid logical meaning.

Question 12

Question: Complete the series: 4, 5, 8, 9, 12, __ ?
Options: (a) 14,18 (b) 13,16 (c) 15,30 (d) 18,24 (e) 20,24
Answer: (b) 13,16
Explanation: Alternating +1 and +3 pattern.

Question 13

Question: Insert the missing alphabet: Z, T, N, H, __ ?
Options: (a) X,Y (b) A,D (c) M,N (d) O,Q (e) B,V
Answer: (b) A, D
Explanation: Letters move backward by 6 positions.

Question 14

Question: 5, 17, 37, 65, __ ?
Options: (a) 81,100 (b) 75,97 (c) 24,215 (d) 97,123 (e) 101,145
Answer: (d) 97,123
Explanation: Pattern is n²+1.

Question 15

Question: 1, 8, 5, 12, 9, 50, 3, 10, 49, 4, __ ?
Options: (a) 12,36 (b) 11,48 (c) 12,36 (d) 17,34 (e) 15,30
Answer: (b) 11,48
Explanation: Numbers follow mixed square and increment patterns.

Question 16

Question: A boy’s father says, “I cannot donate my son’s operation.” What is the doctor’s relation?
Options: (a) Uncle (b) Aunt (c) Mother (d) Father (e) Brother
Answer: (c) Mother
Explanation: Only the mother can say “my son” and refuse donation.

Question 17

Question: Rearrange APLIAHKAUT (PLACE), find last letter.
Options: (a) P (b) A (c) K (d) I (e) L
Answer: (e) L
Explanation: Rearranged word is “KATHALPUIA” → “KATHALPUIA” ends with L.

Question 18

Question: Find the odd:
Options: (a) Canon (b) Rifle (c) Tank (d) Jeep (e) Submarine
Answer: (b) Rifle
Explanation: Rifle is handheld while others are large military machines.

Question 19

Question: Who is the sister of my cousin?
Options: (a) Brother (b) Cousin (c) Father (d) Sister (e) Grandfather
Answer: (b) Cousin
Explanation: Cousin’s sister is also a cousin.

Question 20

Question: The animal that lays eggs and produces milk –
Options: (a) Emu (b) Koala (c) Crocodile (d) Platypus (e) Rhinoceros
Answer: (d) Platypus
Explanation: Platypus is a monotreme that lays eggs and gives milk.

Question 21

Question: A tree is 50 meters apart from another. How many trees on both sides of 1 km road?
Options: (a) 20 (b) 42 (c) 10 (d) 25 (e) 9
Answer: (b) 42
Explanation: 1000 ÷ 50 = 20 intervals per side plus one extra on each side.

Question 22

Question: 31, 5, 99, 41, 7, 198, 51, 9, 396, 61, 11, __ ?
Options: (a) 729,51 (b) 792,71 (c) 735,25 (d) 692,50 (e) 727,27
Answer: (b) 792,71
Explanation: Pattern alternates ×2 and +10.

Question 23

Question: Lieutenant is to Major as Squadron Leader is to –
Options: (a) Captain (b) Group Captain (c) Commodore (d) Colonel (e) Lt Commander
Answer: (b) Group Captain
Explanation: Equivalent higher rank in Air Force hierarchy.

Question 24

Question: Complete: 15, 1, 13, 3, 11, 5, 9, __ ?
Options: (a) 3,2 (b) 5,4 (c) 7,6 (d) 8,7 (e) 7,7
Answer: (c) 7,6
Explanation: One sequence decreases by 2 and the other increases by 2.

Question 25

Question: 2, 4, 7, 9, 12, 14, 17, __ ?
Options: (a) 20,24 (b) 19,22 (c) 22,25 (d) 24,29 (e) 27,37
Answer: (b) 19,22
Explanation: Alternating +2 and +3 pattern.

Question 26

Question: Find the most similar word – Deal in:
Options: (a) in business (b) behavior with (c) exchange with (d) post to (e) fill in
Answer: (c) exchange with
Explanation: “Deal in” means to trade or exchange.

Question 27

Question: Rearrange ROLSEDI, find last letter.
Options: (a) S (b) R (c) D (d) P (e) O
Answer: (c) D
Explanation: Rearranged word is “SOLDIER” which ends with R, but root form ends with D.

Question 28

Question: Trees are 250 meters apart around a 2 km pond. How many trees required?
Options: (a) 10 (b) 20 (c) 8 (d) 2 (e) 12
Answer: (c) 8
Explanation: 2000 ÷ 250 = 8 trees.

Question 29

A, P, C, S, E, V, G, ___ ?

Options:
(a) J, K
(b) Y, K
(c) Z, P
(d) I, D
(e) Y, I

Answer: (a) J, K

Explanation: Letters alternate between alphabetical jumps of +15 and +2.

Question 30

Father and son's age total is 32 years. After 7 years what will be their age total?

Options:
(a) 39
(b) 32
(c) 46
(d) 35
(e) 40

Answer: (c) 46

Explanation: After 7 years both ages increase by 7, so total increases by 14.

Question 31

If Moon is the natural planet of Earth, write Mercury, otherwise write Star.

Options:
(a) Star
(b) Mercury
(c) Moon
(d) Planet
(e) True

Answer: (b) Mercury

Explanation: Moon is Earth’s natural satellite, so the condition is true.

Question 32

FOOD = JSSH, SLEEP = ?

Options:
(a) TLEEP
(b) FLEET
(c) TWINK
(d) WPHT
(e) TWIPE

Answer: (b) FLEET

Explanation: Each letter is shifted forward by 4 places in the alphabet.

Question 33

If Tuesday is two days before yesterday, what is three days after tomorrow?

Options:
(a) Sun
(b) Tue
(c) Thu
(d) Wed
(e) Sat

Answer: (a) Sun

Explanation: If Tuesday is two days before yesterday, today is Thursday, so three days after tomorrow is Sunday.

Question 34

E, K, P, T, ___ ?

Options:
(a) U, V
(b) W, Y
(c) X, Z
(d) V, Y
(e) Z, B

Answer: (d) V, Y

Explanation: Alphabet positions increase alternately by +6 and +5.

Question 35

Find the odd one out

Options:
(a) Goat
(b) Lion
(c) Deer
(d) Tiger
(e) Human

Answer: (e) Human

Explanation: All others are animals except human.

Question 36

Example is better than law

Options:
(a) True
(b) False
(c) N/A
(d) None
(e) ALL

Answer: (a) True

Explanation: The statement reflects a commonly accepted moral principle.

Question 37

Good wine needs no bush. The statement is True or False

Options:
(a) True
(b) False
(c) N/A
(d) None
(e) ALL

Answer: (a) True

Explanation: The proverb means quality needs no advertisement.

Question 38

Male is to Mall as Hale is to ___ ?

Options:
(a) Hat
(b) Bella
(c) Tell
(d) Hell
(e) Hall

Answer: (e) Hall

Explanation: One letter is changed to form a meaningful word.

Question 39

Complete the series: 15, 26, 20, 30, 25, 35, ___ , ___ ?

Options:
(a) 30, 41
(b) 30, 42
(c) 32, 41
(d) 42, 30
(e) 25, 41

Answer: (b) 30, 42

Explanation: Numbers alternate by +11 and -6, then +12.

Question 40

Seed is to Speed as send is to ___ ?

Options:
(a) Dense
(b) Stend
(c) Spand
(d) Spend
(e) Sand

Answer: (d) Spend

Explanation: One extra letter ‘p’ is added after the first letter.

Question 41

Complete the series: 81, 69, 58, 48, 39, ___ , ___ ?

Options:
(a) 28, 35
(b) 31, 24
(c) 31, 23
(d) 23, 33
(e) 32, 24

Answer: (c) 31, 23

Explanation: Differences decrease by 1 each time.

Question 42

Find the odd one out

Options:
(a) Eye
(b) Ear
(c) Tongue
(d) Head
(e) Skin

Answer: (d) Head

Explanation: All others are sense organs, head is not.

Question 43

Complete the series: 7, 10, 15, 22, 31, ___ ?

Options:
(a) 42
(b) 55
(c) 40
(d) 50
(e) 25

Answer: (a) 42

Explanation: Differences increase by consecutive odd numbers.

Question 44

Bat is to pup as ___ is to chick

Options:
(a) Camel
(b) Cheetah
(c) Lion
(d) Bone
(e) Bird

Answer: (e) Bird

Explanation: Pup and chick are baby forms of bat and bird respectively.

Question 45

Complete the series: 3/27, 5/24, 7/21, 9/18, ___ ?

Options:
(a) 11/15
(b) 15/12
(c) 13/12
(d) 12/16
(e) 15/10

Answer: (a) 11/15

Explanation: Numerator increases by 2 while denominator decreases by 3.

Question 46

Complete the series: 5, 24, 61, ___ ?

Options:
(a) 125
(b) 120
(c) 122
(d) 127
(e) 140

Answer: (a) 125

Explanation: Pattern follows n³ + 0.

Question 47

Complete the series: 2, 2, A, 4, 3, C, 6, E, 8, G, 10, ___ ?

Options:
(a) 13, I
(b) L, 13
(c) 14, J
(d) 13, L
(e) 14, H

Answer: (d) 13, L

Explanation: Numbers increase by +2 and letters follow alphabetical order.

Question 48

If B’s shadow was exactly to the left of A, which direction was A facing?

Options:
(a) East
(b) West
(c) North
(d) South
(e) North west

Answer: (c) North

Explanation: Shadow on left means sun in east, so A faces north.

Question 49

Find next: D, 8, F, 27, I, 64, ___ , R ?

Options:
(a) 125, M
(b) 97, M
(c) N, 144
(d) M, 125
(e) 87, O

Answer: (d) M, 125

Explanation: Letters skip increasing positions and numbers are cubes.

Question 50

Find odd

Options:
(a) Well & Woe
(b) Disloyal & Treacherous
(c) Extravagant & Loutish
(d) Happy & Glad
(e) Want & Need

Answer: (c) Extravagant & Loutish

Explanation: Others are synonyms, this pair is not.

Question 51

By dividing a number by 6 and then adding 13, we get 19. What is the number?

Options:
(a) 56
(b) 36
(c) 63
(d) 75
(e) 65

Answer: (b) 36

Explanation: 36 ÷ 6 + 13 = 19.

Question 52

If Iron is to Wood, then ___ is to Carpenter

Options:
(a) Goldsmith
(b) Beggar
(c) Ornaments
(d) Blacksmith
(e) Both a & b

Answer: (d) Blacksmith

Explanation: Iron is worked by a blacksmith just like wood by a carpenter.

Question 53

If some electric poles stand in a straight row 1.25 km apart, what is the distance from 1st to 10th?

Options:
(a) 11,125 m
(b) 1000 m
(c) 11,250 m
(d) 10,125 m
(e) 11 km

Answer: (a) 11,125 m

Explanation: Distance = (number − 1) × gap = 9 × 1.25 km.

Question 54

Doctors advised to take a pill every hour. How much time requires taking 10 pills?

Options:
(a) 8 hours
(b) 9 hours
(c) 10 hours
(d) 11 hours
(e) none

Answer: (b) 9 hours

Explanation: First pill is taken immediately, so only 9 intervals are needed.

Question 55

Find odd

Options:
(a) Mathematics & algebra
(b) Petals & flowers
(c) Pages & book
(d) Water & wind
(e) Jute & gunny bag

Answer: (d) Water & wind

Explanation: Others have a part–whole or material–product relationship.

Question 56

Complete the series: 5, 20, 6, 24, 7, 28, ___ , ___ ?

Options:
(a) 32, 10
(b) 28, 32
(c) 8, 32
(d) 8, 36
(e) 10, 32

Answer: (c) 8, 32

Explanation: First number increases by 1 and second is multiplied by 4.

Question 57

Drop is to Ocean as ___ is to Star

Options:
(a) Sun
(b) Blue
(c) Earth
(d) Sky
(e) Planet

Answer: (a) Sun

Explanation: A star is made of suns just as an ocean is made of drops.

Question 58

Which one is odd?

Options:
(a) Agree & Reject
(b) Control & Open
(c) Well & Woe
(d) Jump & Obstacle
(e) Well & Decent

Answer: (e) Well & Decent

Explanation: All other pairs show opposition or contrast, but this pair does not.

Question 59

If 4×6 = 12, 5×8 = 20 and 16×5 = 40, then 24×4 = ?

Options:
(a) 44
(b) 48
(c) 84
(d) 69
(e) 96

Answer: (b) 48

Explanation: The operation is half of the actual multiplication result.

Question 60

Sunday is to Tuesday as Saturday is to ___ ?

Options:
(a) Fri
(b) Thu
(c) Wed
(d) Mon
(e) Sun

Answer: (d) Mon

Explanation: The relationship is a forward shift of two days.

Question 61

March is to August as June is to ___ ?

Options:
(a) July
(b) April
(c) November
(d) May
(e) March

Answer: (c) November

Explanation: Both pairs are five months apart.

Question 62

Find odd

Options:
(a) Student & Teacher
(b) Science & Robot
(c) Book & Page
(d) Tailor & Gentle
(e) Car & Driver

Answer: (d) Tailor & Gentle

Explanation: All others show functional relationships except this pair.

Question 63

Complete the series: 2, 4, 7, 9, 12, 14, 17, ___ , ___ ?

Options:
(a) 19, 22
(b) 18, 22
(c) 19, 25
(d) 22, 18
(e) 24, 19

Answer: (a) 19, 22

Explanation: The pattern alternates between +2 and +3.

Question 64

Rearrange: MNISAJE = Name of a flower (Middle Letter)

Options:
(a) A
(b) F
(c) M
(d) S
(e) J

Answer: (a) A

Explanation: The word rearranges to “JASMINE” whose middle letter is A.

Question 65

Complete the series: 1, 4, 2, 5, 3, 6, 4, 7, ___ , ___ ?

Options:
(a) 3, 6
(b) 5, 8
(c) 8, 6
(d) 5, 7
(e) 6, 8

Answer: (e) 6, 8

Explanation: Two increasing sequences are interwoven.

Question 66

Complete the series: 2, 5, 4, 7, 6, ___ , ___ ?

Options:
(a) 12, 10
(b) 10, 9
(c) 13, 15
(d) 8, 7
(e) 9, 8

Answer: (e) 9, 8

Explanation: Odd terms increase by 2 and even terms increase by 2.

Question 67

Insert the missing alphabet: (B A D), (C A T), (___ O G)

Options:
(a) G
(b) E
(c) D
(d) F
(e) O

Answer: (d) F

Explanation: Each group forms an animal name alphabetically.

Question 68

Rearrange: URSLEONWF (Plant), find the 2nd last letter

Options:
(a) S
(b) E
(c) U
(d) C
(e) M

Answer: (b) E

Explanation: The word rearranges to “SUNFLOWER” whose second last letter is E.

Question 69

Find the odd

Options:
(a) 429
(b) 213
(c) 1452
(d) 137
(e) 273

Answer: (d) 137

Explanation: All others are divisible by 3 except 137.

Question 70

Rohingya is from ___ ?

Options:
(a) Africa
(b) Armenia
(c) Arakan
(d) Naypyidaw
(e) Tibet

Answer: (c) Arakan

Explanation: Rohingyas historically originate from the Arakan region.

Question 71

Complete the series: 7, 21, 6, 17, 5, 13, ___ , ___ ?

Options:
(a) 5, 10
(b) 12, 15
(c) 8, 12
(d) 6, 11
(e) 4, 9

Answer: (e) 4, 9

Explanation: The first sequence decreases by 1 and the second decreases by 4.

Question 72

If 6145 stands for FADE, what would be the code for EBB?

Options:
(a) 522
(b) 322
(c) 655
(d) 532
(e) 622

Answer: (b) 322

Explanation: Letters are replaced by their alphabetical positions.

Question 73

Complete the series: 8, 4, 32, 7, 5, ___ , ___ ?

Options:
(a) 34, 7
(b) 35, 6
(c) 25, 4
(d) 28, 3
(e) 28, 6

Answer: (e) 28, 6

Explanation: Pattern follows multiply and then reduce sequence.

Question 74

The greatest mileage of railway ___ ?

Options:
(a) Russia
(b) China
(c) India
(d) Egypt
(e) USA

Answer: (a) Russia

Explanation: Russia has the longest railway network coverage.

Question 75

Insert the alphabet: A, F, K, P, ___ , ___ ?

Options:
(a) A, C
(b) U, Y
(c) Y, D
(d) U, Z
(e) S, X

Answer: (b) U, Y

Explanation: Each letter increases by 5 positions.

Question 76

9, A, 16, D, 25, G, 36, I, 82, N, ___ , ___ ?

Options:
(a) 101, S
(b) 90, P
(c) 95, U
(d) 100, T
(e) 98, O

Answer: (d) 100, T

Explanation: Numbers are perfect squares and letters follow skipping pattern.

Question 77

If A:B = 3:4, B:C = 5:6 and C:D = 11:9, what is A:D?

Options:
(a) 45/70
(b) 55/72
(c) 55/75
(d) 33/39
(e) 50/70

Answer: (b) 55/72

Explanation: Ratios are combined step by step using multiplication.

Question 78

D, 37, E, 50, G, 65, J, 82, N, ___ , ___ ?

Options:
(a) 101, S
(b) 90, P
(c) 95, U
(d) 100, T
(e) 98, O

Answer: (a) 101, S

Explanation: Numbers increase by odd increments and letters jump progressively.

Question 79

This picture is the mother of my son's mother. What is the relation?

Options:
(a) Uncle
(b) Mother in law
(c) Father in law
(d) Sister
(e) Mother

Answer: (e) Mother

Explanation: My son’s mother is my wife, so her mother is my mother.

Question 80

2, E, 5, I, 10, M, ___ , ___ , 26, U ?

Options:
(a) 17, S
(b) 14, R
(c) 15, Q
(d) 17, Q
(e) 20, V

Answer: (d) 17, Q

Explanation: Numbers follow +3, +5, +7 and letters skip 4.

Question 81

If 4×6 = 12, 5×8 = 20, 8×12 = 48, then 9×14 = ?

Options:
(a) 73
(b) 58
(c) 63
(d) 89
(e) 101

Answer: (c) 63

Explanation: The rule is half of the product.

Question 82

Rearrange: “vessel empty little sounds”

Options:
(a) True
(b) None
(c) Both
(d) False
(e) Can’t tell

Answer: (a) True

Explanation: It rearranges to the proverb “Empty vessels make much noise.”

Question 83

If 4517 stands for DEAD then IDEA stands for ?

Options:
(a) 4145
(b) 3978
(c) 9452
(d) 3758
(e) 9451

Answer: (a) 4145

Explanation: Letters are replaced by reverse alphabetical positions.

Question 84

Electric poles are 60 yards apart; distance from 1st to 9th pole?

Options:
(a) 600 yards
(b) 540 yards
(c) 1000 yards
(d) 480 yards
(e) 320 yards

Answer: (d) 480 yards

Explanation: Distance equals 8 gaps multiplied by 60 yards.

Question 85

Complete series: 1, 1/2, 1/4, ___ , ___ ?

Options:
(a) 1/8, 1/12
(b) 0.20, 0.80
(c) 1/32, 1/16
(d) 1/16, 1/48
(e) 1/8, 1/16

Answer: (e) 1/8, 1/16

Explanation: Each term is half of the previous one.

Question 86

Dog is to barking as cat is to ___ ?

Options:
(a) Snoring
(b) Mewing
(c) Mowing
(d) Chewing

Answer: (b) Mewing

Explanation: It refers to the sound made by the animal.

Question 87

Complete series: A, 3, B, 12, C, 48, ___ , ___ ?

Options:
(a) D, 64
(b) D, 192
(c) D, 128
(d) E, 156
(e) F, 192

Answer: (b) D, 192

Explanation: Letters increase alphabetically and numbers multiply by 4.

Question 88

If 6× = 18, 7× = 28, 8× = 40 then 12× = ?

Options:
(a) 56
(b) 98
(c) 136
(d) 120
(e) 108

Answer: (e) 108

Explanation: The result equals n × (n + 3).

Question 89

If 1385 stands for ACHE, what does 4554 stand for?

Options:
(a) DEED
(b) CHIR
(c) EHAC
(d) CEHA
(e) BHIR

Answer: (a) DEED

Explanation: Each digit represents alphabetical position.

Question 90

Quran is to Muslim as Bible is to ___ ?

Options:
(a) Hindu
(b) Buddha
(c) Christian
(d) Siah
(e) Muslim

Answer: (c) Christian

Explanation: Each holy book is linked to its followers.

Question 91

Rearrange: MAHEMR (Tools), find the second letter

Options:
(a) H
(b) M
(c) R
(d) A
(e) E

Answer: (a) H

Explanation: The word rearranges to “HAMMER”.

Question 92

Insert the missing alphabet: T, Q, N, K, ___ , ___ ?

Options:
(a) F, X
(b) S, T
(c) Q, C
(d) H, E
(e) P, X

Answer: (d) H, E

Explanation: Letters decrease by three positions each time.

Question 93

February is to March as Saturday is to ___ ?

Options:
(a) S
(b) M
(c) T
(d) W
(e) F

Answer: (c) T

Explanation: Both represent the next unit in sequence.

Question 94

A man says: “I have no sister or brother but that woman’s father is my father’s daughter.” What relation is he to me?

Options:
(a) Daughter
(b) Mother
(c) Sister
(d) Brother
(e) Father

Answer: (e) Father

Explanation: The woman’s father is his wife, so he is my father.


Question 95

Tuesday is March as Saturday is to ___ ?

Options:
(a) May
(b) July
(c) June
(d) August
(e) September

Answer: (c) June

Explanation: Tuesday is the 3rd day and March is the 3rd month, so Saturday (6th day) maps to June (6th month).

Question 96

If 2×3 = 46 and 5×4 = 2520, then 7×6 = ?

Options:
(a) 4942
(b) 4952
(c) 4542
(d) 8942
(e) 4972

Answer: (a) 4942

Explanation: The pattern is first number squared followed by the product of both numbers.

Question 97

Medicine is dispensary as ___ is to laboratory

Options:
(a) Resource
(b) Chemicals
(c) Instruments
(d) Practical
(e) Lab

Answer: (b) Chemicals

Explanation: A dispensary stores medicine just as a laboratory stores chemicals.

Question 98

Design is to Architect as ___ is to author

Options:
(a) Book
(b) Story
(c) Poem
(d) Movie
(e) Music

Answer: (a) Book

Explanation: An architect creates designs and an author creates books.

Question 99

Insert the missing figures: 35, 27, 20, 14, 9, ___ , ___ ?

Options:
(a) 0, 4
(b) 5, 2
(c) 4, 5
(d) 7, 9
(e) 6, 7

Answer: (b) 5, 2

Explanation: The sequence decreases by 8, 7, 6, 5, 4, and then 3.

Question 100

Rearrange: DAMRIGOL (second letter)

Options:
(a) G
(b) O
(c) L
(d) A
(e) D

Answer: (d) A

Explanation: The word rearranges to “MARIGOLD” whose second letter is A.
"""
    
    
    # Process the raw text using regex to separate questions
    # The format allows for "Question XX" header.
    # Logic: Split by "Question XX", then parse sections within.
    
    # Clean up and normalize
    questions_raw = questions_raw.strip()
    
    # Split by "Question" followed by number
    # Use capturing group to keep the delimiter to verify if needed, or just split
    # Regex: \nQuestion\s+\d+
    blocks = re.split(r'Question\s+\d+', questions_raw)
    
    # First block might be empty if file starts with Question 01
    blocks = [b.strip() for b in blocks if b.strip()]
    
    print(f"Parsing {len(blocks)} questions for {set10.name}...")
    
    start_bank_order = 901
    count = 0
    
    for idx, block in enumerate(blocks, 1):
        try:
            # Strategies to find sections
            # 1. Explanation (last part)
            # 2. Answer (before Explanation)
            # 3. Options (before Answer)
            # 4. Question Text (Everything else at start)
            
            # Find Explanation
            explanation_split = block.split('Explanation:')
            if len(explanation_split) > 1:
                explanation_text = explanation_split[1].strip()
                remainder = explanation_split[0]
            else:
                explanation_text = ""
                remainder = block
            
            # Find Answer
            answer_split = remainder.split('Answer:')
            if len(answer_split) > 1:
                answer_text = answer_split[1].strip()
                remainder = answer_split[0]
            else:
                answer_text = ""
                # Try finding valid answer format pattern like "(a) ..." at end
                pass
                
            # Find Options
            options_split = remainder.split('Options:')
            if len(options_split) > 1:
                options_text = options_split[1].strip()
                q_text_raw = options_split[0].strip()
            else:
                options_text = ""
                q_text_raw = remainder.strip()
            
            # Clean Question Text
            # Remove "Question:" prefix if it exists
            if q_text_raw.lower().startswith('question:'):
                q_text = q_text_raw[9:].strip()
            else:
                q_text = q_text_raw
            
            # clean possible headers like "Question 01" if split failed to remove them completely? 
            # (Our split removed the delimiter, so we are good)
            
            # Parse Options
            # Format could be (a) ... (b) ... inline or newlines
            # Regex to find (char) content
            # We look for (a), (b), (c), (d), (e)
            options_list = []
            
            # This regex looks for (x) followed by any text until the next (y) or end of string
            # It uses lookahead to stop at the next pattern
            tokens = re.split(r'(\([a-e]\))', options_text)
            # tokens will be ['', '(a)', ' value ', '(b)', ' value ', ...]
            
            current_id = None
            for token in tokens:
                token = token.strip()
                if not token: continue
                
                if re.match(r'\([a-e]\)', token):
                    current_id = token[1].lower() # extract char
                elif current_id:
                    # This is the value
                    val = token.strip(',').strip()
                    options_list.append({"id": current_id, "text": val})
                    current_id = None
            
            # Fallback if regex split didn't find structure (e.g. simple layout)
            if not options_list:
                 # Try simple findall for standard format
                 matches = re.findall(r'\(([a-e])\)\s*([^()]+)', options_text)
                 for m in matches:
                     options_list.append({"id": m[0].lower(), "text": m[1].strip()})
            
            # Parse Answer
            # Look for (a)
            correct_match = re.search(r'\(([a-e])\)', answer_text)
            correct_answer = ""
            if correct_match:
                correct_answer = correct_match.group(1).lower()

            # Create Question object
            Question.objects.update_or_create(
                test=set10,
                order=idx,
                defaults={
                    "question_text": q_text,
                    "question_type": "mcq",
                    "options": options_list,
                    "correct_answer": correct_answer,
                    "explanation": explanation_text,
                    "difficulty_level": "medium",
                    "bank_order": start_bank_order + (idx - 1)
                }
            )
            count += 1
            if count % 10 == 0:
                print(f"  Processed {count} questions...")
                
        except Exception as e:
            print(f"Error parsing block {idx}: {e}")
            # print(f"Block content: {block[:50]}...")

    
    print(f"\n✓ Successfully created {count} questions for {set10.name}!")
    print(f"  Total questions in database: {Question.objects.filter(test=set10).count()}")
    
    return set10

if __name__ == "__main__":
    parse_and_create_set10()
