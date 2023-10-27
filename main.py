import pygame
import sys
import re
import random
import os
import math
import pygmtlsv4 as tools

pygame.init()

WIDTH, HEIGHT = 600, 700
PROMPT_BOX_WIDTH = 200
PROMPT_BOX_HEIGHT = 60
INPUT_BOX_WIDTH = 400
INPUT_BOX_HEIGHT = 60

INITIAL_TIME = 10

MAX_LIVES = 5

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word bomb")

image_location = lambda string: os.path.join("images", string)
sound_location = lambda string: os.path.join("sounds", string)

# all of the images that are used in the game
HEART = pygame.transform.scale(pygame.image.load(image_location("heart.png")), (70, 70))
BOMB1 = pygame.transform.scale(pygame.image.load(image_location("bomb1.png")), (150, 150))
BOMB2 = pygame.transform.scale(pygame.image.load(image_location("bomb2.png")), (150, 150))

# all of the sounds that are used in the game
EXPLOSION = pygame.mixer.Sound(sound_location("explosion.mp3"))
TICK = pygame.mixer.Sound(sound_location("tick tock.mp3"))
TICK.set_volume(0.1)
LOCKED = pygame.mixer.Sound(sound_location("locked.mp3"))
BEEP = pygame.mixer.Sound(sound_location("beep.mp3"))
BEEP.set_volume(0.3)
ERROR = pygame.mixer.Sound(sound_location("error.mp3"))
ERROR.set_volume(0.2)

# general colours
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
RED =    (211,   0,   0)
GREEN =  (  0, 150,   0)
DGREEN = (  0, 100,   0)
BLUE =   (  0,   0, 211)
LBLUE =  (137, 207, 240)
GREY =   (201, 201, 201)
LGREY =  (231, 231, 231)
DGREY =  ( 50,  50,  50)
LBROWN = (185, 122,  87)
DBROWN = (159, 100,  64)

# useful constants
DURATION = 200 #ms
PADDING = 20
FPS = 60

# fonts
FONT = pygame.font.SysFont("consolas.ttf", 50)
INPUTFONT = pygame.font.SysFont("consolas.ttf", 30)

# USEREVENTS that are called in the program
START = pygame.USEREVENT + 1
GENERATE_PROMPT = pygame.USEREVENT + 2
RESET_INPUT = pygame.USEREVENT + 3
LOSE_LIFE = pygame.USEREVENT + 4
RESTART = pygame.USEREVENT + 5
PLAY_EXPLOSION = pygame.USEREVENT + 6
GO_TO_MENU = pygame.USEREVENT + 7


class dictionary:
  """This class holds all of the words in the chosen dictionary"""
  def __init__(self):
    with open("all words - sowpods + enable 1.txt") as p:
      self.words = p.read().split("\n")
  def get_words(self) -> list:
    """Returns a list of all words"""
    return self.words
  
  def search_word(self, text:str) -> bool:
    """Returns a bool value depending on if argument text is in the dictionary"""
    text = text.lower()
    for word in self.words:
      if text == word:
        return True
    return False

class prompt:
  """This class holds all possible prompts"""
  def __init__(self):
    with open("prompts.txt") as p:
      self.prompts = p.read()
      
      # removes any bracketed information
      self.prompts = re.sub("[\(\[].*?[\)\]]", "", self.prompts) # i have no idea what this function is doing :/
      self.prompts = self.prompts.split("\n")
      
      #removes whitespace
      for prompt in range(len(self.prompts)):
        self.prompts[prompt] = self.prompts[prompt].strip()
      
  def get_prompts(self) -> list:
    """returns all possible prompts"""
    return self.prompts
  
  def generate_prompt(self) -> str:
    """Returns a random item from the list"""
    return self.prompts[random.randrange(0, len(self.prompts))]


