def detect_lucky():
    x = []
    number = input()
    digits = number.encode()
    new_digits = [digits[i:i + 1] for i in range(len(digits))]
    for i in new_digits:
        y = int(i)
        x.append(y)
    left=0
    right=0
    lfull=int(len(x))
    lhalf=int(lfull/2)
    for j in range(lhalf):
        left += x[j]
    for j in range(lhalf, lfull):
        right += x[j]
    if left == right:
        return True
    else:
        return False


# число для теста 985778