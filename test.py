from customtkinter import *
import subprocess
import threading
import os
from secrets import token_hex, randbelow

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Testing")
        CTkLabel(self, text="ALASDIOHAUHFIDSF").pack()
        self.console = CTkTextbox(self)
        self.console.pack(fill='both', expand=True)
        self.commands = []
        for _ in range(5):
            self._execute(f'echo Trying to trigger segfault... {token_hex(randbelow(256))}')
        self._execute("passwd bsd", input="bsd\nbsd")

        self._execute_commands(self.commands)

    def _execute(self, command: str, input: str = None):
        if input:
            self.commands.append({"command": command, "input": input})
        else:
            self.commands.append({"command": command})

    def _execute_commands(self, commands: list):
        def run_commands():
            for cmd in commands:
                try:
                    print(f"Executing: {cmd['command']}")
                    process = subprocess.Popen(
                        cmd["command"],
                        stdin=subprocess.PIPE if "input" in cmd else None,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True,
                        text=True,
                        executable="/bin/bash",
                        bufsize=1  # Line-buffered output
                    )
                    if "input" in cmd:
                        process.stdin.write(cmd["input"])
                        process.stdin.close()

                    def update_console(text):
                        self.console.configure(state="normal")
                        self.console.insert(END, text)
                        self.console.see(END)
                        self.console.configure(state="disabled")

                    for line in process.stdout:
                        print(line, end="")
                        self.console.after(0, update_console, line)

                    for line in process.stderr:
                        print(line, end="")
                        self.console.after(0, update_console, line)

                    process.wait()
                    print("\n")

                except Exception as e:
                    self.console.after(0, update_console, f"Error: {str(e)}\n")

        threading.Thread(target=run_commands, daemon=True).start()


if __name__ == "__main__":
    if os.getuid() != 0:
        print("run as root plz.")
        exit(1)
    App().mainloop()