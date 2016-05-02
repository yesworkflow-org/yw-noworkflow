# @begin EmphasizedHelloWorld @desc Display one or more greetings to the user.
# @in provided_greeting
# @out displayed_greeting @desc Greeting displayed to user.

def greet_user(provided_greeting):

    # @begin emphasize_greeting @desc Add emphasis to the provided greeting
    # @in provided_greeting
    # @out greeting @as modified_greeting
    greeting = provided_greeting + '!!'
    # @end emphasize_greeting

    # @begin print_greeting @desc Greet the user with the emphasized message.
    # @in greeting @as modified_greeting
    # @out greeting @as displayed_greeting @file stream:stdout
    print(greeting)
    # @end print_greeting

# @end EmphasizedHelloWorld

if __name__ == '__main__':
    first_greeting = 'Hello World'
    greet_user(first_greeting)
    second_greeting = 'Goodbye World'
    greet_user(second_greeting)
    greet_user("Back again")