def drawWin(state:str, buttons:tools.Button, user_prompt:str, user_input:str, time_left:int, lives:int, bombs:tools.Animation, explosion:tools.Animation, words_used:list, time_used:int):
  """Any changes to the window ("drawing") is done in this function"""
  
  pygame.draw.rect(WIN, DGREY, pygame.Rect(0, 0, WIDTH, HEIGHT)) # blank canvas
  
  if state == "game":
    # displays user prompt
    text = FONT.render(user_prompt, 1, WHITE)
    rect = pygame.Rect(WIDTH/2 - PROMPT_BOX_WIDTH/2, HEIGHT/2 - PROMPT_BOX_HEIGHT/2, PROMPT_BOX_WIDTH, PROMPT_BOX_HEIGHT)
    pygame.draw.rect(WIN, GREEN, rect, border_radius = PROMPT_BOX_HEIGHT//2)
    WIN.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))
    
    #displays user input
    text = INPUTFONT.render(user_input, 1, WHITE)
    rect = pygame.Rect(WIDTH/2 - INPUT_BOX_WIDTH/2, HEIGHT - PADDING - INPUT_BOX_HEIGHT, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)
    pygame.draw.rect(WIN, BLACK, rect, border_radius = INPUT_BOX_HEIGHT//2)
    WIN.blit(text, ((WIDTH - text.get_width())/2, HEIGHT - PADDING - INPUT_BOX_HEIGHT/2 - text.get_height()/2))
    
    # displays time left
    text = str((time_left//1000) + 1)
    text = FONT.render(text, 1, WHITE)
    WIN.blit(text, (PADDING, PADDING))
    
    # displays how many lives the user has left
    for heart in range(lives+1):
      WIN.blit(HEART, (WIDTH-heart*(HEART.get_width()+PADDING/2), PADDING/2))
      
    # draws the animations of the bomb and explosion
    bombs.play(WIN, True, False)
    explosion.play(WIN, True, auto_stop = True)
    
  if state == "end":
    
    # displays all statistics gathered over the course of the game
    text = INPUTFONT.render(f"Number of words used: {len(words_used)}", 1, WHITE)
    WIN.blit(text, (PADDING, PADDING))
    text = INPUTFONT.render(f"Time used: {time_used//1000} seconds", 1, WHITE)
    WIN.blit(text, (PADDING, PADDING*2+text.get_height()))
    average = math.ceil((time_used//1000)/len(words_used)*100)/100
    text = INPUTFONT.render(f"Average time per word: {average} seconds", 1, WHITE)
    WIN.blit(text, (PADDING, PADDING*3+text.get_height()*2))
    text = INPUTFONT.render(f"Average word length: {int(sum( map(len, words_used) ) / len(words_used))} characters", 1, WHITE)
    WIN.blit(text, (PADDING, PADDING*4+text.get_height()*3))
    
  # draws any of the displayed buttons
  buttons.draw(WIN)
  pygame.display.flip()


def main():

  buttons = tools.Button()

  width = WIDTH/3
  height = PADDING*3  
  start_rect = pygame.Rect(WIDTH/2-width/2, HEIGHT/2, width, height)
  menu_rect = pygame.Rect(WIDTH/2-width/2-1, HEIGHT/2, width, height)
  
  buttons.create(start_rect, BLACK, START, text="START", font=FONT, textColour=WHITE)
  buttons.create(menu_rect, BLACK, GO_TO_MENU, text="MENU", font=FONT, textColour=WHITE, visible=False)
  
  prompts = prompt()
  dict = dictionary()
  
  # creates animation class for the bomb which alternates between a) 2 images b) slowly
  bombs = tools.Animation(WIDTH/2 - 75 - PADDING*0.8, 100, "image")
  
  # a
  bombs.add_frame(BOMB1)
  bombs.add_frame(BOMB2)
  
  # b
  bombs.duplicate_all_frames(10)
  
  # creates animation class for the explosion which is a sequence of a) 9 images b) quickly
  explosion = tools.Animation(WIDTH/2 - 150, 75, frame_type="image")
  
  # a
  explosion.set_frames(
    [pygame.transform.scale( # ensures all correct size
      pygame.image.load(os.path.join("explosion", str(x) + ".png")), # loads images
      (300, 300)) for x in range(4, 13)]) # for all frames
  explosion.set_offsets([[0, 0] for _ in range(4, 13)])
  
  # b
  explosion.duplicate_all_frames(4)
  
  state = "menu"
  user_prompt = ""
  user_input = ""
  time_left = INITIAL_TIME*1000
  last_decrement_time = 0
  lives = MAX_LIVES
  words_used = []

  #initiates the clock
  clock = pygame.time.Clock()
  
  time_used = 0

  #initiates game loop
  run = True
  while run:
    
    #ticks the clock
    clock.tick(FPS)
    
    if time_left <= 0:
      pygame.event.post(pygame.event.Event(LOSE_LIFE))
    
    if state == "game":
      time_left -= pygame.time.get_ticks() - last_decrement_time
      last_decrement_time = pygame.time.get_ticks()
      

    #gets mouse position
    mouse = pygame.mouse.get_pos()
    
    #for everything that the user has inputted ...
    for event in pygame.event.get():

      #if the "x" button is pressed ...
      if event.type == pygame.QUIT:

        #ends game loop
        run = False

        #terminates pygame
        pygame.quit()

        #terminates system
        sys.exit()
        
      elif event.type == pygame.MOUSEBUTTONUP:
        buttons.check(mouse)  # checks if any of the buttons were clicked
        
      elif event.type == pygame.KEYDOWN:
        if state == "game":
          # checks if a character key is pressed
          if 97 <= event.key <= 122:
            inputted = event.key - 32
            user_input += chr(inputted)
            
          if event.key == pygame.K_BACKSPACE:
            if user_input != "":
              user_input = user_input[0:-1]
              
          if event.key == pygame.K_RETURN:
            # checks if user got a valid word
            if dict.search_word(user_input) and (user_prompt in user_input) and (user_input not in words_used):
              pygame.event.post(pygame.event.Event(GENERATE_PROMPT))
              pygame.event.post(pygame.event.Event(RESET_INPUT))
              time_left = INITIAL_TIME*1000
              words_used.append(user_input)
              BEEP.play()
            
            # checks if the word has already been used
            elif user_input in words_used:
              LOCKED.play()
              pygame.event.post(pygame.event.Event(RESET_INPUT))
            
            # else, the word was not in the dictionary and therefore not a valid word
            else:
              ERROR.play()
              pygame.event.post(pygame.event.Event(RESET_INPUT))

      elif event.type == START:
        # resets the stats and prompts
        user_prompt = ""
        user_input = ""
        
        lives = MAX_LIVES
        words_used = []
        start_time = pygame.time.get_ticks()
        buttons.toggleVis(start_rect)
        state = "game"
        pygame.event.post(pygame.event.Event(GENERATE_PROMPT))
        last_decrement_time = pygame.time.get_ticks()
        
        bombs.start()
        TICK.play(-1)
        
      elif event.type == GENERATE_PROMPT:
        user_prompt = prompts.generate_prompt()
        
      elif event.type == RESET_INPUT:
        user_input = ""
        
      elif event.type == LOSE_LIFE:
        EXPLOSION.play()
        lives -= 1
        if lives <= 0:
          state = "end"
          time_left = INITIAL_TIME*1000
          last_decrement_time = 0
          time_used = pygame.time.get_ticks() - start_time
          
          buttons.toggleVis(menu_rect)
          
          # ends animations
          bombs.stop()
          explosion.set_current_frame(0)
          explosion.stop()
          TICK.stop() # TICK is set to repeat continually so has to be told to stop playing
        else:
          pygame.event.post(pygame.event.Event(PLAY_EXPLOSION))
          pygame.event.post(pygame.event.Event(GENERATE_PROMPT))
          pygame.event.post(pygame.event.Event(RESET_INPUT))
          time_left = INITIAL_TIME*1000
      
      elif event.type == PLAY_EXPLOSION:
        explosion.start()
        
      elif event.type == GO_TO_MENU:
        state = "menu"
        buttons.toggleVis(menu_rect)
        buttons.toggleVis(start_rect)

    drawWin(state, buttons, user_prompt, user_input, time_left, lives, bombs, explosion, words_used, time_used)

main()