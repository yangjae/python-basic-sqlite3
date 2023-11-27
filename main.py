import pygame_textinput
import pygame, sys, os
import sqlite3
from components.button import Button
from datetime import datetime

score_data = []
current_score = 0
use_database = True

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# Function to save scores to text file when game ends
def save_scores_to_text_file(score):
    if not os.path.exists("db"):
        os.makedirs("db")
    
    with open("db/game_scores.txt", "a") as file:
        for s, n, t in score:
            file.write(f"Score: {s}, Name: {n}, Time: {t}\n")

# Function to display top scores from text file
def get_top_scores_from_txt():
    # top_scores_label.config(text="Top 10 Scores:")
    with open("db/game_scores.txt", "r") as file:
        scores = file.readlines()
        score_data = []
        for i, score in enumerate(scores[:3], 1):
            score_data.append(score)
            
    return score_data

# Function to save scores to sqlite3 database when game ends
def save_scores_to_database(score):
    try:
        if not os.path.exists("db"):
            os.makedirs("db")

        # Connect to the database
        conn = sqlite3.connect('db/game_scores.db')
        c = conn.cursor()
        # Create the table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS game_scores
                     (score integer, name text, time text)''')
        
        # Insert the scores into the table
        c.executemany("INSERT INTO game_scores VALUES (?, ?, ?)", score)
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Function to display top scores from database
def get_top_scores_from_database():
    try:        
        # Connect to the database
        conn = sqlite3.connect('db/game_scores.db')
        c = conn.cursor()
        
        # Get the top 10 scores from the database
        c.execute("SELECT * FROM game_scores ORDER BY score DESC LIMIT 3")
        scores = c.fetchall()
        
        # Append the top scores to the score_data list
        score_data = []
        for score in scores:
            score_data.append(score)
        
        # Close the connection
        conn.close()

        return score_data
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def play():
    global current_score
    
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("SCORE: " + str(current_score), True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="END", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        current_score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    new_high()

        pygame.display.update()
    
def new_high():
    global current_score, use_database
    # But more customization possible: Pass your own font object
    font = get_font(45)
    # Create own manager with custom input validator
    manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 15)
    # Pass these to constructor
    textinput_custom = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)
    # Customize much more
    textinput_custom.cursor_width = 12
    textinput_custom.cursor_blink_interval = 400 # blinking interval in ms
    textinput_custom.antialias = False
    textinput_custom.font_color = (0, 85, 170)

    clock = pygame.time.Clock()

    # Pygame now allows natively to enable key repeat:
    pygame.key.set_repeat(200, 25)

    while True:
        events = pygame.event.get()

        NEWHIGH_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        NEWHIGH_TEXT = get_font(45).render("Enter Your Name(Max=15)", True, "Black")
        NEWHIGH_RECT = NEWHIGH_TEXT.get_rect(center=(640, 130))
        SCREEN.blit(NEWHIGH_TEXT, NEWHIGH_RECT)

        NEWHIGH_BACK = Button(image=None, pos=(640, 460), 
                            text_input="ENTER", font=get_font(75), base_color="Black", hovering_color="Green")

        NEWHIGH_BACK.changeColor(NEWHIGH_MOUSE_POS)
        NEWHIGH_BACK.update(SCREEN)

        # Feed it with events every frame
        textinput_custom.update(events)

        # Get its surface to blit onto the screen
        SCREEN.blit(textinput_custom.surface, (320, 250))

        # Modify attributes on the fly - the surface is only rerendered when .surface is accessed & if values changed
        textinput_custom.font_color = [(c+10)%255 for c in textinput_custom.font_color]

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEWHIGH_BACK.checkForInput(NEWHIGH_MOUSE_POS):
                    name = textinput_custom.value
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Convert current time to string
                    score_data.append((current_score, name, timestamp))
                    if(use_database == True):
                        save_scores_to_database(score_data)   # Save the scores to the database
                    else:
                        save_scores_to_text_file(score_data)  # Save the scores to the text file
                    ranking()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                name = textinput_custom.value
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Convert current time to string
                score_data.append((current_score, name, timestamp))
                if(use_database == True):
                    save_scores_to_database(score_data)   # Save the scores to the database
                else:
                    save_scores_to_text_file(score_data)  # Save the scores to the text file
                ranking()
                print("Oooweee")

        pygame.display.update()

def ranking():
    global score_data, use_database, current_score

    while True:
        SCREEN.fill("white")

        RANKING_MOUSE_POS = pygame.mouse.get_pos()

        RANKING_TEXT = get_font(45).render("RANKING", True, "Black")
        RANKING_RECT = RANKING_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(RANKING_TEXT, RANKING_RECT)

        if(use_database == True): 
            score_data = get_top_scores_from_database()
        else:
            score_data = get_top_scores_from_txt()

        for i, score in enumerate(score_data, 1):
           print(score)
           s, n, *_ = score
           RANKING = "Rank " f"{i}. Score: {s}, Name: {n}"
           RANKING_DATA = get_font(20).render(RANKING, True, "Black")
           RANKING_DATA_RECT = RANKING_DATA.get_rect(topleft=(250, 150+(i*50)))
           SCREEN.blit(RANKING_DATA, RANKING_DATA_RECT) 


        RANKING_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        RANKING_BACK.changeColor(RANKING_MOUSE_POS)
        RANKING_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RANKING_BACK.checkForInput(RANKING_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Button Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        RANKING_BUTTON = Button(image=pygame.image.load("assets/Button Rect.png"), pos=(640, 370), 
                            text_input="RANKING", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        NEWHIGH_BUTTON = Button(image=pygame.image.load("assets/Button Rect.png"), pos=(640, 490), 
                            text_input="NEW HIGH", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Button Rect.png"), pos=(640, 610), 
                            text_input="QUIT", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, RANKING_BUTTON, NEWHIGH_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if RANKING_BUTTON.checkForInput(MENU_MOUSE_POS):
                    ranking()
                if NEWHIGH_BUTTON.checkForInput(MENU_MOUSE_POS):
                    new_high()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()