# tmp = 'Привет пока 12 когда 11 что где'


def solution():
    x = input().split()
    y = []
    z = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    z = set(z)
    for i in range(len(x)-1):
        if x[i][0] in z:
            continue
        elif x[i+1][0] in z:
            continue
        else:
            if x[i] in y:
                y.append(x[i+1])
                print(x[i]+' '+x[i+1])
            else:
                y.append(x[i])
                y.append(x[i + 1])
                print(x[i]+' '+x[i+1])
    if len(y)==0:
        print("Мало слов!")