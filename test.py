a = ["linux", 'linux-headers', 'linux-lts', 'linux-lts-headers']
for i in a:
    if 'headers' in i:
        a.remove(i)
print(a)