
import math
def get_total(arr):

    count = 0

    arr.sort()
    i = 0
    while i < (len(arr)-1):
 
        # A valid pair is found
        if (math.isclose(arr[i],arr[i + 1])):
            count += 1

            print(arr[i],arr[i + 1])
            i = i + 2
 
        else:
            i += 1
 
    return count

    # for i in arr:
    #     for j in arr:

    #         if math.isclose(i,j ,rel_tol =3):
    #             count +=1
    # print(math.isclose(a,b ,rel_tol =3))


    return count

def get_total1(arr):

    count = 0
    d= {}
    l = []
    for i in arr:

        d[i] = d.get(i,0) + 1
    print(d)
    import math
    a = (0.2 * 0.2)
    b = 0.2 + 0.2
    print(math.isclose(a,b ,rel_tol =3))

    if float(a) == float(b):
        print("inside if")
    else:
        print("im else")

    for key , value in d.items():
        # print(type(value) ,value)
        if value >= 2:
            count +=1
    # print(count)
    return count

print( "Count :" ,get_total([1,2,3,5,6,7,8,1,8 ,8.1,8.0 ,8.01 ,8.01 ,1,1]))   


####################OutPUT #################

1 1
1 1
8 8
8.01 8.01

Count : 4
