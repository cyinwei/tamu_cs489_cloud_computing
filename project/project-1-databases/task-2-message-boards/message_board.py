"""
Implements the prototype for the AggieFit messsage board.
"""

import signal

from pymongo import MongoClient
import redis

from lib import read, write, listen

redis_config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

mongo_config = ('localhost', 27017)
mongo_db_name = 'message_board_721008432'

help_str = ("AggieFit message board commands:\n"
            "help:            show this message\n"
            "quit:            exit the message board\n"
            "select <topic>:  pick the topic on the forum\n"
            "read:            get all the messages from the selected topic\n"
            "write <message>: write a single message to the selected topic\n"
            "listen:          listen to the selected topic\n")

def main():
    """
    main() function that executes message_board.py.
    """

    # connect to mongo, redis
    print('Welcome to the AggieFit message boards! (implemented by Charlie!)')
    print('Connecting to databases ... ')
    mongo_client = MongoClient(*mongo_config)
    mongo_db = mongo_client[mongo_db_name]
    redis_client = redis.StrictRedis(**redis_config)
    print('Done')
    print()
    print(help_str)

    topic = None
    prompt = "> "
    input_str = input(prompt)
    quit_inputs = ('q', 'quit', 'exit')
    while input_str not in quit_inputs:
        input_tokens = input_str.split()
        if len(input_tokens) == 1:
            if input_tokens[0] == 'read':
                read_str = read(mongo_db, topic)
            elif input_tokens[0] == 'listen':
                listen(redis_client, topic)
        elif len(input_tokens) == 2:
            if input_tokens[0] == 'select':
                topic = input_tokens[1]
                prompt = "({}) > ".format(topic)
            elif input_tokens[0] == 'write':
                write(mongo_db, redis_client, topic, input_tokens[1])

        input_str = input(prompt) # loop again

if __name__ == "__main__":
    main()
