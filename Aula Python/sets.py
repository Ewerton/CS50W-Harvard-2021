#creates an empty set
s = set()

#add elements to set
s.add(1)
s.add(2)
s.add(3)
s.add(4)
s.add(3) # mesmo repetindo o 3 ele será ignorado, pois so podem ter unique elements

print(s)

s.remove(2)

print(s)

len(s) # numero de elementos
print(f" The set has {len(s)} elements.")

