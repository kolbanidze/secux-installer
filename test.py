import customtkinter as ct


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Test")
        self.geometry("640x480")

        self.end_button = ct.CTkButton(self, text="DESTROY")
        self.end_button.pack(padx=10, pady=30)

        self.page1_frame = ct.CTkFrame(self)
        self.page1_button = ct.CTkButton(self.page1_frame, text="Page 1", command=self.show_page2)
        self.page1_button.pack()
        self.page1_menu = ct.CTkOptionMenu(self.page1_frame)
        self.page1_menu.pack()

        self.page2_frame = ct.CTkFrame(self)
        self.page2_button = ct.CTkButton(self.page2_frame, text="Page 1", command=self.show_page1)
        self.page2_button.pack()
        self.page2_menu = ct.CTkOptionMenu(self.page2_frame)
        self.page2_menu.pack()

        self.page1_frame.pack()

        self.end_button.configure(command=lambda: (self.page1_frame.destroy(), self.page2_frame.destroy()))

    def show_page2(self):
        ct.set_widget_scaling(0.5)
        self.page1_frame.pack_forget()
        self.page2_frame.pack()

    def show_page1(self):
        ct.set_widget_scaling(2)
        self.page2_frame.pack_forget()
        self.page1_frame.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()