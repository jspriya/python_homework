# Task 1
def hello():
    return "Hello!"

# Task 2 
def greet(name):
    return f"Hello, {name}!"
print(greet("Priya"))

# Task 3
def calc(num1,num2,op='multiply'):
 try:
    if op == 'multiply': 
        result = num1 * num2
        return result
    elif op == 'add':
       result = num1 + num2
       return result
    elif op == 'subtract':
        result = num1 - num2
        return result
    elif op == 'divide':
        result = num1 / num2
        return result
    elif op == 'modulo':
        result = num1 % num2
        return result
    elif op == 'int_divide':
        result = num1 // num2
        return result
    elif op == 'power':
        result = num1 ** num2
        return result
 
 except ZeroDivisionError:
        return "You can't divide by 0!"
 except TypeError:
        return "You can't multiply those values!"
    
print(calc(4, 0,'divide'))

# Task 4 

def data_type_conversion(value,type):
    try:
        if type == 'float':
            return float(value)
        elif type == 'int':
            return int(value)
        elif type == 'str':
            return str(value)
        else:
            return "Invalid data type"
        
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {type}." 
    
print(data_type_conversion("banana", "int"))

# Task 5
def grade(*args):
    try:
        result = sum(args)/len(args)
        if result >= 90:
            grade_val = "A"
        elif result >= 80 and result < 90:
            grade_val = "B"
        elif result >= 70 and result < 80:
            grade_val = "C"
        elif result >= 60 and result < 70:
            grade_val = "D"
        else:
            grade_val = "F" 
        return grade_val
    except(TypeError, ZeroDivisionError):
        return "Invalid data was provided."
    
print(grade(25, 85, 95))

# Task 6
def repeat(str, n):
    repeat_str = ""
    for i in range(n):
        repeat_str += str
    return repeat_str   
print(repeat('hello',5))

# Task 7
def student_scores(what,**scores):
    if what =='best':
        best_student = max(scores,key= scores.get)
        return best_student
    elif what == 'mean':
        avg = sum(scores.values()) / len(scores)
        return avg
    else:
        return "Invalid mode"
    
print(student_scores("mean", A=78, B=85, C=98))

# Task 8

def titleize(str):
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]

    words = str.split()

    title_cased =[]
    last_index = len(words) - 1

    for index, word in enumerate(words):
        # Capitalize if it's the first or last word
        if index == 0 or index == last_index:
            title_cased.append(word.capitalize())
        elif word.lower() in little_words:
            title_cased.append(word.lower())
        else:
            title_cased.append(word.capitalize())

    return " ".join(title_cased)

print(titleize('road less tRAVELED'))

# Task 9

def hangman(secret, guess):

    result =[]
    for letter in secret:
        if letter in guess:
            result.append(letter)
        else:
            result.append("_") 
    return "".join(result)

print(hangman("alphabet", "ab"))

# Taks 10

def pig_latin(text):
  vowels = "aeiou"
  words = text.split()
  translated_words = []
  
  for word in words:
    if word[0] in vowels:
        translated_words.append(word + "ay")
              
    else:
        split_index = 0  
        for i in range(len(word)):
          if word[i] in vowels:
            if word[i] == 'u' and i > 0 and word[i-1] == 'q':
              continue
            else:
              split_index = i
              break
        
        beginning = word[:split_index]
        rest = word[split_index:]
        translated_words.append(rest + beginning + "ay")
          
  return " ".join(translated_words)        
            
print(pig_latin("the quick brown fox jumped over the fence"))


