import re
import difflib
import sys


class RubberDuckChatbot:
    def __init__(self):
        self.programming_languages = {

            # Add many as prrogramming languages you want and add their key words respectively
            'C': [
                "auto", "break", "case", "char",
                "const", "continue", "default", "do",
                "double", "else", "enum", "extern",
                "float", "for", "goto", "if",
                "inline", "int", "long", "register",
                "restrict", "return", "short", "signed",
                "sizeof", "static", "struct", "switch",
                "typedef", "union", "unsigned", "void",
                "volatile", "while", "_Alignas", "_Alignof",
                "_Atomic", "_Bool", "_Complex", "_Generic",
                "_Imaginary", "_Noreturn", "_Static_assert", "_Thread_local"
            ],
            'C++': [
                "asm", "auto", "bool", "break",
                "case", "catch", "char", "class",
                "const", "const_cast", "continue", "default",
                "delete", "do", "double", "dynamic_cast",
                "else", "enum", "explicit", "export",
                "extern", "false", "float", "for",
                "friend", "goto", "if", "inline",
                "int", "long", "mutable", "namespace",
                "new", "operator", "private", "protected",
                "public", "register", "reinterpret_cast", "return",
                "short", "signed", "sizeof", "static",
                "static_cast", "struct", "switch", "template",
                "this", "throw", "true", "try",
                "typedef", "typeid", "typename", "union",
                "unsigned", "using", "virtual", "void",
                "volatile", "wchar_t", "while", "and",
                "and_eq", "bitand", "bitor", "compl",
                "not", "not_eq", "or", "or_eq",
                "xor", "xor_eq"
            ],
            'java': [
                "abstract", "assert", "boolean", "break",
                "byte", "case", "catch", "char",
                "class", "const", "continue", "default",
                "do", "double", "else", "enum",
                "extends", "final", "finally", "float",
                "for", "if", "goto", "implements",
                "import", "instanceof", "int", "interface",
                "long", "native", "new", "package",
                "private", "protected", "public", "return",
                "short", "static", "strictfp", "super",
                "switch", "synchronized", "this", "throw",
                "throws", "transient", "try", "void",
                "volatile", "while", "_", "exports",
                "module", "non-sealed", "open", "opens",
                "permits", "provides", "record", "requires",
                "sealed", "to", "transitive", "uses",
                "var", "with", "yield"
            ],
            'python': [
                "False", "None", "True", "and",
                "as", "assert", "async", "await",
                "break", "class", "continue", "def",
                "del", "elif", "else", "except",
                "finally", "for", "from", "global",
                "if", "import", "in", "is",
                "lambda", "nonlocal", "not", "or",
                "pass", "raise", "return", "try",
                "while", "with", "yield", "match",
                "case"
            ]

        }

    def greet_user(self):
        print("Duck: Hello! May I know your name?")
        user_name = input("User: ")
        print(f"Duck: It's nice meeting {user_name} here! Let's talk about your program.")

    # specifies what programming language is being used
    def get_programming_language(self):
        while True:
            print("Duck: What programming language did you use for your coding?")
            user_language = input("User: ")
            if user_language in self.programming_languages:
                return user_language
            else:
                print("Duck: Please enter a valid programming language.")

    # returns each line of the file
    def get_input_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        return lines

    def process_program(self, user_language):
        print("Duck: Let's get started! Please enter your file path.")
        file_path = input("User: ")

        keywords = self.programming_languages[user_language]

        program_lines = self.get_input_file(file_path)
        print(f"program_lines: {program_lines[0]}\n")

        user_keywords = [(word.lower(), index + 1) for index, line in enumerate(program_lines) for word in
                         re.findall(r'\b\w+\b', line)]
        print(f"user_keywords: {user_keywords}")
        #         user_keywords = [word.lower() for word in re.findall(r'\b\w+\b', user_program)]
        matching_keywords = [(word, index) for word, index in user_keywords if word in keywords]
        print(f"matching_keywords: {matching_keywords}")

        for keyword, line in matching_keywords:
            print(f"Duck: What's the purpose of '{keyword}' on line {line} in your program?")
            user_explanation = input("User: ")

        print("Duck: That's an impressive program! Well done.")
        print("Duck: What does the program intend to do?")
        user_goal = input("User: ")

        print("Duck: What were your challenges while writing this program?")
        user_challenges = input("User: ")

        print("Duck: How did you solve the challenges?")
        user_solution = input("User: ")

        print("Duck: Thank you for sharing your coding experience!")

    def run_chatbot(self):
        self.greet_user()
        user_language = self.get_programming_language()
        self.process_program(user_language)


rubber_duck_chatbot = RubberDuckChatbot()
rubber_duck_chatbot.run_chatbot()
