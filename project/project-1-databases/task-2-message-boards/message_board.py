"""
Implements the prototype for the AggieFit messsage board.
"""

import signal
import sys

from pymongo import MongoClient
import redis

from lib import read, write, listen
from config import redis_config, mongo_config, mongo_db_name

# global objects so our handler can close them
# NOTE: redis-py and pymongo's connections disconnect as they go out of scope
listener_thread = None

def sigint_handler(signal, frame):
    global listener_thread
    if listener_thread is None:
        sys.exit(0)
    print('\nCleaning up listener thread... ')
    listener_thread.stop()
    listener_thread.join()
    print('Done. Bye!')
    sys.exit(0)

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
    global listener_thread
    topic = None
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
            if not topic:
                print('Error: Need a selected topic to read from.')
            else:
                print(read(mongo_db, topic))
        elif input_str == 'listen':
            if not topic:
                print('Error: Need a selected topic to listen to.')
            elif listener_thread is not None:
                print('Error: Already listening to this topic.')
            else:
                listener_thread = listen(redis_pubsub, topic)
                print("Type \'quit\' to stop listening.")
        elif input_str == 'write':
            print('Error: Needs a message (like \'write: hi\')')
        elif input_str == 'select':
            print('Error: Needs a topic name (like \'select: test\')')
        elif input_str[:7] == 'select ':
            if listener_thread is not None:
                # if we have a listener thread, then we already have a topic
                # we need to close the listener, since only one listener is allowed
                print("Currently listening on topic {}, exit listener before switching.".format(topic))
            else:
                topic = input_str[7:].strip()
                prompt = "({}) > ".format(topic)
        elif input_str[:6] == 'write ':
            if not topic:
                print('Need a selected topic to write to.')
            else:
                write(mongo_db, redis_client, topic, input_str[6:].strip())
                print('[written]')

        # loop again
        input_str = input(prompt)
        input_str = input_str.strip()

    # cleanup
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
    print('Done\n')

    # initial help menu
    print(help_str)

    # our shell, where we loop forever until the quit command
    loop_sh(mongo_db, redis_client)

    # clean up
    mongo_client.close()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    main()

