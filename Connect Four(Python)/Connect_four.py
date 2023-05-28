import numpy as np
import pygame
import sys
import math

pygame.init()                 #Something you have to do when using pygame
pygame.mixer.init()           #Sound

#Screen
Squaresize = 100
Blue = (0, 0, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Yellow = (255, 255, 0)
Green = (0, 255, 0)
Radius = int(Squaresize/2 - 5)  #Since it's raius of the circle, it's dividing by two. Also, we don't want circle to touch each other, so "-5"

ROW_COUNT = 6
COLUMN_COUNT = 7

#Font
myfont = pygame.font.SysFont("monospace", 75)   #font, size

#Tie
Tie = False
Total_space = 42

#Sound
Piece_Drop = "Audio/Piece_Drop.wav"
sound = pygame.mixer.Sound(Piece_Drop)
sound.set_volume(1)

def create_board():
  board = np.zeros((ROW_COUNT,COLUMN_COUNT))      #Make the board 6 Row by 7 Column 
  return board                                    

class drop_piece():
  def __init__(self, Total_space, Tie):
    self.Total_space = Total_space
    self.Tie = Tie
  def main(self, board, row, column_to_drop, piece):
      board[row][column_to_drop] = piece              #After knowing the row that is open, we use the column number that player give us to drop and land on the row
      sound.play()                                    #Play the sound when drop piece
      #piece is 1 or 2 depending on what the number is when passed in
      self.Total_space -= 1
      if(self.Total_space == 0):
        self.Tie = True
        return self.Tie

def is_valid_location(board, column_to_drop):
  return board[ROW_COUNT-1][column_to_drop] == 0     #Check the top row and the column to see if it is 0
  #Row_count is the top part. -1 because it starts from 0
  #column_to_drop is the places that player choose to drop

def get_next_open_row(board, column_to_drop):           #Get called after passed the is_valid_location function test
  for r in range(ROW_COUNT):                          #Check the row from bottom to top
    if board[r][column_to_drop] == 0:               
      return r                                      #After finding the row that is not filled yet, return the row
          
# def print_board(board):
#   print(np.flip(board,0))       #Flip the board when call this function(need to pass in the argument, board)

def winning_move(board, piece):
  #check horizontal locations
  for c in range(COLUMN_COUNT-3):   #Since horizontally, it requires 4 to win, we don't need to check the last three
    for r in range(ROW_COUNT):      #Check every row
      if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:   #Check the first piece and every piece after it
        return True              

  #check vertical locations for win
  for c in range(COLUMN_COUNT):   
    for r in range(ROW_COUNT - 3):
      if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:   #Check the first piece and every piece after it
        return True  

  #check positively sloped diaganols
  for c in range(COLUMN_COUNT -3):   
    for r in range(ROW_COUNT - 3):
      if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:   #Check the first piece and every piece after it
        return True  

  #check negatively sloped diaganols
  for c in range(COLUMN_COUNT - 3):   
    for r in range(3, ROW_COUNT):   #from 3 to ROW_COUNT which is 6 (start from 0)
      if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:   #Check the first piece and every piece after it
        return True  

def draw_board(board):
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT):
      pygame.draw.rect(screen, Blue, ((c)*Squaresize, (r+1)*Squaresize, Squaresize, Squaresize))  #Draw a rectangle
      #Screen, color = Blue, (position on x axis, y axis, height, width)
      #Since axis starts at 0, 0(the top), we want to do (r + 1)(y) because we want to leave the uppder layer black
      pygame.draw.circle(screen, Black, ((c*Squaresize + Squaresize/2), ((r+1)*Squaresize + Squaresize/2)), Radius)
        #The Squaresize/2 is the offset. It is required because a circle start from middle and go towards both side. If not added, half of the circle would be cut off.
        #Screen, color = Black, position, Radius
  for c in range(COLUMN_COUNT):   #Loop through all of the column and row
    for r in range(ROW_COUNT):    
      if board[r][c] == 1:        #For which ever column and row that has 1(placed), turn the circle to red
        pygame.draw.circle(screen, Red, (c*Squaresize + Squaresize/2, height-((r)*Squaresize + Squaresize/2)), Radius)
        #Height - int(...) because pygame screen's top corner is (0, 0), but we want it to start from bottom
        #Remove (r+1) because we don't want to count the first row
      elif board[r][c] == 2:
        pygame.draw.circle(screen, Yellow, (c*Squaresize + Squaresize/2, height-((r)*Squaresize + Squaresize/2)), Radius)

board = create_board()        #Make board = create_board so that you can pass in board in different function
# print_board(board)            #Call print_board to flip the board's x axis 
game_over = False             #The game is not over so keep on running the loop
turn = 0                      #A variable to help determine which player's turn it is

width = COLUMN_COUNT * Squaresize     #This way the board fits perfectly with the width
height = (ROW_COUNT + 1) * Squaresize   #ROW_COUNT + 1 because we want an additional row to drop pieces from

size = (width, height)

screen = pygame.display.set_mode(size)   #The screen
draw_board(board)

