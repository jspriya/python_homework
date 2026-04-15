import traceback

try:
    input_not_first =" "
    file = open("diary.txt", "a")

    input_first = input("What happened today? ")
    file.write(input_first  + "\n")

    while input_not_first != "done for now":

        input_not_first = input("What esle?")
        file.write(input_not_first  + "\n")
    file.close()

except Exception as e:
    print("An exception occurred.")
    print(type(e).__name__)   
    traceback.print_exc() 

