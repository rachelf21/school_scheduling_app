# groceries = {1:1, 2:4, 3:9, 4:16}
#
# for value in groceries.values():
#     print(value)

doubles = {}
for x in range(1,11):
    doubles[x]=x*2

print(doubles.values())

if 1 in doubles:
    print("yes")

for key in doubles:
    print(doubles[key])

print(any(doubles))

d = dict()
for x in range(1,6):
    d[x] = x*2

print(d)