import random

# ch = [] # 포함할 수
ch = [1, 3, 5, 6, 7,
      9, 11, 13,
      15, 16, 17, 19, 21,
      22, 23, 25, 26, 27,
      29, 31, 33, 35,
      36, 37, 39, 41, 43, 45]
ch = set(ch)

result = random.sample(ch, 6)
result.sort()
print(result)
