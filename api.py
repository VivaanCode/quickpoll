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
    if id in polls:
        return createId()
    return id

def createPoll(question, *args):
    print(question)
    print(args)
    id = createId()

    votes = [0] * len(args)

    polls[id] = {
        "question": question,
        "options": args,
        "votes": votes
    }

    return id

def getPoll(id):
    return polls.get(id, None)

def vote(id, option):
    poll = getPoll(id)
    if poll:
        if option in poll["options"]:
            index = poll["votes"].index(option)
            poll["votes"][index] += 1
            return True
    return False

