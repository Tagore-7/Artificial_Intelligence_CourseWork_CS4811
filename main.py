import sys
import random
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

patterns_responses = {
    r"(hello|hi|hey)": [
        "Hello there! How can I assist you today?",
        "Hi! What's on your mind?",
        "Hey! How can I help you?"
    ],
    r"my name is|I'm ([\w\s]+)": [
        "Nice to meet you, {1}! How can I assist you?",
        "Hello, {1}! How can I be of service?",
        "Welcome, {1}! What's on your mind?"
    ],
    r"i feel (?:lost|confused)": [
        "Can you tell me more about what's on your mind?",
        "When did you start feeling this way?",
        "That's okay, we all experience it sometimes. What's troubling you?"
    ],
    r"how (?:can|do) (?:i|you) (?:find|achieve) (?:happiness|joy)": [
        "What typically brings joy to your heart?",
        "Finding happiness can be a lifelong journey. What small steps can you take toward it?",
        "Achieving happiness often involves self-discovery. What makes you feel truly alive?"
    ],
    r"(?:procrastinat|delay) (?:work|tasks|responsibilities)": [
        "Procrastination can be a challenge. What usually triggers your procrastination?",
        "How do you feel when you delay your tasks? Let's explore this further.",
        "Procrastination can be a form of self-sabotage. What do you think might be causing it?"
    ],
    r"why do (?:we|people) (?:dream|have dreams)": [
        "What's a recent dream you've had?",
        "Dreams can be fascinating. Can you recall a recurring dream?",
        "If dreams could speak, what do you think they'd say about you?"
    ],
    r"(?:what do you|tell me about your) (?:thoughts on|opinion about) (?:love|romance)": [
        "Love is a complex emotion. How do you perceive it?",
        "Love, an age-old question! How would you define romance?"
    ],
    r"life is (?:unfulfilling|meaningless)": [
        "I'm here to help you explore your feelings. What aspects of your life feel unfulfilling?",
        "Finding meaning in life can be challenging. Have you identified any specific goals or passions?",
        "Let's discuss changes you could make to find more fulfillment."
    ],
    r"i can\'?t (?:sleep|rest) properly": [
        "Sleep issues can be distressing. Can you describe your sleep patterns and any possible causes?",
        "What thoughts or worries keep you awake at night?",
        "Have you tried any relaxation techniques to improve your sleep?"
    ],
    r"i have (?:anxiety|panic attacks)": [
        "I'm here to support you. When do these feelings of anxiety or panic usually occur?",
        "Addressing anxiety is important. Have you considered professional help or coping strategies?"
    ],
    r"my job is (?:stressful|unfulfilling)": [
        "Tell me more about your job and what specifically makes it stressful or unfulfilling.",
        "What do you enjoy about your job, if anything?",
        "Have you considered discussing your concerns with your supervisor or seeking new opportunities?"
    ],
    r"i can\'?t (?:focus|concentrate) on anything": [
        "Lack of focus can be frustrating. Can you describe the situations where you struggle to concentrate?",
        "Are there any distractions or external factors that might be affecting your concentration?"
    ],
    r"i\'m (?:lonely|isolated) and have no one to talk to": [
        "I'm here to chat with you. What's been causing you to feel lonely or isolated?",
        "Are there any activities or hobbies that you used to enjoy and could revisit to connect with others?"
    ],
    r"i\'m (?:overwhelmed|burdened) by responsibilities": [
        "It sounds like you have a lot on your plate. Can you list some of your main responsibilities?",
        "Feeling overwhelmed is common when we have too much to handle. Have you considered prioritizing your tasks?",
        "What would be the ideal outcome for you in terms of managing your responsibilities?"
    ],
    r"i (?:procrastinate|delay) too much": [
        "Procrastination can be challenging. What tasks or activities tend to be postponed most frequently?",
        "What factors do you think contribute to your tendency to delay these tasks?"
    ],
    r"my (?:self-esteem|confidence) is (?:low|fragile)": [
        "Self-esteem is important. Can you identify situations that have negatively impacted your self-esteem?",
        "What positive qualities or achievements can you remind yourself of?",
        "Let's work on building your self-esteem together. What steps can you take?"
    ],
    r"i have (?:relationship|marital) issues": [
        "Relationships can be complex. Can you share more about the issues you're facing?",
        "Effective communication is key in relationships. How well do you and your partner communicate?",
        "Let's explore ways to enhance your relationship or find resolutions."
    ],
    r"i feel (?:trapped|stuck) in my current situation": [
        "Feeling stuck can be distressing. What specific aspects of your current situation contribute to this feeling?",
        "Have you considered exploring alternatives or changes to improve your situation?",
        "Let's brainstorm potential solutions as you explore your options."
    ],
    r"i have (?:trust|betrayal) issues": [
        "Trust is a vital aspect of relationships. Can you elaborate on the trust-related concerns you're facing?",
        "Have you discussed your concerns with the person involved?"
    ],
    r"tell me a joke|joke": [
        "Sure, here's one: Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Here's a classic: Why don't scientists trust atoms? Because they make up everything!",
        "How about this one: Parallel lines have so much in common. It's a shame they'll never meet!"
    ]
}

