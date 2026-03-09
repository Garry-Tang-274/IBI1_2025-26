a=5.08
b=5.33
c=5.55
d=b-a
e=c-b
if e>d:
    print("Population growth is accelerating.")
elif e<d:
    print("Population growth is decelerating.")
else:
    print("Population growth rate remains unchanged.")
# Result: Population growth is decelerating because d>e.
X=True
Y=False
W=X or Y
print ("The value of W is:", W)
# Truth Table of W
# X    | Y    | W (X OR Y)
# ------------------------
# True | True | True
# True | False| True
# False| True | True
# False| False| False
# In this code, X=True and Y=False, so W=True