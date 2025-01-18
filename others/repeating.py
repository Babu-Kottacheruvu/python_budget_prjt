st = "Hello, world"

letter = input("Enter the letter to find occurance:")
occurance = 0


for i in st.lower():
    if i == letter:
        if letter == " ":
            print("Space is occured:")
            break
        occurance +=1
    
print(f"{letter} is repeated for {occurance} times.")
# print(occurance)


