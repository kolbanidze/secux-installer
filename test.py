from customtkinter import *
import subprocess
import threading

class TestApp(CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Test APP")
        self.geometry("600x400")

        self.label = CTkLabel(self, text="Console output")
        self.console = CTkTextbox(self, state="disabled")

        self.label.pack(padx=10, pady=10)
        self.console.pack(padx=10, pady=10, side="bottom", fill="both", expand=True)
        self.begin_installation()

    def _execute(self, command: str, input: str = None):
        if input:
            self.commands.append({"command": command, "input": input})
        else:
            self.commands.append({"command": command})

    def _execute_commands(self, commands: list):
        def run_commands():
            for cmd in commands:
                try:
                    # Run the command
                    if "input" in cmd:
                        process = subprocess.Popen(
                            cmd["command"],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            text=True
                        )
                        stdout, stderr = process.communicate(input=cmd["input"])
                    else:
                        process = subprocess.Popen(
                            cmd["command"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            text=True
                        )
                        stdout, stderr = process.communicate()

                    # Update the console with the output
                    self.console.configure(state="normal")
                    if stdout:
                        self.console.insert(END, stdout + "\n")
                    if stderr:
                        self.console.insert(END, stderr + "\n")
                    self.console.configure(state="disabled")

                    self.console.see(END)  # Scroll to the end of the console
                except Exception as e:
                    self.console.configure(state="normal")
                    self.console.insert(END, f"Error: {str(e)}\n")
                    self.console.configure(state="disabled")
                    self.console.see(END)

        # Run the commands in a separate thread to avoid blocking the UI
        threading.Thread(target=run_commands, daemon=True).start()

    def begin_installation(self):
        self.commands = []
        self._execute("echo Hello, World!")
        self._execute("ping google.com -c 3")
        self._execute("sudo passwd jdoe", input="12345678\n12345678\n")
        self._execute("echo Hello, World! Again...")

        self._execute_commands(self.commands)
if __name__ == "__main__":
    TestApp().mainloop()
