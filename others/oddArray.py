arr = [1,2,3,4,5,6,7,8,9]
odd = []

# for i in arr:
#     if(i%2)!=0:
#         # print(f"Odd Elements:",i)
#         odd=i
#     else:
#         print(f"Even Elements:",i)
# print(odd)

print("Even Elements:")
for i in arr:
    if(i%2)==0:
        print(i)
print()

print("Odd Elements:")
for i in arr:
    if(i%2)!=0:
        odd.append(i)
        print(i)

print(odd)