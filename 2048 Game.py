from tkinter import messagebox
import tkinter as tk
from tkinter import *
from pygame import mixer
import random
import os
import pygame

# Design numbers & words
GRID_COLOR = "#c2b3a9"
EMPTY_CELL_COLOR = "#a89283"
SCORE_LABEL_FONT = ("ROSEMARY", 22, "bold")
TITLE_FONT = ("ROSEMARY", 29)
DESCRIPTION_FONT = ("Century", 14)
SCORE_FONT = ("ROSEMARY", 22)
CELL_NUMBER_COLORS = {2: "#ffffff", 4: "#ffffff", 8: "#ffffff"}
CELL_NUMBER_FONTS = ("ROSEMARY", 22)
CELL_COLORS = {2: "#b2cd44",
               4: "#78ba3f",
               8: "#3ab073",
               16: "#2da8e1",
               32: "#3566b0",
               64: "#514597",
               128: "#7d4294",
               256: "#c3308b",
               512: "#dc2e4e",
               1024: "#e04932",
               2048: "#e86325",
               4096: "#ffd900"}


class Game_2048(tk.Frame):
    def __init__(user):
        # Set main window
        tk.Frame.__init__(user)
        user.grid()
        user.master.title("2048 Game :)")
        user.main_grid = tk.Frame(user, bg=GRID_COLOR, bd=3, width=100, height=100)
        user.main_grid.grid(padx=(14, 0), pady=(175, 0))

        # 2048Game functions and parameters
        # Top value to play the game
        user.top_value = 2048

        # Grid size
        user.grid_size = 4

        # Main window position
        user.sw = user.master.winfo_screenwidth()
        user.sh = user.master.winfo_screenheight()

        # Game initialization
        user.make_GUI()
        user.start_game()

        # Buttons
        user.guide_button()
        user.about_us_button()
        user.play_music_button()
        user.mute_music_button()

        # Defining button to start new game
        user.master.bind('<r>', user.restart_massage)

        # Defining button to close game
        user.master.bind('<q>', user.quit_massage)

        # Defining buttons to play 
        user.master.bind('<a>', user.left)
        user.master.bind('<s>', user.down)
        user.master.bind('<d>', user.right)
        user.master.bind('<w>', user.up)

        user.mainloop()


    # Functions to set game desing
    def make_GUI(user):        
        user.cells = []
        # Creating the grid 
        for i in range(user.grid_size):
            row = []
            for j in range(user.grid_size):
                cell_frame = tk.Frame(user.main_grid, bg=EMPTY_CELL_COLOR, width=80, height=80)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(user.main_grid, bg=EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {'frame': cell_frame, "number": cell_number}
                row.append(cell_data)
            user.cells.append(row)
            
        # Game position in screen
        w = user.grid_size*99
        h = (user.grid_size+2)*93
        x = (user.sw - w)/2
        y = (user.sh - h)/2
        user.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        user.master.resizable(False,False)
        user.configure(bg='#f0eddf')

        # Game title
        act_frame = tk.Frame(user)
        act_frame.place(relx=0.16, rely=0.1, anchor="center",)
        tk.Label(
            act_frame,
            text="2048",
            font=TITLE_FONT,
            bg='#ecc400',
            fg='white',
            width=4,
            height=2,
        ).grid(row=0)

        # Description
        description_frame = tk.Frame(user)
        description_frame.place(relx=0.52, rely=0.285, anchor="center")
        tk.Label(
            description_frame,
            text = "join the numbers & get to the 2048 tile!!",
            font = DESCRIPTION_FONT,
            fg='#787167',
            bg='#f0eddf',
        ).grid(row=0)
  

        # Game current score and best score
        user.score = 0
        user.bstScore = 0
        # Save best score
        if os.path.exists("bestscore.ini"):
            with open("bestscore.ini", "r") as f:
                user.bstScore = int(f.read())

        # Score
        score_frame = tk.Frame(user)
        score_frame.place(relx=0.5, y=46, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=SCORE_LABEL_FONT,
        ).grid(row=0) 
        user.score_label = tk.Label(score_frame, text=user.score, font=SCORE_FONT)
        user.score_label.grid(row=1)

        # Record
        record_frame = tk.Frame(user)
        record_frame.place(relx=0.84, y=46, anchor="center")
        tk.Label(
            record_frame,
            text="Record",
            font=SCORE_LABEL_FONT,
        ).grid(row=0)
        user.record_label = tk.Label(record_frame, text=user.bstScore, font=SCORE_FONT)
        user.record_label.grid(row=2)
    
    # Function for restart game
    def new_game(user):
        user.make_GUI()
        user.start_game()

    # Create new game
    def start_game(user):
        # Place the first random number in a random position
        user.matrix = [[0]*user.grid_size for _ in range(user.grid_size)]
        row = random.randint(0, user.grid_size-1)
        col = random.randint(0, user.grid_size-1)
        user.matrix[row][col] = 2
        user.cells[row][col]["frame"].configure(bg=CELL_COLORS[2])
        user.cells[row][col]["number"].configure(
            bg=CELL_COLORS[2],
            fg=CELL_NUMBER_COLORS[2],
            font=CELL_NUMBER_FONTS,
            text="2"
        )

        # Place the second random number in an empty random position
        while(user.matrix[row][col] != 0):
            row = random.randint(0, user.grid_size-1)
            col = random.randint(0, user.grid_size-1)
        user.matrix[row][col] = 2
        user.cells[row][col]["frame"].configure(bg=CELL_COLORS[2])
        user.cells[row][col]["number"].configure(
            bg=CELL_COLORS[2],
            fg=CELL_NUMBER_COLORS[2],
            font=CELL_NUMBER_FONTS,
            text="2"
        )
        user.score = 0

        # Play music in background of game                                  
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('musics/Approaching Dusk.mp3'), loops= -1)
        

    # Show message for how to play
    def guide_message(user):
        messagebox.showinfo("Game Guide","Hi, thanks for choose this game:)\n\
     -Press'A','S','D','W' on keybord to move left,down,right &          up.\n\
     -Press'Q' on keybord to exit the game and'R'to start new           game. "
     )
        
    # Button for help player how can play whith this game 
    def guide_button(user): 
        g_button = Button(user,
                          text="How to play",
                          bg="#a09999", 
                          fg="white", 
                          font=("Century", 8, 'bold'),
                          command=user.guide_message,
                          width=10
                          )
        g_button.place(relx=0.84, rely=0.21, anchor="center")    


    # show message for introduction creator
    def about_us(user):
        messagebox.showinfo('About Me', 'Hello, Im Fatemeh Rahmani a third semester student of computer engineering at the Faculty of Technology and Engineering - East of Guilan.\n\n\
    This is a game for Data Structures project.')

    # Button for introduction 
    def about_us_button(user): 
        about_button = Button(user,
                          text="About us",
                          bg="#cca993", 
                          fg="white", 
                          font=("Century", 8, 'bold'),
                          command=user.about_us,
                          width=10)
        about_button.place(relx=0.50, rely=0.21, anchor="center")


    # Play music in background of game    
    def play_music(user):                               
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('musics/Approaching Dusk.mp3'), loops= -1)

    # Mute background sound
    def mute_music(user):
        pygame.mixer.Channel(0).stop()   

    # Button for play music in background of game 
    def play_music_button(user):
        global play_photo
        play_photo = PhotoImage(file="images/play.png")
        playBtn = Button(user, image=play_photo, command=user.play_music, bg='#f0eddf', bd=0)
        playBtn.image = play_photo
        playBtn.place(relx=0.11, rely=0.23, anchor="center")

    # Button for mute music in background of game       
    def mute_music_button(user):
        global mute_photo
        mute_photo = PhotoImage(file="images/mute.png")
        muteBtn = Button(user, image=mute_photo, command=user.mute_music, bg='#f0eddf', bd=0)
        muteBtn.image = mute_photo
        muteBtn.place(relx=0.21, rely=0.23, anchor="center")  


    # For ask player wants quite game or continue
    def quit_massage(user, event):
        q_win=Tk()
        frame1 = Frame(q_win, highlightbackground="green", highlightcolor="green",highlightthickness=1, bd=0)
        frame1.pack()
        q_win.overrideredirect(1)
        q_win.geometry("200x70+650+400")
        label = Label(frame1, text="Are you sure you want to quit game?")
        label.pack()
        yes_button = Button(frame1, text="Yes", bg="light blue", fg="dark blue",command=quit, width=10)
        yes_button.pack(padx=10, pady=10 , side=LEFT)
        no_button = Button(frame1, text="No", bg="light blue", fg="dark blue",command=q_win.destroy, width=10)
        no_button.pack(padx=10, pady=10, side=LEFT)
        q_win.mainloop()

    
    # For ask player wants restart game or no
    def restart_massage(user, event): 
        r_win=Tk()
        frame1 = Frame(r_win, highlightbackground="green", highlightcolor="green",highlightthickness=1, bd=0)
        frame1.pack()
        r_win.overrideredirect(1)
        r_win.geometry("240x70+650+400")
        label = Label(frame1, text="Are you sure you want to start a new game?")
        label.pack()                                                          
        yes_button = Button(frame1, text="Yes", bg="light blue", fg="dark blue", command=user.new_game, width=10)
        yes_button.pack(padx=13, pady=10 , side=LEFT)
        no_button = Button(frame1, text="No", bg="light blue", fg="dark blue", command=r_win.destroy, width=10)
        no_button.pack(padx=25, pady=10, side=LEFT)
        r_win.mainloop()      
       
    
    # Stack of number 
    def stack(user):
        new_matrix = [[0] * user.grid_size for _ in range(user.grid_size)]
        for row in range(user.grid_size):
            fill_position = 0
            for col in range(user.grid_size):
                if user.matrix[row][col] != 0:
                    new_matrix[row][fill_position] = user.matrix[row][col]
                    fill_position += 1
        user.matrix = new_matrix


    # Combine equal numbers
    def combine(user):
        for row in range(user.grid_size):
            for col in range(user.grid_size-1):
                if (user.matrix[row][col] != 0) and (user.matrix[row][col] == user.matrix[row][col + 1]):
                    user.matrix[row][col] *= 2
                    user.matrix[row][col + 1] = 0
                    user.score += user.matrix[row][col]
                    if user.score > user.bstScore:
                        user.bstScore = user.score
                        with open("bestscore.ini", "w") as f:
                            f.write(str(user.bstScore))

                    # Sound effect for combine tiles                                       
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('musics/combine.mp3'))

    # Reverse function    
    def reverse(user):
        new_matrix = []
        for row in range(user.grid_size):
            new_matrix.append([])
            for col in range(user.grid_size):
                new_matrix[row].append(user.matrix[row][(user.grid_size-1) - col])
        user.matrix = new_matrix


    # Transpose function
    def transpose(user):
        new_matrix = [[0]*user.grid_size for _ in range(user.grid_size)]
        for row in range(user.grid_size):
            for col in range(user.grid_size):
                new_matrix[row][col] = user.matrix[col][row]
        user.matrix = new_matrix


    # Add new number in a random position
    def add_new_tile(user):
        if any(0 in row for row in user.matrix):
            row = random.randint(0, user.grid_size-1)
            col = random.randint(0, user.grid_size-1)
            while(user.matrix[row][col] != 0):
                row = random.randint(0, user.grid_size-1)
                col = random.randint(0, user.grid_size-1)
            # Display numbers 2 and 4 with probabilities of 0.8 and 0.2    
            user.matrix[row][col] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 4, 4])


    # Functions to update de GUI
    def update_GUI(user):
        cell_text_color = 0
        cell_cell_color = 0
        for row in range(user.grid_size):
            for col in range(user.grid_size):
                cell_value = user.matrix[row][col]
                if cell_value == 0:
                    user.cells[row][col]["frame"].configure(bg=EMPTY_CELL_COLOR)
                    user.cells[row][col]["number"].configure(bg=EMPTY_CELL_COLOR, text="")
                else:
                    if cell_value >= 8:
                        cell_text_color = 8
                    else:
                        cell_text_color = cell_value
                    if cell_value >= 4096:
                        cell_cell_color = 4096
                    else:
                        cell_cell_color = cell_value
                    
                    user.cells[row][col]["frame"].configure(bg=CELL_COLORS[cell_cell_color])
                    user.cells[row][col]["number"].configure(
                        bg=CELL_COLORS[cell_cell_color], 
                        fg=CELL_NUMBER_COLORS[cell_text_color],
                        font=CELL_NUMBER_FONTS,
                        text=str(cell_value))
        user.score_label.configure(text=user.score)
        user.record_label.configure(text=user.bstScore)
        user.update_idletasks()


    # Check for possibles moves
    def any_move(user):
        for i in range(user.grid_size):
            for j in range(user.grid_size-1):
                if user.matrix[i][j] == user.matrix[i][j + 1] or \
                   user.matrix[j][i] == user.matrix[j + 1][i]:
                    return True
        return False


    # Check for game over
    def game_over(user):
        # Check if to value is reached
        if any(user.top_value in row for row in user.matrix):
            text = f"You did {user.top_value}!!"
            user.popup(text, text + "Cotinue?")
            user.top_value = user.top_value*2
        # Check if there are no more moves in the grid say game over
        elif not any(0 in row for row in user.matrix) and not user.any_move():
            user.popup("Game Over:(", "\t\tGame Over!!\t\t\nbut you can try it again later :)")
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('musics/game_over.mp3'))
            print("Record:", str(user.bstScore))
            print("Score:", str(user.score))


    # Create popup for game over and win  
    def popup(user, win_title, win_message):
        popup_win = tk.Toplevel()
        popup_win.wm_title(win_title)
        w = 280
        h = 90
        x = (user.sw - w)/2
        y = (user.sh - h)/2
        popup_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
        l = tk.Label(popup_win, text=win_message)
        l.pack(padx=11, pady=3)
        ok_btn = tk.Button(popup_win, text="Ok", bg="light blue", fg="dark blue", command=popup_win.destroy, width=10)
        no_btn = tk.Button(popup_win, text="NO", bg="light blue", fg="dark blue", command=popup_win.quit, width=10)
        popup_win.master.resizable(False,False)
        ok_btn.pack(padx=26, pady=5, side=LEFT)
        no_btn.pack(padx=30, pady=5, side=LEFT)


    mixer.init()
    # Stacking for move left
    def left(user, event):
        user.stack()
        user.combine()
        user.stack()
        user.add_new_tile()
        user.update_GUI()
        user.game_over()
        # Sound effect for move tiles
        mixer.music.load('musics/left_right.mpeg')
        mixer.music.play(-1)
        user.after(500, mixer.music.stop)

    # Stacking for move right
    def right(user, event):
        user.reverse()
        user.stack()
        user.combine()
        user.stack()
        user.reverse()
        user.add_new_tile()
        user.update_GUI()
        user.game_over()
        # Sound effect for move tiles
        mixer.music.load('musics/left_right.mpeg')
        mixer.music.play(-1)
        user.after(500, mixer.music.stop)

    # Stacking for move up
    def up(user, event):
        user.transpose()
        user.stack()
        user.combine()
        user.stack()
        user.transpose()
        user.add_new_tile()
        user.update_GUI()
        user.game_over()
        # Sound effect for move tiles
        mixer.music.load('musics/up_down.mpeg')
        mixer.music.play(-1)
        user.after(500, mixer.music.stop)
     
    # Stacking for move down
    def down(user, event):
        user.transpose()
        user.reverse()
        user.stack()
        user.combine()
        user.stack()
        user.reverse()
        user.transpose()
        user.add_new_tile()
        user.update_GUI()
        user.game_over()
        # Sound effect for move tiles
        mixer.music.load('musics/up_down.mpeg')
        mixer.music.play(-1)
        user.after(500, mixer.music.stop)          


if __name__ == "__main__":
    Game_2048()                                                                            