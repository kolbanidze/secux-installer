from subprocess import run, PIPE

process = run("[ -d /sys/firmware/efi ] && echo -n UEFI || echo -n BIOS", shell=True, capture_output=True)
if process.stdout == b"UEFI":
    uefi = True