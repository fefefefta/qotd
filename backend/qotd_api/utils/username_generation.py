import random


adjectives = ['angry', 'funny', 'smart', 'brave', 'silly', 'happy', 'clever', 'fast', 'kind', 'gentle',
              'loud', 'quiet', 'shiny', 'wild', 'calm', 'proud', 'sweet', 'wise', 'young', 'old',
              'tiny', 'huge', 'curious', 'mysterious', 'spicy', 'cold', 'fierce', 'jolly', 'noisy', 'peaceful']

animals = ['cat', 'dog', 'rabbit', 'elephant', 'lion', 'tiger', 'bear', 'fox', 'deer', 'wolf',
           'horse', 'monkey', 'penguin', 'koala', 'zebra', 'giraffe', 'otter', 'panda', 'turtle', 'dolphin',
           'crocodile', 'frog', 'owl', 'sparrow', 'hawk', 'whale', 'shark', 'snail', 'bee', 'butterfly']

def create_username() -> str:
    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    number = random.randint(1000, 9999)
    return f"{adjective}_{animal}_{number}" if random.random() < 0.5 else f"{adjective.capitalize()}{animal.capitalize()}{number}"