drop = drop_piece(Total_space, Tie)

while not game_over:        
  #pygame
  pygame.display.update()              #Keep on updating the changes in pygame screen

  for event in pygame.event.get():
    if event.type == pygame.QUIT:      #When click the "x" button, the window close (If you don't add this, the window will not close)
      sys.exit()

    if event.type == pygame.MOUSEMOTION:    #If the mouse move
      posx = event.pos[0]                   #This is going to constantly update
      if turn == 0: #When player 1 is going
        #Prevent the circle move out of the screen in the first row
        if posx <= Radius:
          pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
          pygame.draw.circle(screen, Red, (Radius, int(Squaresize/2)), Radius)
        elif posx >= (width-Radius):
          pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
          pygame.draw.circle(screen, Red, (width-Radius, int(Squaresize/2)), Radius)
        else:
          pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
          #Since the circle doesn't delete by itself, we want to make a new black rectangle everytime the mouse move so that it seems like the circle is following our mouse
          pygame.draw.circle(screen, Red, (posx, int(Squaresize/2)), Radius)
          #int(Sqauresize/2) because we want to give circle a offset so that it doesn't go out of the screen
      elif turn == 1:
        #Prevent the circle move out of the screen in the first row
        if posx <= Radius:
          pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
          pygame.draw.circle(screen, Yellow, (Radius, int(Squaresize/2)), Radius)
        elif posx >= (width-Radius):
          pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
          pygame.draw.circle(screen, Yellow, (width-Radius, int(Squaresize/2)), Radius)
        else:
          pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
          #Since the circle doesn't delete by itself, we want to make a new black rectangle everytime the mouse move so that it seems like the circle is following our mouse
          pygame.draw.circle(screen, Yellow, (posx, int(Squaresize/2)), Radius)
          #int(Sqauresize/2) because we want to give circle a offset so that it doesn't go out of the screen
      
    if event.type == pygame.MOUSEBUTTONDOWN:
      #print(event.pos)     #Print the position of (x,y) when mouse is down
      #Ask for Player 1 Input
      if turn == 0:
        posx = event.pos[0] #Since the event.pos would output (x, y), [0] means to get x           
        column_to_drop = int(math.floor(posx/Squaresize))    #math.floor round it to the nearest interger, but we add int() just in case
        
        if is_valid_location(board, column_to_drop):        #If it pass the function is_valid_location() test
          row = get_next_open_row(board,column_to_drop)     #The returned open "row" is stored in the row variable
          drop.main(board, row, column_to_drop, 1)         #Then, call the drop_piece function

          if winning_move(board, 1):
            pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))    #Make the first row black again so that the circle is not in the way
            label = myfont.render("Player 1 Wins!", 1, Red) 
            screen.blit(label, (40, 10))        #Display message on the first row
            draw_board(board)                 
            pygame.display.update()             #Need this so that the window can update the new message
            game_over = True                    #Stop running the loop
        
        else: 
          turn = turn - 1

      # Ask for Player 2 Input
      elif turn == 1:
        posx = event.pos[0]   #The first column is 0 - 100, the second column is 100 - 200
        column_to_drop = int(math.floor(posx/Squaresize))  #Sqauresize is 100. 0/100 is 0, so the column to drop in is 0
        #Even if it's 99/100, math.floor would still round down the number to 0

        if is_valid_location(board,column_to_drop):
          row = get_next_open_row(board,column_to_drop)
          drop.main(board, row, column_to_drop, 2)

          if winning_move(board, 2):
            pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
            label = myfont.render("Player 2 Wins!", 1, Yellow)
            screen.blit(label, (40, 10))     #(40, 10) is where the message start displaying
            draw_board(board)
            pygame.display.update()
            game_over = True
      
      #Check if there is still open room
      if drop.Tie == True:
        pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
        label = myfont.render("Tie!", 1, Green)
        screen.blit(label, (280, 10))
        draw_board(board)
        pygame.display.update()
        game_over = True
                                            
      # print_board(board)  #We no longer need to print it using CMD
      draw_board(board)
  
      turn += 1
      turn = turn % 2

      if turn == 0:    #Since pygame.MOUSEMOTION only acativates when the mouse moves, to change color immediately after a player made their choice, we need to add this 
        #Switch color in first row
        pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
        #Since the circle doesn't delete by itself, we want to make a new black rectangle everytime the mouse move so that it seems like the circle is following our mouse
        pygame.draw.circle(screen, Red, (posx, int(Squaresize/2)), Radius)
        #int(Sqauresize/2) because we want to give circle a offset so that it doesn't go out of the screen
      elif turn == 1:
        #Switch color in first row
        pygame.draw.rect(screen, Black, (0, 0, width, Squaresize))
        #Since the circle doesn't delete by itself, we want to make a new black rectangle everytime the mouse move so that it seems like the circle is following our mouse
        pygame.draw.circle(screen, Yellow, (posx, int(Squaresize/2)), Radius)
        #int(Sqauresize/2) because we want to give circle a offset so that it doesn't go out of the screen

if game_over:
  pygame.time.delay(3000)