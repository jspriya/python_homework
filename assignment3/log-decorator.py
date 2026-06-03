
import logging
import functools
import os

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))
#logger.log(logging.INFO, "this string would be logged")

def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Call the function and get the return value
        result = func(*args,**kwargs)

        #prepare log components
        func_name = func.__name__
        pos_args = args if args else "none"
        kw_args = kwargs if kwargs else "none"

        #Create log message
        log_message = (
            f"function: {func_name}\n"
            f"positional parameters: {pos_args}\n"
            f"keyword parameters: {kw_args}\n"
            f"return: {result}\n"
        )

        #Write to log
        logger.log(logging.INFO, log_message)

        return result
    return wrapper

# Function 1: no parameters, returns nothing
@logger_decorator
def say_hello():
    print("Hello, World!")

# Function 2: variable positional arguments, returns True
@logger_decorator
def positional_only(*args):
    return True

# Function 3: variable keyword arguments, returns logger_decorator
@logger_decorator
def keyword_only(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    say_hello()
    positional_only(1, 2, 3, "test")
    keyword_only(a=1, b=2, c="hello")

