import numpy as np

n, err = 0, 0
result = []
while True:
    n += 1
    if err == 0:
        a1 = np.random.randint(2,10)
        a2 = np.random.randint(2,10)
    a3 = input(f"{a1} * {a2} = ")
    try:
        a3 = int(a3)
    except:
        print("Ошибка")
        continue

    if a3 == 0:
        if n > 30:
            break
        else:
            print("Решено мало примеров. Надо продолжать")
            err = 1
            continue

    if a3 == (a1 * a2):
        print("Верно")
        err = 0
    else:
        print("Ошибка")
        err = 1
        result.append((a1, a2, a3))
    
print("===============================================")
print(f"Решено {n} примеров")
if len(result) == 0:
    print("Ошибок нет")
else:
    print(f"Твои ошибки: ({len(result)})")
    for a in result:
        print(f"{a[0]} * {a[1]} = {a[2]}")