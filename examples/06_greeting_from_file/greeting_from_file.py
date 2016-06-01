import csv

# @begin greetings_from_file @desc Compose and display custom greetings defined in a file.
# @param input_file_path
# @param input_file
# @out displayed_greeting @desc Greeting displayed to user.

def greet_user(input_file_path):

    # @begin read_greeting_definitions @desc Read the greeting definitions from the file
    # @param input_file_path
    # @in input_file
    # @out greeting @as provided_greeting
    # @out emphasis  @as provided_emphasis
    # @out count @as emphasis_count
    input_file = open(input_file_path, 'rt')
    greeting_definitions = csv.DictReader(input_file)

    for greeting_def in greeting_definitions:

        greeting = greeting_def['text']
        emphasis = greeting_def['emphasis']
        count = int(greeting_def['count'])

    # @end read_greeting_definitions

        # @begin emphasize_greeting @desc Add emphasis to the provided greeting
        # @in greeting @as provided_greeting
        # @in emphasis @as provided_emphasis
        # @param count @as emphasis_count
        # @out greeting @as emphasized_greeting
        greeting = add_suffix(greeting, emphasis, count)
        # @end emphasize_greeting

        # @begin print_greeting @desc Greet the user with the emphasized message.
        # @in greeting @as emphasized_greeting
        # @out greeting @as displayed_greeting @file stream:stdout
        print(greeting)
        # @end print_greeting

# @end greetings_from_file

def add_suffix(prefix, suffix, count):
    string = prefix
    if (count > 0):
        for i in range(0, count):
            string = string + suffix
    return string

if __name__ == '__main__':
    greet_user('input.csv')
