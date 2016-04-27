# @begin CustomHelloWorld @desc Display one or more greetings to the user.
# @in provided_greeting
# @out displayed_greeting @desc Greeting displayed to user.

# @begin accept_greeting @desc Receive message to be displayed to the user as a greeting.
# @in greeting @as provided_greeting
# @out greeting @as custom_greeting
def print_greeting(greeting):
# @end accept_greeting

# @begin greet_user @desc Greet the program user with the given message.
# @in greeting @as custom_greeting
# @out greeting @as displayed_greeting @file stream:stdout
    print(greeting)
# @end greet_user

# @end CustomHelloWorld

if __name__ == '__main__':
    first_greeting = 'Hello World!'
    print_greeting(first_greeting)
    second_greeting = 'Goodbye World!'
    print_greeting(second_greeting)
    print_greeting("Back again!")
