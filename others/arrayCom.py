arr = [1,2,3,4,5,6,7,8,9]

arrEven = [i for i in arr if i%2 ==0]
arrOdd = [i for i in arr if i%2 !=0]

print(f"Even array Elements:{arrEven}")
print(f"Odd array Elements:{arrOdd}")