name_introductions = [
    "Hi, I don't believe we've met. What's your name?",
    "Hello there, I'm ELIZA. May I ask for your name?",
    "Nice to meet you! What should I call you?",
    "Hi, I'm ELIZA. And you are?",
    "Pardon my manners, but I don't know your name yet. What is it?",
    "Hey, I'm ELIZA. What do your friends call you?",
    "I'm ELIZA, by the way. What's your name?",
    "Greetings! Before we dive into conversation, can you share your name with me?",
    "Hello, stranger! Mind sharing your name with me?",
    "I'm ELIZA, and you are...?",
    "It's a pleasure to meet you. Can I get your name?",
    "Hey, I'm ELIZA. And you?",
    "Hi, I'm ELIZA. What should I call you?",
    "Nice to make your acquaintance. May I know your name?",
    "Hello! I'm ELIZA, and you are?",
    "Before we get into our conversation, can you introduce yourself with your name?",
    "I'm ELIZA. What's your name?",
    "I'm ELIZA, and I'd love to know your name.",
    "Hi, I'm ELIZA. What do you go by?"
]

name_responses = [
    "{}? What a great name! I'm ELIZA. What would you like to talk about?",
    "Pleased to make your acquaintance, {}. What would you like to talk about?",
    "Thanks for sharing your name, {}. How can I help you today?",
    "Hi there, {}! I'm ELIZA. What would you like to talk about?",
    "{}, it's a pleasure to know your name. What would you like to talk about?",
    "Hello, {}! I'm delighted to meet you. How can I help you today?",
    "Great to have you here, {}. What would you like to talk about today?",
    "{}, I'm glad to know who you are. What would you like to talk about?",
    "{}, welcome! How can I help you today?",
    "It's wonderful to meet you, {}. How can I help you today?"
]

default_responses = [
    "Tell me more, {}...",
    "I hear what you're saying.",
    "Tell me more about that.",
    "How does that make you feel?",
    "I'm here to listen, and I won't judge you.",
    "I appreciate your honesty.",
    "Let's explore that further.",
    "It seems like you've put a lot of thought into this.",
    "I'm listening with an open heart and mind.",
    "I'm grateful that you're sharing this with me.",
    "You have my full attention."
]

feelings_responses = [
    "I hear you're feeling {}, can you tell me more about that?",
    "It sounds like you're feeling {}. How does that make you feel?",
    "Tell me more about your feelings of {}.",
    "Feelings of {} are important. Can you elaborate?",
    "I'm here to listen. What's behind your feelings of {}?",
]

rules = {
    "hello|hi|hey": "name_introductions",
    "my name is|I'm": "name_responses",
    "feelings": "feelings_responses",
    "default": "default_responses"
}

class ChatbotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Eliza Clone")
        self.setGeometry(100, 100, 400, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.chat_history.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_history.setStyleSheet(
            """
            QTextEdit {
                background-color: #f4f4f4;
                border: none;
                padding: 12px;
                font-size: 16px;
                font-family: Segoe UI;
            }
            """
        )
        layout.addWidget(self.chat_history)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Type your message here...")
        self.user_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #f4f4f4;
                border: none;
                padding: 12px;
                font-size: 16px;
                font-family: Segoe UI;
            }
            """
        )
        layout.addWidget(self.user_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet(
            """
            QPushButton {
                background-color: #00adef;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                font-family: Segoe UI;
                border: none;
            }
            QPushButton:hover {
                background-color: #0090d1;
            }
            """
        )
        layout.addWidget(self.send_button, alignment=Qt.AlignRight)

        self.central_widget.setLayout(layout)

        self.send_button.clicked.connect(self.handle_user_input)
        self.user_input.returnPressed.connect(self.handle_user_input)

        self.user_name = None
        self.awaiting_name = True
        self.chat_history.append("<font color='green'>Eliza Clone:</font> Please enter your name:")
        self.user_input.setPlaceholderText("Your Name")

    def eliza_response(self, input_text):
        input_text = input_text.lower()
        for pattern, response_list in patterns_responses.items():
            if re.search(pattern, input_text):
                response = random.choice(response_list)
                return response.format(name=self.user_name)
        return random.choice(default_responses).format(name=self.user_name)

    def handle_user_input(self):
        user_input = self.user_input.text().strip()
        if self.awaiting_name:
            self.user_name = user_input
            self.chat_history.clear()
            self.chat_history.append(f"<font color='green'>Eliza Clone:</font> Hello, {self.user_name}! How can I help you today?")
            self.awaiting_name = False
            self.user_input.clear()
            self.user_input.setPlaceholderText("Type your message here.")
        else:
            if user_input:
                self.chat_history.append(f"<font color='blue'>{self.user_name}:</font> {user_input}")
                bot_response = self.eliza_response(user_input)
                self.chat_history.append("<font color='green'>Eliza Clone:</font> " + bot_response)
                self.user_input.clear()

def main():
    app = QApplication(sys.argv)
    window = ChatbotApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
