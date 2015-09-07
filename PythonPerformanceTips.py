
# An alternative way to speed up sorts is 
# to construct a list of tuples whose first 
# element is a sort key that will sort properly
# using the default comparison, and whose second element
# is the original list element. This is so-called
# "Schwartzian Transfrom"


# The default wat to sort by the n-th field of each tuple
def sortby(somelist, n):
	nlist = [(x[n], x) for x in somelist]
	nlist.sort()
	return [val for (key, val) in nlist]


# Sorting inplace method
def sortby_inplace(somelist, n):
	somelist[:] = [(x[n], x) for x in somelist]
	somelist.sort()
	somelist[:] = [val for (key,val) in somelist]
	return

somelist = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
somelist.sort()

# Need spend more time on python sorting study

# Tips in String manipulation in python

# String Concatenation avoid case
s1 = ""
s2 = ""
list1 = ['physics','chemistry', '1997', '2000']

for x in list1:
	s1 += x

print ("list s1" + s1)

# String concatenation correct method
s2 = "".join(list1)

print ("list s2" + s2)

# Python tips - avoid use loop but map
oldlist = ["amazon","skybox"]
newlist1 = []
newlist2 = []

for word1 in oldlist:
	newlist1.append(word1.upper())
print "List from for loop", newlist1[:]

newlist2 = map(str.upper, oldlist)
print "List from map", newlist2[:]







