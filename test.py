from customtkinter import *

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("YO.")
        self.main_frame = CTkScrollableFrame(self)
        mainlabel = CTkLabel(self.main_frame, text="MAIN FRAME")
        next_button = CTkButton(self.main_frame, text="NEXT", command=self._next_stage)
        scaling = CTkOptionMenu(self.main_frame, values=["80%", "100%", "125%", "150%"], command=self._scaling_handler)
        self.main_frame.pack(fill='both', expand=True)
        mainlabel.pack(padx=10, pady=5)
        next_button.pack(padx=10, pady=5)
        scaling.pack(padx=10, pady=5)
        # self.main_frame.pack_forget()
        self.second_frame = CTkScrollableFrame(self)
        return_button = CTkButton(self.second_frame, text="Return to main frame", command=self._return_to)
        return_button.pack(padx=10, pady=5)
    
    def _scaling_handler(self, value):
        value = int(value.replace("%", "")) / 100
        set_widget_scaling(value)
        # set_window_scaling(value)
    
    def _next_stage(self):
        self.main_frame.pack_forget()
        self.second_frame.pack(fill='both', expand=True)
    
    def _return_to(self):
        self.second_frame.pack_forget()
        self.main_frame.pack(fill='both', expand=True)

if __name__ == "__main__":
    App().mainloop()
# I'll commit it for history.
# That script has proven that flexible scalable widgets EXISTS in customtkinter :)
# glhf 18.02.2025
# thx ndtp for such opportunity