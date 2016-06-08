import random
def say_hello():
    messages = ["Hello", "At your service, sir.", "Hey there.", "How are you?"]
    message = messages[random.randint(0, len(messages) - 1)]
    return [{"text": message}]


def say_goodbye():
    messages = ["Goodbye.", "See you soon.", "Talk to you later.", "Bye Bye (y)"]
    message = messages[random.randint(0, len(messages) - 1)]
    return [{"text": message}]
