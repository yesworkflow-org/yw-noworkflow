# @begin HelloWorld @desc Exercise YW and NW with a classic program.
# @in provided_greeting
# @out displayed_greeting @desc Greeting displayed to user.

# @begin print_greeting @desc Greet the program user.
# @in greeting @as provided_greeting
# @out displayed_greeting @file stream:stdout
def print_greeting(greeting):
    print(greeting)
# @end print_greeting

# @end HelloWorld

if __name__ == '__main__':
    first_greeting = 'Hello World!'
    print_greeting(first_greeting)
    second_greeting = 'Goodbye World!'
    print_greeting(second_greeting)
