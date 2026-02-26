import random

polls = {
    # 1 : {
    #     "question": "What is your favorite color?",
    #     "options": ["Red", "Green", "Blue"],
    #     "votes": [0, 0, 0]
    # }
}

def createId():
    id = ""
    for i in range(6):
        id += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return id

def createPoll(question, *args):
    print(question)
    print(args)