
def a():
    print("A")

def b():
    print("B")

def c():
    print("C")

d = dict()

d["a"] = a
d["b"] = b
d["c"] = c

d["b"]()