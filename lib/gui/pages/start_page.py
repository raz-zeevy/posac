import tkinter as tk
from ttkbootstrap import Button


class TextAnimator(tk.Frame):
    def __init__(self, parent, word, font=('Times', 86,), delay=150, *args,
                 **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.word = word
        self.index = 0
        self.delay = delay
        self.font = font
        # Create the label to display the animated text
        self.display_label = tk.Label(self, font=self.font, text="",
                                      padx=10)
        self.display_label.pack()

    def animate_text(self):
        if self.index <= len(self.word):
            self.display_label.config(text=self.word[:self.index])
            self.index += 1
            self.after(self.delay,
                       self.animate_text)  # Schedule next letter animation

    def reset_animation(self):
        self.index = 0  # Reset the index
        self.display_label.config(text="")  # Clear the label text
        self.animate_text()  # Restart the animation


class StartPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, borderwidth=1, relief=tk.SUNKEN, *args,
                         **kwargs)
        self._parent = parent
        self._create_widgets()

    def _create_widgets(self):
        # Embedding TextAnimator widget into the window
        word_to_animate = "P  O  S  A  C"
        self.title_frame = tk.Frame(self)
        self.title_frame.pack(fill="x", expand=True, pady=15)

        self.animator = TextAnimator(self.title_frame, word_to_animate)
        self.animator.pack()

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(fill="x", expand=True, pady=0)

        # Create buttons: What is Posac? and Exit
        about_frame = tk.Frame(buttons_frame)
        about_frame.pack(side="left", fill="x", expand=True)
        exit_frame = tk.Frame(buttons_frame)
        exit_frame.pack(side="left", fill="x", expand=True)

        what_is_posac_button = Button(about_frame, text="What is POSAC?",
                                      width=15)
        what_is_posac_button.pack()

        self.exit_button = Button(exit_frame, text="Exit", width=15)
        self.exit_button.pack()

    def pack(self, *args, **kwargs):
        # Restart the animation every time the frame is packed
        self.animator.reset_animation()
        super().pack(*args, **kwargs)  # Call the original pack method