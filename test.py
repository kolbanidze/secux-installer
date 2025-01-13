import subprocess

def list_partitions(drive):
    result = subprocess.run(['lsblk', '-ln', '-o', 'NAME,TYPE'], stdout=subprocess.PIPE, text=True)
    partitions = []
    for line in result.stdout.splitlines():
        name, type_ = line.split()
        if type_ == 'part' and name.startswith(drive.replace('/dev/', '')):
            partitions.append(f"/dev/{name}")
    return partitions

drive = "/dev/sda"
partitions = list_partitions(drive)
print("Partitions:", partitions)
