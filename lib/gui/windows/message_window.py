import ttkbootstrap as ttk

from lib.gui.const import p_ICON
from lib.utils import get_resource, real_size, rreal_size

from .window import Window


class MessageWindow(Window):
    """
    A custom message dialog window with enhanced visual styling.
    Can be used for both information messages and yes/no questions.
    """

    @classmethod
    def show_message(cls, parent, message, title=None):
        """Show an information message with an OK button"""
        return cls.show_dialog(parent, message=message, title=title)

    @classmethod
    def show_question(
        cls,
        parent,
        message,
        title=None,
        yes_command=None,
        no_command=None,
        buttons=None,
    ):
        """Show a question message with Yes/No buttons"""
        if buttons is None:
            buttons = ["Yes:primary", "No:secondary"]

        return cls.show_dialog(
            parent,
            message=message,
            title=title,
            is_question=True,
            yes_command=yes_command,
            no_command=no_command,
            buttons=buttons,
        )

    def setup_window(
        self,
        message="",
        title=None,
        is_question=False,
        yes_command=None,
        no_command=None,
        buttons=None,
    ):
        """Set up the message window with appropriate widgets"""
        if buttons is None:
            buttons = ["Yes:primary", "No:secondary"]

        self.title(title if title else "Message")
        self.iconbitmap(get_resource(p_ICON))
        self.resizable(False, False)

        # Create the message frame with enhanced padding and border
        frame = ttk.Frame(
            self, padding=(rreal_size(25), rreal_size(20)), bootstyle="light"
        )
        frame.pack(fill="both", expand=True)

        # Add a header with a different background if title is provided
        if title:
            header_frame = ttk.Frame(frame, bootstyle="primary")
            header_frame.pack(fill="x", side="top", pady=rreal_size((0, 15)))
            header_label = ttk.Label(
                header_frame,
                text=title,
                font=("Segoe UI", rreal_size(12), "bold"),
                bootstyle="inverse-primary",
                padding=rreal_size(10),
            )
            header_label.pack(fill="x")

        # Message label with improved styling
        message_label = ttk.Label(
            frame,
            text=message,
            wraplength=real_size(400),
            justify="center",
            font=("Segoe UI", rreal_size(10)),
            padding=(rreal_size(5), rreal_size(10)),
        )
        message_label.pack(pady=rreal_size(15), fill="both", expand=True)

        # Separator line
        separator = ttk.Separator(frame)
        separator.pack(fill="x", pady=rreal_size(10))

        # Buttons frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=rreal_size((5, 10)), fill="x")

        if is_question:
            # Create "Yes" and "No" buttons for question dialog
            yes_button_text = buttons[0].split(":")[0]
            yes_button_style = (
                buttons[0].split(":")[1] if ":" in buttons[0] else "primary"
            )

            no_button_text = buttons[1].split(":")[0]
            no_button_style = (
                buttons[1].split(":")[1] if ":" in buttons[1] else "secondary"
            )

            def on_yes():
                self.result = yes_button_text
                self.destroy()
                if yes_command:
                    yes_command()

            def on_no():
                self.result = no_button_text
                self.destroy()
                if no_command:
                    no_command()

            # Pack the buttons to the right side
            button_frame.columnconfigure(0, weight=1)  # Make left column expandable

            yes_button = ttk.Button(
                button_frame,
                text=yes_button_text,
                bootstyle=yes_button_style,
                command=on_yes,
                width=rreal_size(10),
            )
            yes_button.grid(row=0, column=1, padx=rreal_size(5))

            no_button = ttk.Button(
                button_frame,
                text=no_button_text,
                bootstyle=no_button_style,
                command=on_no,
                width=rreal_size(10),
            )
            no_button.grid(row=0, column=2, padx=rreal_size(5))

            # Set focus to the yes button
            yes_button.focus_set()
        else:
            # Create "OK" button for info dialog
            def on_ok():
                self.result = "OK"
                self.destroy()

            # Center the OK button
            button_frame.columnconfigure(0, weight=1)
            button_frame.columnconfigure(2, weight=1)

            ok_button = ttk.Button(
                button_frame,
                text="OK",
                bootstyle="primary",
                command=on_ok,
                width=rreal_size(10),
            )
            ok_button.grid(row=0, column=1, padx=rreal_size(5))

            # Set focus to the OK button
            ok_button.focus_set()

        # Add a slight shadow effect with a border
        self.configure(borderwidth=rreal_size(1), relief="ridge")
