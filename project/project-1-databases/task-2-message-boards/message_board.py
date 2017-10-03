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
            "quit:            exit the message board (q, exit also work)\n"
            "select <topic>:  pick the topic on the forum\n"
            "read:            get all the messages from the selected topic\n"
            "write <message>: write a single message to the selected topic\n"
            "listen:          listen to the selected topic (one max)\n")

def loop_sh(mongo_db, redis_client, stop_words=('q', 'quit', 'exit')):
    """
    The shell of the AggieFit message board.  Loops until we quit.
    """

    topic = None
    listener_thread = None
    redis_pubsub = redis_client.pubsub()

    prompt = "> "
    input_str = input(prompt)
    input_str = input_str.strip()
    quit_inputs = ('q', 'quit', 'exit')
    while (input_str not in quit_inputs) or (listener_thread is not None):

        # check if we need to close our listener
        if input_str in quit_inputs:
            # that means we have an active listener_thread
            if not listener_thread:
                print('In loop_sh(): Unknown error, should never happen.')

            listener_thread.stop()
            listener_thread.join()
            listener_thread = None

            print("Stopped listening to topic [{}]".format(topic))

        # parse our input for commands
        if input_str == 'help':
            print(help_str)
        elif input_str == 'read':
            print(read(mongo_db, topic))
        elif input_str == 'listen':
            listener_thread = listen(redis_pubsub, topic)
            print("Type \'quit\' to stop listening.")
        elif input_str[:7] == 'select ':
            if listener_thread is not None:
                # if we have a listener thread, then we already have a topic
                # we need to close the listener, since only one listener is allowed
                print("Currently listening on topic {}, exit listener before switching.".format(topic))
            else:
                topic = input_str[7:].strip()
                prompt = "({}) > ".format(topic)
        elif input_str[:6] == 'write ':
            write(mongo_db, redis_client, topic, input_str[6:].strip())
            print('Written.')

        # loop again
        input_str = input(prompt)
        input_str = input_str.strip()

    redis_pubsub.unsubscribe()
    redis_pubsub.close()
    return

def main():
    """
    main() function that executes message_board.py.
    """
    print('Welcome to the AggieFit message boards! (implemented by Charlie!)')

    # connect to mongo, redis
    print('Connecting to databases (MongoDB, Redis) ... ')
    mongo_client = MongoClient(*mongo_config)
    mongo_db = mongo_client[mongo_db_name]
    redis_client = redis.StrictRedis(**redis_config)
    print('Done')
    print()
    print(help_str)

    loop_sh(mongo_db, redis_client)
    mongo_client.close()

if __name__ == "__main__":
    main()
