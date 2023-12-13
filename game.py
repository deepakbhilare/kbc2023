import csv
import random
import os

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

with open("/Users/abhay/Documents/flask/website/correctanswers.csv") as file:
    answer = file.read()
    for check in answer:
        if check == '\n':
            continue
        rightanswer = check
        correctanswer.append(rightanswer)

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

def randoms(select_index):
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

                if status == "incomplete":
                    print("Continue the previous game? (yes/no)")
                    permission = input()
                    if permission.lower() == 'yes':
                        break
                else:
                    print("Start the game again? (yes/no)")
                    permission = input()
                    if permission.lower() == 'yes':
                        break


    if permission.lower() == 'yes':
        print("enter the your name ")
        player_name=input()

        while True:
            random_number = randoms(select_index)
            current_question = (questions[random_number], difficulties[random_number])
            current_options = (option1[random_number], option2[random_number], option3[random_number], option4[random_number])
            #user_answer = screen(player_name, current_question, current_options, correctanswer_count, price_own)
            return current_question, current_options

            select_index_string = str(select_index)

            if user_answer == correctanswer[random_number]:
                print("Correct! You win.")
                correctanswer_count += 1
                price_own += 1000

                if correctanswer_count == len(serial_numbers):
                    status_1 = "complete"
                    # Save the data of the user in the player_data file
                    save_player_data(player_name, correctanswer_count, price_own, status_1, select_index_string)

            elif user_answer == 'change':
                continue
            else:
                status_1 = "incomplete"
                print("Incorrect! You fail.")
                break

        # save the data of the user in the player_data file
        save_player_data(player_name, correctanswer_count, price_own, status_1, select_index_string)

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

# Call the game function
game()
