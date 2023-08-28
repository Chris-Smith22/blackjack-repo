letters = ['a', 'b', 'c', 'e']
print(letters)
#letters.insert(3, 'd')
#print(letters)

for l in letters:
    if l == 'c':
        letters.insert(3, 'd')

    print(l)

print(letters)