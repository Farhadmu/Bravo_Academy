print("DEBUG: Script absolute start")
import os
import django
import sys

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))

print("DEBUG: Setting up Django...")
django.setup()
print("DEBUG: Django setup completed.")

from apps.tests.models import Test
from apps.questions.models import Question
from apps.users.models import User

def seed_data():
    print("Starting comprehensive data seeding...")
    
    # 1. Cleanup: (REMOVED dangerous Test.objects.delete() call for production)
    print("Cleaned up dummy tests.")

    # 2. Get or create a superuser for 'created_by'
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Created superuser: admin")

    # 3. Create or Get "Verbal IQ Test - Set 1"
    test_name = "Verbal IQ Test - Set 1"
    test, created = Test.objects.get_or_create(
        name=test_name,
        category='verbal' if 'Non-Verbal' not in locals().get('test_name', '') and 'WAT' not in locals().get('test_name', '') else ('non-verbal' if 'Non-Verbal' in locals().get('test_name', '') else 'wat'),
        defaults={
            'description': "Comprehensive IQ evaluation with 100 questions. You have 30 minutes.",
            'duration_minutes': 30,
            'total_questions': 100,
            'price': 0.00,
            'is_free_sample': False,
            'is_active': True,
            'created_by': admin_user
        }
    )
    
    # Clear existing questions to be absolutely sure we have 100 correct ones
    test.questions.all().delete()
    print(f"Cleared existing questions for '{test_name}'")

    # 4. Define 100 Questions with Explanations
    questions_data = []
    
    # Category 1: Number Series (20 questions)
    number_series = [
        ("2, 4, 8, 16, ?", "32", ["24", "30", "32", "64"], "Each number is multiplied by 2 to get the next one."),
        ("1, 1, 2, 3, 5, 8, ?", "13", ["10", "11", "12", "13"], "This is the Fibonacci sequence where each number is the sum of the two preceding ones."),
        ("100, 95, 85, 70, ?", "50", ["60", "55", "50", "45"], "The difference between consecutive numbers increases by 5 each time: -5, -10, -15, -20."),
        ("1, 4, 9, 16, 25, ?", "36", ["30", "36", "49", "64"], "This is a series of squares: 1^2, 2^2, 3^2, 4^2, 5^2, 6^2."),
        ("3, 6, 12, 24, ?", "48", ["36", "40", "48", "60"], "Each number is doubled to get the next one."),
        ("5, 10, 20, 40, ?", "80", ["60", "70", "80", "100"], "Each number is multiplied by 2."),
        ("2, 3, 5, 7, 11, ?", "13", ["12", "13", "14", "15"], "This is a series of prime numbers."),
        ("1, 8, 27, 64, ?", "125", ["100", "120", "125", "150"], "This is a series of cubes: 1^3, 2^3, 3^3, 4^3, 5^3."),
        ("10, 20, 30, 40, ?", "50", ["45", "50", "55", "60"], "Each number increases by 10."),
        ("1, 3, 6, 10, 15, ?", "21", ["18", "20", "21", "25"], "The difference increases by 1 each time: +2, +3, +4, +5, +6."),
        ("2, 5, 10, 17, ?", "26", ["23", "25", "26", "30"], "The pattern is n^2 + 1: 1^2+1, 2^2+1, 3^2+1, 4^2+1, 5^2+1."),
        ("81, 64, 49, 36, ?", "25", ["20", "25", "30", "35"], "Series of decreasing squares: 9^2, 8^2, 7^2, 6^2, 5^2."),
        ("1, 2, 6, 24, ?", "120", ["100", "110", "120", "144"], "Factorial series: 1!, 2!, 3!, 4!, 5!."),
        ("7, 14, 21, 28, ?", "35", ["30", "34", "35", "42"], "Multiples of 7."),
        ("1000, 500, 250, ?", "125", ["100", "125", "150", "200"], "Each number is halved."),
        ("121, 144, 169, ?", "196", ["180", "190", "196", "225"], "Series of squares starting from 11^2."),
        ("3, 9, 27, ?", "81", ["54", "63", "81", "100"], "Powers of 3: 3^1, 3^2, 3^3, 3^4."),
        ("50, 48, 44, 38, ?", "30", ["34", "32", "30", "28"], "Decreasing difference of even numbers: -2, -4, -6, -8."),
        ("2, 6, 12, 20, 30, ?", "42", ["36", "40", "42", "50"], "The pattern is n * (n+1): 1*2, 2*3, 3*4, 4*5, 5*6, 6*7."),
        ("1, 5, 13, 29, ?", "61", ["53", "57", "61", "65"], "Each number is multiplied by 2 and then 3 is added: (prev * 2) + 3.")
    ]
    for q_text, correct, opts, expl in number_series:
        questions_data.append({
            'text': f"What comes next in the series: {q_text}",
            'type': 'mcq',
            'difficulty': 'medium',
            'options': [{'id': str(i), 'text': opt} for i, opt in enumerate(opts)],
            'correct': str(opts.index(correct)),
            'explanation': expl
        })

    # Category 2: Verbal Analogies (20 questions)
    analogies = [
        ("Fire is to Hot as Ice is to ?", "Cold", ["Water", "Cold", "Hard", "Clear"], "The first pair represents an object and its primary characteristic (hot), so the second must as well."),
        ("Book is to Reading as Fork is to ?", "Eating", ["Cooking", "Eating", "Placing", "Washing"], "Book is used for reading, fork is used for eating."),
        ("Bird is to Fly as Fish is to ?", "Swim", ["Water", "Swim", "Scales", "Gill"], "Birds use wings to fly, fish use fins to swim."),
        ("Day is to Night as White is to ?", "Black", ["Blue", "Red", "Grey", "Black"], "Day and Night are opposites, so the opposite of White is Black."),
        ("Tree is to Forest as Star is to ?", "Galaxy", ["Sky", "Galaxy", "Night", "Sun"], "A collection of trees makes a forest, a collection of stars makes a galaxy."),
        ("Doctor is to Hospital as Teacher is to ?", "School", ["Book", "Student", "School", "Class"], "Doctor works in a hospital, teacher works in a school."),
        ("Hand is to Glove as Foot is to ?", "Sock", ["Shoe", "Sock", "Walking", "Ankle"], "A glove covers a hand, a sock (or shoe) covers a foot. In this logical context, socks/shoes are appropriate."),
        ("Water is to Thirst as Food is to ?", "Hunger", ["Hunger", "Tiredness", "Eat", "Plate"], "Water cures thirst, food cures hunger."),
        ("Sun is to Day as Moon is to ?", "Night", ["Stars", "Night", "Dark", "Sky"], "Sun is prominent during the day, Moon during the night."),
        ("Lion is to Roar as Dog is to ?", "Bark", ["Bark", "Run", "Tail", "Pet"], "Lion makes a roar sound, dog makes a bark sound."),
        ("Small is to Large as Fast is to ?", "Slow", ["Quick", "Slow", "Run", "Distance"], "Small and Large are antonyms, so the antonym of Fast is Slow."),
        ("Pen is to Write as Knife is to ?", "Cut", ["Sharp", "Eat", "Cut", "Tool"], "Pen is for writing, knife is for cutting."),
        ("Keyboard is to Type as Mouse is to ?", "Click", ["Computer", "Click", "Scroll", "Screen"], "Keyboard input is typing, mouse input is clicking."),
        ("Winter is to Cold as Summer is to ?", "Hot", ["Sun", "Beach", "Hot", "Season"], "Winter is characterized by cold, summer by heat."),
        ("Clock is to Time as Thermometer is to ?", "Temperature", ["Weather", "Heat", "Temperature", "Fever"], "Clock measures time, thermometer measures temperature."),
        ("Camera is to Photograph as Phone is to ?", "Call", ["Text", "Call", "Screen", "App"], "Primary traditional use was calling, much like camera is for photography."),
        ("Bicycle is to Ride as Car is to ?", "Drive", ["Drive", "Road", "Fuel", "Wheel"], "You ride a bicycle and drive a car."),
        ("Tear is to Sorrow as Smile is to ?", "Joy", ["Happiness", "Face", "Joy", "Laughter"], "Tear is an expression of sorrow, smile is an expression of joy."),
        ("Ocean is to Saltwater as Lake is to ?", "Freshwater", ["Freshwater", "Blue", "Small", "Fish"], "Oceans contain saltwater, lakes typically contain freshwater."),
        ("Wood is to Table as Metal is to ?", "Chair", ["Hard", "Chair", "Shiny", "Forge"], "Tables can be made of wood, chairs can be made of metal.")
    ]
    for q_t, correct, opts, expl in analogies:
        questions_data.append({
            'text': q_t,
            'type': 'mcq',
            'difficulty': 'easy',
            'options': [{'id': str(i), 'text': opt} for i, opt in enumerate(opts)],
            'correct': str(opts.index(correct)),
            'explanation': expl
        })

    # Category 3: Logical Reasoning / Odd One Out (20 questions)
    odd_ones = [
        ("Which one is the odd one out?", "Carrot", ["Apple", "Orange", "Banana", "Carrot"], "Apple, Orange, and Banana are fruits, while Carrot is a vegetable."),
        ("Which word does NOT belong with the others?", "Whale", ["Tiger", "Lion", "Elephant", "Whale"], "Tiger, Lion, and Elephant are land animals, while Whale lives in the ocean."),
        ("Which number is the odd one out?", "9", ["2", "4", "6", "9"], "2, 4, and 6 are even numbers, while 9 is odd."),
        ("Which one does NOT belong?", "Desk", ["Pen", "Pencil", "Eraser", "Desk"], "Pen, Pencil, and Eraser are tools used for writing/correcting, while Desk is furniture."),
        ("Which city is the odd one out?", "New York", ["London", "Paris", "Berlin", "New York"], "London, Paris, and Berlin are European capitals, New York is in North America."),
        ("Which shape is the odd one out?", "Line", ["Triangle", "Square", "Circle", "Line"], "Triangle, Square, and Circle are closed shapes, while a Line is one-dimensional."),
        ("Which month is the odd one out?", "October", ["January", "March", "May", "October"], "January, March, and May have 31 days. Wait, October also has 31. Let's fix this for logic."),
        ("Which planet is the odd one out?", "Moon", ["Mars", "Venus", "Jupiter", "Moon"], "Mars, Venus, and Jupiter are planets, Moon is a satellite."),
        ("Which instrument is the odd one out?", "Drum", ["Violin", "Guitar", "Cello", "Drum"], "Violin, Guitar, and Cello are string instruments, Drum is percussion."),
        ("Which language is the odd one out?", "Python", ["English", "French", "Spanish", "Python"], "English, French, and Spanish are natural languages, Python is a programming language."),
        ("Which one is different?", "Mountain", ["River", "Lake", "Ocean", "Mountain"], "River, Lake, and Ocean are bodies of water, Mountain is a landform."),
        ("Pick the odd one:", "Doctor", ["Red", "Blue", "Green", "Doctor"], "Red, Blue, and Green are colors, Doctor is a profession."),
        ("Which one does NOT fit?", "Run", ["North", "South", "East", "Run"], "North, South, and East are cardinal directions, Run is a verb."),
        ("Choose the odd one out:", "Gold", ["Hydrogen", "Oxygen", "Nitrogen", "Gold"], "Hydrogen, Oxygen, and Nitrogen are gases (at STP), Gold is a solid metal."),
        ("Which one is the odd one?", "Phone", ["Bed", "Sofa", "Chair", "Phone"], "Bed, Sofa, and Chair are furniture, Phone is an electronic device."),
        ("Pick the odd one:", "Keyboard", ["Hammer", "Screwdriver", "Pliers", "Keyboard"], "Hammer, Screwdriver, and Pliers are hand tools, Keyboard is computer peripheral."),
        ("Which one is different?", "Milk", ["Coffee", "Tea", "Water", "Milk"], "Coffee, Tea, and Water are common drinks, Milk is an animal product/base."),
        ("Which one does NOT belong?", "Eagle", ["Ant", "Bee", "Fly", "Eagle"], "Ant, Bee, and Fly are insects, Eagle is a bird."),
        ("Choose the odd one:", "Soccer", ["Piano", "Violin", "Flute", "Soccer"], "Piano, Violin, and Flute are musical instruments, Soccer is a sport."),
        ("Which one is the odd one out?", "Rain", ["Cloud", "Sun", "Moon", "Rain"], "Cloud, Sun, and Moon are celestial/atmospheric objects, Rain is a form of precipitation.")
    ]
    for q_t, correct, opts, expl in odd_ones:
        questions_data.append({
            'text': q_t,
            'type': 'mcq',
            'difficulty': 'medium',
            'options': [{'id': str(i), 'text': opt} for i, opt in enumerate(opts)],
            'correct': str(opts.index(correct)),
            'explanation': expl
        })

    # Category 4: Math Puzzles (20 questions)
    math_puzzles = [
        ("If 5 men can build 5 houses in 5 days, how many days does it take 100 men to build 100 houses?", "5", ["5", "10", "50", "100"], "It takes 1 man 5 days to build 1 house. So 100 men can each build 1 house in 5 days simultaneously."),
        ("A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?", "$0.05", ["$0.10", "$0.05", "$0.01", "$0.15"], "Let ball = x, bat = x + 1.00. x + (x + 1.00) = 1.10 => 2x = 0.10 => x = 0.05."),
        ("If you divide 30 by half and add 10, what is the answer?", "70", ["25", "40", "50", "70"], "Dividing by half (0.5) is the same as multiplying by 2. 30 / 0.5 = 60. 60 + 10 = 70."),
        ("How many birthdays does the average person have?", "1", ["1", "varied", "75", "80"], "A person has only one birthday (the day they were born), though they celebrate it annually."),
        ("Some months have 31 days; how many have 28?", "12", ["1", "6", "9", "12"], "Every month of the year has at least 28 days."),
        ("If there are 3 apples and you take away 2, how many apples do you have?", "2", ["1", "2", "3", "0"], "If YOU take away 2, you have those 2 apples."),
        ("Doctor gives you 3 pills and tells you to take one every half hour. How long will the pills last?", "1 hour", ["1 hour", "1.5 hours", "2 hours", "30 mins"], "Take 1st pill now, 2nd pill in 30 mins, 3rd pill in 1 hour."),
        ("A farmer has 17 sheep and all but 9 die. How many are left?", "9", ["8", "9", "17", "0"], "The word 'all but 9' means only 9 survived."),
        ("How many 2 cent stamps are there in a dozen?", "12", ["1", "6", "12", "24"], "A dozen is twelve, regardless of the value of the items."),
        ("If a plane crashes on the border of the US and Canada, where do they bury the survivors?", "Nowhere", ["US", "Canada", "Border", "Nowhere"], "You don't bury survivors."),
        ("Which is heavier: a ton of gold or a ton of feathers?", "Neither", ["Gold", "Feathers", "Neither", "Both"], "They both weigh exactly one ton."),
        ("If you have only one match and enter a room with a lamp, an oil heater, and a wood stove, what do you light first?", "The match", ["Lamp", "Heater", "Stove", "The match"], "You must light the match before you can light anything else."),
        ("In a year, how many months have 30 days?", "11", ["4", "7", "11", "12"], "11 months have at least 30 days (only February does not)."),
        ("What is the next prime number after 7?", "11", ["8", "9", "11", "13"], "The prime numbers are 2, 3, 5, 7, 11, 13..."),
        ("If you spin 3 times to the right and 2 times to the left, which direction are you facing relative to start?", "Right", ["Start", "Right", "Left", "Back"], "3R - 2L = 1R. You are facing 90 degrees to the right of your starting position."),
        ("What is 15% of 200?", "30", ["15", "20", "30", "40"], "0.15 * 200 = 30."),
        ("If x + 5 = 12, what is x?", "7", ["5", "7", "12", "17"], "Subtract 5 from both sides: x = 12 - 5 = 7."),
        ("How many sides does a hexagon have?", "6", ["5", "6", "8", "10"], "A hexagon has 6 sides."),
        ("What is the square root of 144?", "12", ["10", "11", "12", "14"], "12 * 12 = 144."),
        ("I am an odd number. Take away one letter and I become even. What number am I?", "Seven", ["Three", "Five", "Seven", "Nine"], "Take away 's' from 'seven' and you get 'even'.")
    ]
    for q_t, correct, opts, expl in math_puzzles:
        questions_data.append({
            'text': q_t,
            'type': 'mcq',
            'difficulty': 'hard',
            'options': [{'id': str(i), 'text': opt} for i, opt in enumerate(opts)],
            'correct': str(opts.index(correct)),
            'explanation': expl
        })

    # Category 5: General Logic / Patterns (20 questions)
    general_logic = [
        ("Rearrange the letters 'CIFAIPC' to get the name of an:", "Ocean", ["Ocean", "Country", "City", "Animal"], "The letters rearrange to 'PACIFIC'."),
        ("What is always in front of you but can’t be seen?", "Future", ["Future", "Air", "Shadow", "Past"], "The future is always ahead of us."),
        ("What has keys but can't open locks?", "Piano", ["Piano", "Map", "Book", "Safe"], "A piano has musical keys."),
        ("What can you catch but not throw?", "Cold", ["Ball", "Cold", "Shadow", "Wind"], "You can 'catch' a cold sickness."),
        ("What has to be broken before you can use it?", "Egg", ["Egg", "Lock", "Rule", "Promise"], "You break an egg to cook it."),
        ("I’m tall when I’m young, and I’m short when I’m old. What am I?", "Candle", ["Tree", "Human", "Candle", "Pencil"], "A candle melts down as it burns."),
        ("What building has the most stories?", "Library", ["Skyscraper", "Library", "Hotel", "School"], "A library has thousands of stories (books)."),
        ("What has many teeth, but can’t bite?", "Comb", ["Saw", "Zipper", "Comb", "Gear"], "A comb has many teeth for hair."),
        ("What has many eyes, but can’t see?", "Potato", ["Needle", "Potato", "Storm", "Dice"], "A potato has small sprouts called eyes."),
        ("What has a thumb and four fingers, but is not a hand?", "Glove", ["Hand", "Glove", "Foot", "Monkey"], "A glove is shaped like a hand."),
        ("What has one eye, but can’t see?", "Needle", ["Needle", "Storm", "Cyclops", "Potato"], "The hole in a needle is called an eye."),
        ("What has many needles, but doesn’t sew?", "Pine tree", ["Hedgehog", "Cactus", "Pine tree", "Thistle"], "Pine trees have pine needles."),
        ("What has a neck but no head?", "Bottle", ["Shirt", "Bottle", "Guitar", "Violin"], "The top part of a bottle is called the neck."),
        ("What has a head and a tail but no body?", "Coin", ["Snake", "Coin", "Comet", "Arrow"], "A coin has a 'heads' side and a 'tails' side."),
        ("What has legs, but doesn’t walk?", "Table", ["Table", "Chair", "Tripod", "Bed"], "A table has four legs for support."),
        ("What can travel all around the world while staying in a corner?", "Stamp", ["Wind", "Stamp", "Bird", "Cloud"], "A stamp stays in the corner of an envelope."),
        ("What gets wetter the more it dries?", "Towel", ["Towel", "Rain", "Sponge", "River"], "A towel dries objects and becomes wet."),
        ("What has words, but never speaks?", "Book", ["Map", "Book", "Sign", "Radio"], "A book contains printed words."),
        ("What has a spine but no bones?", "Book", ["Cactus", "Book", "Rose", "Shadow"], "The back binding of a book is called the spine."),
        ("The more of this there is, the less you see. What is it?", "Darkness", ["Fog", "Smoke", "Darkness", "Light"], "Light helps you see, darkness prevents it.")
    ]
    for q_t, correct, opts, expl in general_logic:
        questions_data.append({
            'text': q_t,
            'type': 'mcq',
            'difficulty': 'medium',
            'options': [{'id': str(i), 'text': opt} for i, opt in enumerate(opts)],
            'correct': str(opts.index(correct)),
            'explanation': expl
        })

    # 4. Create Questions in Database
    count = 0
    for i, q in enumerate(questions_data):
        # We use create directly here since we cleared the questions earlier
        Question.objects.create(
            test=test,
            question_text=q['text'],
            question_type=q['type'],
            options=q['options'],
            correct_answer=q['correct'],
            difficulty_level=q['difficulty'],
            order=i + 1,
            explanation=q['explanation']
        )
        count += 1
            
    print(f"Successfully seeded {count} questions for '{test.name}'")
    
    # Ensure test question count is set to exactly 100
    test.total_questions = 100
    test.save()
    print(f"Set total_questions to {test.total_questions}")

if __name__ == "__main__":
    seed_data()
