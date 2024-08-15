from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
IMAGE_WIDTH = 200
IMAGE_HEIGHT = 224
IMAGE_PATH = "tomato.png"
PADDING_X = 100
PADDING_Y = 50
OFFSET = 18
CLOCK_START = "00:00"
CLOCK_COLOR = "white"
CHECK_MARK = "✔"
SECONDS_IN_MIN = 60
MS_IN_S = 1000
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """
    Function to reset the timer back to its initial state once the 'Reset' button is clicked.
    :return: None
    """
    global reps, timer

    window.after_cancel(timer)
    reps = 0
    title_label.config(text="Timer", fg=GREEN, bg=YELLOW)
    canvas.itemconfig(timer_text, text=CLOCK_START)
    check_mark_label.config(text="")

    # Enable the start button once the application is reset
    start_button.config(state=NORMAL)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """
    Function to start the timer once a work or break repetition is complete.
    This function is also called if the 'Start' button is clicked.
    :return: None
    """
    # Disable the start button to prevent unintended behaviour
    start_button.config(state=DISABLED)

    global reps
    reps += 1
    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * SECONDS_IN_MIN)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * SECONDS_IN_MIN)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(WORK_MIN * SECONDS_IN_MIN)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count: int):
    """
    Function to decrease the number of seconds depending on whether the user is working or on a break. The
    value is then expressed in the GUI as "Minutes:Seconds" (e.g. 25:00).
    :param count: The number of seconds remaining in the repetition cycle.
    :return: None
    """
    global reps
    mins_left = count // SECONDS_IN_MIN
    secs_left = count % SECONDS_IN_MIN

    if 0 <= secs_left <= 9:
        secs_left = "0" + str(secs_left)
    canvas.itemconfig(timer_text, text=f"{mins_left}:{secs_left}")
    if count > 0:
        # invoke the count-down function after a delay of 1 second with 1 less second left in the count
        global timer
        timer = window.after(MS_IN_S, count_down, count - 1)
    else:
        # restart the timer after the repetition cycle completes
        start_timer()
        work_sessions = reps // 2

        # number of work cycles completed indicated as check marks
        for _ in range(work_sessions):
            new_text = CHECK_MARK * work_sessions
            check_mark_label.config(text=new_text)


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Pomodoro")
window.config(padx=PADDING_X, pady=PADDING_Y, bg=YELLOW)

# Canvas
canvas = Canvas(width=IMAGE_WIDTH, height=IMAGE_HEIGHT, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=IMAGE_PATH)
canvas.create_image(IMAGE_WIDTH / 2, IMAGE_HEIGHT / 2, image=tomato_img)
timer_text = canvas.create_text(IMAGE_WIDTH / 2, IMAGE_HEIGHT / 2 + OFFSET, text=CLOCK_START, fill=CLOCK_COLOR,
                   font=(FONT_NAME, 26, "bold"))
canvas.grid(column=1, row=1)

# Title Label
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 35, "bold"))
title_label.grid(column=1, row=0)

# Start Button
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

# Reset Button
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

# Checkmark Label
check_mark_label = Label(fg=GREEN, bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 20, "bold"))
check_mark_label.grid(column=1, row=3)

window.mainloop()
