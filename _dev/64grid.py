import pprint
import os
os.system('cls')

root = 0


note = 0
key = 0
inc = 0
for row in range(8):
	print('row',row)
	for col in range(8):
		note = scale[key] + (inc * 12)
		if col in[4,7]:
			print(note)
		key += 1
		if key >= len(scale):
			key = 0
		if key == 0:
			inc += 1
	inc -= 1
	key -= (len(scale) - 5)