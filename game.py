import csv
import random
import os

random_number = 0
serial_numbers = []
questions = []
difficulties = []
ans_serial_numbers = []
option1 = []
option2 = []
option3 = []
option4 = []
correctanswer = []

# LIFE LINES
change_question = 1
change_option = 1
player_name = ""
select_index = set()
correctanswer_count = 0
price_own = 0

# Questions file
file_path = '/Users/abhay/Documents/flask/website/questions.csv'
#correct_answer = os.path.abspath('/Users/abhay/Documents/flask/website/correctanswers.csv')


def which_lifeline_available():
    return change_question, change_option

# Read questions file into variables
with open(file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Extract data from each row
        serial_number, question_text, difficulty_level = row
        serial_numbers.append(int(serial_number))
        questions.append(question_text)
        difficulties.append(difficulty_level)

file_path = '/Users/abhay/Documents/flask/website/options.csv'
with open(file_path, newline="") as csvfile:
    guess = csv.reader(csvfile)
    for ptr in guess:
        #ans_serial_number, opt1, opt2, opt3, opt4 = ptr
        opt1, opt2, opt3, opt4 = ptr
        #ans_serial_numbers.append(ans_serial_number)
        option1.append(opt1)
        option2.append(opt2)
        option3.append(opt3)
        option4.append(opt4)

file_path = '/Users/abhay/Documents/flask/website/correctanswers.csv'
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        answer = line.strip()  # Remove newline characters and any leading/trailing whitespace
        correctanswer.append(answer)

def get_current_state():
    global select_index
    random_number = randoms()
    current_question = getQuestion()
    current_options = getOption()
    return current_question, current_options

def save_player_data(player_name, correctanswer_count, price_own, status_1, select_index):
    with open('player_data.txt', 'a') as player_data_file:
        player_data_file.write(f"{player_name},{correctanswer_count},{price_own},{status_1},{select_index}\n")

def score(correctanswer_count):
    return correctanswer_count

def price(price_won):
    return price_won

def screen(user_name, questions, options, correctanswer_count, price_won):
    global change_question
    global change_option
    print("|----------------------------------------------------------------------------|")
    print(f"|  name:{user_name}                                                         |")
    print(f"| score : {score(correctanswer_count)}              price own : {price(price_won)}                                |")

    str = ""
    cq, co = which_lifeline_available()
    if cq == 1:
        str += " Change Question "
    if co == 1:
        str += "| Change Option "

    print(f"|    lifeline :{str}                                                                     |")
    print(f"|                                                                           |")
    print(f"| question : {questions[0]}                                                 |")
    print(f"|   a) {options[0]}                                                       |")
    print(f"|   b) {options[1]}                                                       |")
    print(f"|   c) {options[2]}                                                       |")
    print(f"|   d) {options[3]}                                                       |")
    print("|                                                                            |")
    print("|----------------------------------------------------------------------------|")

    while True:
        user_input = input("Your answer: ")

        if user_input in ['a', 'b', 'c', 'd']:
            return user_input

        elif user_input.lower() == 'change' and change_question > 0:
            change_question -= 1
            return 'change'
        else:
            print("Invalid input. Please enter 'a', 'b', 'c', or 'd'.")

def randoms():
    global random_number
    global select_index
    random_number = random.randint(0, len(serial_numbers) - 1)
    while random_number in select_index:
        random_number = random.randint(0, len(serial_numbers) - 1)
    select_index.add(random_number)
    return random_number

def checkAndCreateFile(fName):
    if(os.path.exists(fName)):
        return
    else:
        with open(fName, 'w') as fp:
            return


def get_user_answer():
    def get_user_answer():
        while True:
            user_input = input("Your answer: ")

            if user_input in ['a', 'b', 'c', 'd']:
                return user_input

            elif user_input.lower() == 'change' and change_question > 0:
                change_question -= 1
                return 'change'


def check_answer(user_answer):
    global random_number
    global correctanswer_count
    global price_own

    # 0 = failure
    # 1 = success
    # 2 = change question lifeline
    # 3 = change option lifeline
    returnValue = 0

    print("correct answer : ")
    print("correct answer:",correctanswer)
    print("user answer:",user_answer)
    print("print randomm no:",random_number)
    print("correct answer:",correctanswer[random_number])

    if user_answer == correctanswer[random_number]:
        print("Correct! You win.")
        correctanswer_count += 1
        price_own += 1000
        returnValue = 1


        if correctanswer_count == len(serial_numbers):
            status_1 = "complete"
            # Save the data of the user in the player_data file
            save_player_data(player_name, correctanswer_count, price_own, status_1, str(select_index))
    elif user_answer == 'change_question':
        returnValue = 2
    elif user_answer == 'change_option':
        returnValue = 3
    else:
        returnValue = 0
        status_1 = "incomplete"
        print("Incorrect! You fail.")
        save_player_data(player_name, correctanswer_count, price_own, status_1, str(select_index))
    return returnValue




def getQuestion():
    global random_number
    r = randoms()
    #print("random number generated : " + str(r))
    current_question = (questions[random_number], difficulties[random_number])
    return current_question

def getOption():
    global random_number
    current_options = (option1[random_number], option2[random_number], option3[random_number], option4[random_number])
    return current_options


def which_lifeline_available():
    return change_question, change_option

def price(price_won):
    return price_won

def score(correctanswer_count):
    return correctanswer_count

def game():
    global select_index
    global correctanswer_count
    global price_own
    global player_name

    # ask user - continue previous game --> Y/N
    permission = "yes"

    checkAndCreateFile("player_data.txt")

    file_path1 = 'player_data.txt'
    with open(file_path1, newline="") as csvfile:
        global random_number
        read = csv.reader(csvfile)
        player_name = ""  # Initialize player_name here
        for ptr in read:
            # Check the length of the row before unpacking
            if len(ptr) >= 4:
                username, totalquestion, pricewon, status_1, question_asked_str = ptr[:5]
                player_name = username
                price_own = int(pricewon)
                correctanswer_count = int(totalquestion)
                question_asked_set = set(map(int, question_asked_str.strip('{}').split(',')))
                select_index.update(question_asked_set)
                status = status_1

                # if status == "incomplete":
                #     print("Continue the previous game? (yes/no)")
                #     permission = input()
                #     if permission.lower() == 'yes':
                #         break
                # else:
                #     print("Start the game again? (yes/no)")
                #     permission = input()
                #     if permission.lower() == 'yes':
                #         break


            if permission.lower() == 'yes':
                print("enter the your name ")
                # player_name=input()

                while True:
                    random_number = randoms()
                    current_questions=getQuestion()
                    #current_question = (questions[random_number], difficulties[random_number])
                    current_options=getOption()

                    #current_options = (option1[random_number], option2[random_number], option3[random_number], option4[random_number])
                    #user_answer = screen(player_name, current_questions, current_options, correctanswer_count, price_own)
                    #result = check_answer(user_answer, correctanswer[random_number], random_number)
                    #return current_question, current_options
                    return current_questions, current_options

            select_index_string = str(select_index)

            if result == 'change':
                continue

            while True:
                play_again = input("Do you want to play again? (yes/no)")
                if play_again in ['yes', 'no']:
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

                if play_again == 'yes':
                    game()
                else:
                    print("Goodbye!")
        else:
            print("Goodbye!")
if __name__=="__game__":
# Call the game function
    game()
