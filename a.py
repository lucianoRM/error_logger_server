import random
import string

words = []
for i in xrange(800):
    words.append(''.join(random.choice(string.lowercase) for i in range(10)))

print words


