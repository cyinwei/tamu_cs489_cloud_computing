"""
Backend functions for the AggieFit message board.
"""
import time
import threading

def read(mongodb_client, channel):
    """
    Reads the entire history of the topic.   We let the topic the collection,
    with the posts being the documents.

    Learning resources:
    http://api.mongodb.com/python/current/tutorial.html

    NOTE: Expects mongodb_client to be the database containing collections that
    correspond to the message board topics.
    """

    if channel is False:
        return 'Error: no topic selected.'

    topic = mongodb_client[channel]
    messages = topic.find()

    msg_list = []
    for msg in messages:
        msg_list.append(msg['msg'])

    messages.close()
    return '\n'.join(msg_list)


def write(mongodb_client, redis_client, channel, msg):
    """
    Implements the write operation for the AggieFit message board.

    write() writes the message to both MongoDB and Redis.  MongoDB handles read()
    while Redis handles listen(), the two message consuming features of our
    message board.

    Learning resources:
    https://docs.mongodb.com/v3.2/core/databases-and-collections/
    http://api.mongodb.com/python/current/tutorial.html

    NOTE: We choose the mongo collection name and the redis publish key to be
    the same (channel).

    NOTE: Expects mongodb_client to be the database containing collections that
    correspond to the message board topics.
    """

    if channel is False:
        return 'Error: we needed a selected topic to write to.'

    mongodb_topic = mongodb_client[channel]
    mongodb_topic.insert_one({'msg': msg})

    redis_client.publish(channel, msg)

def _listen_handler(message):
    """
    Redis PubSub handler.  Takes in a incoming subscription message, formats
    it, and prints it to the screen.
    """
    print_str = "(listen) => {}"
    print(print_str.format(message['data'].decode('utf-8')))
    # we write in utf 8 by default in python

def listen(redis_pubsub, channel, stop_word='quit'):
    """
    A **non-blocking** listen() that uses redis to subscribe to a message board
    (channel).  Requires the caller to stop listening by closing the thread.
    Also requires the caller to clean up.

    Learning resources:
    Docs (on redis):
    https://github.com/andymccurdy/redis-py
    https://docs.python.org/3/library/threading.html
    https://making.pusher.com/redis-pubsub-under-the-hood/

    Guides (on how to set up redis-py, how to use the pubsub):
    https://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/
    http://programeveryday.com/post/create-a-simple-chat-room-with-redis-pubsub/
    https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python
    https://ravi.pckl.me/short/non-blocking-pubsub-in-python-and-redis/
    https://gist.github.com/jobliz/2596594

    """
    if channel is False:
        return

    redis_pubsub.subscribe(**{channel: _listen_handler})

    thread = redis_pubsub.run_in_thread(sleep_time=0.001)
    return thread
