from customtkinter import *
import subprocess
import threading
import os

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Testing")
        self.console = CTkTextbox(self)
        self.console.pack(fill='both', expand=True)
        self.commands = []
        for _ in range(100):
            self._execute('echo Trying to trigger segfault...')
        for _ in range(100):
            self._execute("sbsign --key sb.key --cert sb.crt --output linux.efi linux.efi")
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
                    self.console.see(END)
                    # Run the command
                    if "input" in cmd:
                        process = subprocess.Popen(
                            # f"stdbuf -oL {cmd["command"]}",
                            cmd["command"],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            text=True,
                            executable="/bin/bash",
                            bufsize=1  # Line-buffered output
                        )
                        process.stdin.write(cmd["input"])
                        process.stdin.close()
                    else:
                        process = subprocess.Popen(
                            # f"stdbuf -oL {cmd["command"]}",
                            cmd["command"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            text=True,
                            executable="/bin/bash",
                            bufsize=1  # Line-buffered output
                        )

                    # Update the console in real-time
                    self.console.configure(state="normal")
                    for line in process.stdout:
                        print(line, end="")
                        self.console.insert(END, line)
                        self.console.see(END)
                    for line in process.stderr:
                        print(line, end="")
                        self.console.insert(END, line)
                        self.console.see(END)

                    process.stdout.close()
                    process.stderr.close()
                    process.wait()  # Ensure the process finishes

                    self.console.configure(state="disabled")
                    print("\n")
                except Exception as e:
                    self.console.configure(state="normal")
                    print(f"Error: {str(e)}\n")
                    self.console.insert(END, f"Error: {str(e)}\n")
                    self.console.configure(state="disabled")
                    self.console.see(END)

        # Run the commands in a separate thread to avoid blocking the UI
        threading.Thread(target=run_commands, daemon=True).start()

if __name__ == "__main__":
    if os.getuid() != 0:
        print("run as root plz.")
        exit(1)
    App().mainloop()