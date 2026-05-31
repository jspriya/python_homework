import traceback

try:
    input_not_first =" "
    with open("diary.txt", mode='a') as file:
        input_first = input("What happened today? ")
        file.write(input_first  + "\n")

        while input_not_first != "done for now":

            input_not_first = input("What else?")
            file.write(input_not_first  + "\n")

            if input_not_first != "done for now":
                    file.write(input_not_first + "\n")

except Exception as e:
    print("An exception occurred.")
    print(type(e).__name__)   
    traceback.print_exc() 

