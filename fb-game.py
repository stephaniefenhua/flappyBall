from tkinter import *
import time
from random import *

tk = Tk()
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=1000, height=600)
canvas.pack()
#my_image = PhotoImage(file='/Users/stephaniesu/Downloads/BrooklynBridgeFlappyBall.gif')
#canvas.create_image(500, 300, image=my_image)
tk.update()

title_text = canvas.create_text(500, 100, text="Flappy Ball:", font=("Papyrus", 30), fill="white")
subtitle_text = canvas.create_text(500, 155, text="Nightlife", font=("Papyrus", 40), fill="white")

colors = ["blue","purple", "cyan", "turquoise", "lavender", "white", "orange", "gold", "grey", "black"]

class Ball:
   def __init__(self, canvas, obstacle_list, color):
       self.id = canvas.create_oval(25, 290, 45, 310, fill=color, outline="white")
       self.canvas = canvas
       self.obstacle_list = obstacle_list
       self.xSpeed = 0
       self.ySpeed = 0
       canvas.bind_all("<KeyPress-Up>", self.move_up)
       canvas.bind_all("<KeyPress-Return>", self.start_game)
       self.game_start = False
       self.canvas_width = canvas.winfo_width()
       self.canvas_height = canvas.winfo_height()
       self.score = 0
       self.score_box = canvas.create_rectangle(850, 230, 900, 275, fill=colors[randint(0, 8)])
       self.display_score = canvas.create_text(875, 250, text="%s" % self.score, font=("Arial", 30), fill="black")
       self.game_over = False
       self.play_button = self.canvas.create_rectangle(435, 240, 565, 290, fill="lavender")
       self.play = self.canvas.create_text(500, 265, text="Play", font=('Arial', 25))
       self.canvas.tag_bind(self.play_button, "<Button-1>", self.prep_game)
       self.canvas.tag_bind(self.play, "<Button-1>", self.prep_game)
       self.instructions_button = self.canvas.create_rectangle(435, 310, 565, 360, fill="lavender")
       self.instructions = self.canvas.create_text(500, 335, text="Instructions", font=('Arial', 25))
       self.instructions_shown = False
       self.canvas.tag_bind(self.instructions_button, "<Button-1>", self.show_instructions)
       self.canvas.tag_bind(self.instructions, "<Button-1>", self.show_instructions)
       self.clicked_play = False

   def show_instructions(self, event):
       if self.instructions_shown == False:
           self.instructions_box = canvas.create_rectangle(270, 365, 730, 460, fill="white")
           self.instructions_text = canvas.create_text(500, 410, text="Welcome to Flappy Ball: Nightlife! The objective of this game is to \n\
move the ball for as long as you can through the obstacles.\nThe only control is the 'Up' key, which will keep the \
ball from falling.\nIf the ball drops to the bottom or it collides with an obstacle, the\ngame is over. Good luck and have fun!",font=("Arial", 15))
           self.instructions_shown = True
       else:
           canvas.delete(self.instructions_text)
           canvas.delete(self.instructions_box)
           self.instructions_shown = False


   def prep_game(self, event):
       self.clicked_play = True
       canvas.delete(self.play_button)
       canvas.delete(self.play)
       canvas.delete(self.instructions)
       canvas.delete(self.instructions_button)
       canvas.delete(title_text)
       canvas.delete(subtitle_text)
       self.button = canvas.create_rectangle(50, 180, 150, 225, fill=colors[randint(0, 8)])
       self.start_text = canvas.create_text(100, 200, text="Press 'Return'", font=("Helvetica", 16), fill="black")

   def start_game(self, event):
       if self.clicked_play == False:
           return
       self.ySpeed = 3
       self.game_start = True
       canvas.delete(self.start_text)
       canvas.delete(self.button)
       if self.instructions_shown == True:
           canvas.delete(
           self.instructions_text)
           canvas.delete(self.instructions_box)

   def move(self):
       pos = self.canvas.coords(self.id)
       for obstacle in obstacle_list:
           if pos[3] >= self.canvas_height or obstacle.id_top in self.canvas.find_overlapping(pos[0], pos[1], pos[2], pos[3]) \
           or obstacle.id_bottom in self.canvas.find_overlapping(pos[0], pos[1], pos[2], pos[3]):
               if self.game_over == False:
                   self.game_over = True
                   canvas.delete(self.display_score)
                   canvas.delete(self.score_box)
                   canvas.create_rectangle(370, 370, 630, 430, fill=colors[randint(0,5)], outline="white")
                   canvas.create_text(490, 400, text="Your Score: %s" % self.score,font=("Arial", 25))
                   if 30 <= self.score < 40:
                       canvas.create_oval(585, 385, 615, 415, fill="orange")
                   elif 40 <= self.score < 50:
                       canvas.create_oval(585, 385, 615, 415, fill="grey")
                   elif self.score >= 50:
                       canvas.create_oval(585, 385, 615, 415, fill="gold")
                   else:
                       canvas.create_oval(585, 385, 615, 415)
                   canvas.create_rectangle(410, 250, 590, 350, fill=colors[randint(0,8)], outline=("white"))
                   end_text = canvas.create_text(500, 300, text="Game Over!", font=("Helvetica", 30))
                   tk.update()
                   time.sleep(3)
                   exit()

       if pos[1] <= 0:
           self.canvas.move(self.id, 0, 7.5)
           self.ySpeed = 0
       else:
           self.canvas.move(self.id, self.xSpeed, self.ySpeed)
           if self.game_start == True:
               self.ySpeed += 0.1

   def move_up(self, event):
       if self.game_start == True:
           self.ySpeed -= 1.5

class Obstacle:
   def __init__(self, canvas, color):
       y2_top = randint(100, 400)
       y1_bottom = y2_top + 125
       self.id_top = canvas.create_rectangle(400, 0, 460, y2_top, fill=color, outline="white")
       self.id_bottom = canvas.create_rectangle(400, y1_bottom, 460, 600, fill=color, outline="white")
       self.canvas = canvas
       self.canvas.move(self.id_top, 300, 0)
       self.canvas.move(self.id_bottom, 300, 0)
       self.score = 0
       self.passed = False

   def move_obstacle(self):
       if myBall.game_start == True:
           canvas.move(self.id_top, -7, 0)
           canvas.move(self.id_bottom, -7, 0)
       self.increase_score()

   def increase_score(self):
       if self.passed == True:
           return
       pos_obstacle = self.canvas.coords(self.id_top)
       pos_ball = self.canvas.coords(myBall.id)
       if pos_ball[2] > pos_obstacle[2]:
           self.passed = True
           myBall.score += 1
           canvas.itemconfig(myBall.display_score, text="%s" % myBall.score)

obstacle_list = []
myBall = Ball(canvas, obstacle_list, colors[randint(0, 9)])
tickCounter = 0
obstacle1 = Obstacle(canvas, colors[randint(0, 9)])
obstacle_list.append(obstacle1)



while True:
   myBall.move()
   if myBall.game_start:
       tickCounter += 1
   if tickCounter % 75 == 0 and myBall.game_start:
       obstacle = Obstacle(canvas, colors[randint(0, 9)])
       obstacle_list.append(obstacle)
   for obstacle in obstacle_list:
       obstacle.move_obstacle()
   tk.update_idletasks()

   tk.update()
   time.sleep(0.01)




