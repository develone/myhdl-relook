l = 192
s = 159
r = 159
ll = 160

print "Even"
e = l + r + 2
f = e >>2 
res = s + f

print e,f,res
ires = res - f
print ires
print "Odd"
print "l    s    r"
print l,s,r
e = l >>1
f = r >>1
res = s - (e + f)
print "l>>1    r>>1  res"
print e,f,res
ires = res + (e + f)
print "ires"
print ires
ap = l
b = s
cp = r
ap = ap - b
d = ll
cp = cp - ((b+d)>>1)
print "ap b cp d"
print ap,b,cp,d

