from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

data = pd.read_csv("data/french_words.csv")
data_list = data.to_dict(orient="records")
new_word = {}


def correct_selection():
    data_list.remove(new_word)
    df = pd.DataFrame(data_list)
    df.to_csv("data/words_to_learn.csv", index=False)
    generate_word()


def generate_word():
    global new_word, flip_timer
    window.after_cancel(flip_timer)
    try:
        words_to_learn = pd.read_csv("data/words_to_learn.csv")
        words_to_learn_list = words_to_learn.to_dict(orient="records")
    except FileNotFoundError:
        new_word = choice(data_list)
    else:
        new_word = choice(words_to_learn_list)
    finally:
        flashcard.itemconfig(flashcard_img, image=flashcard_front_img)
        flashcard.itemconfig(flashcard_word, text=new_word["French"], fill="black")
        flashcard.itemconfig(flashcard_title, text="French", fill="black")
        flip_timer = window.after(3000, flip_card)


def flip_card():
    flashcard.itemconfig(flashcard_img, image=flashcard_back_img)
    flashcard.itemconfig(flashcard_word, text=new_word["English"], fill="white")
    flashcard.itemconfig(flashcard_title, text="English", fill="white")


window = Tk()
window.title("flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

flashcard_front_img = PhotoImage(file="./images/card_front.png")
flashcard_back_img = PhotoImage(file="./images/card_back.png")

flashcard = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
flashcard_img = flashcard.create_image(400, 263, image=flashcard_front_img)
flashcard.grid(row=0, column=0, columnspan=2)

flashcard_title = flashcard.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
flashcard_word = flashcard.create_text(400, 263, text="trouve", font=("Ariel", 60, "bold"))

# Buttons
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=generate_word)
wrong_btn.grid(row=1, column=0)

right_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=correct_selection)
right_btn.grid(row=1, column=1)

generate_word()


window.mainloop()

