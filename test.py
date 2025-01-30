a = ["linux", "linux-lts", "linux-hardened"]
b = " ".join(a) + " " + " ".join([i+"-headers" for i in a])
print(b)