from customtkinter import *
import subprocess
import threading

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("TEST")
        self.console = CTkTextbox(self)
        self.console.pack(padx=10, pady=10, fill='both')
        self.execution()
    
    def execution(self):
        self.commands = []
        self._execute("echo Hello, World")
        self._execute("speedtest")
        self._execute("echo Brave new world.")
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
                    # Run the command
                    if "input" in cmd:
                        process = subprocess.Popen(
                            cmd["command"],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            text=True,
                            bufsize=1  # Line-buffered output
                        )
                        process.stdin.write(cmd["input"])
                        process.stdin.close()
                    else:
                        process = subprocess.Popen(
                            cmd["command"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            text=True,
                            bufsize=1  # Line-buffered output
                        )

                    # Update the console in real-time
                    self.console.configure(state="normal")
                    for line in process.stdout:
                        self.console.insert(END, line)
                        self.console.see(END)
                    for line in process.stderr:
                        self.console.insert(END, line)
                        self.console.see(END)

                    process.stdout.close()
                    process.stderr.close()
                    process.wait()  # Ensure the process finishes

                    self.console.configure(state="disabled")
                except Exception as e:
                    self.console.configure(state="normal")
                    self.console.insert(END, f"Error: {str(e)}\n")
                    self.console.configure(state="disabled")
                    self.console.see(END)

        # Run the commands in a separate thread to avoid blocking the UI
        threading.Thread(target=run_commands, daemon=True).start()

if __name__ == "__main__":
    App().mainloop()