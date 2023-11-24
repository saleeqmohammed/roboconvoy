globalVar =None


def add_to_global_var(num:int):
    global globalVar
    globalVar +=num
def set_global_var():
    global globalVar
    globalVar=0

print(globalVar)

set_global_var()
print(globalVar)
add_to_global_var(2)
print(globalVar)