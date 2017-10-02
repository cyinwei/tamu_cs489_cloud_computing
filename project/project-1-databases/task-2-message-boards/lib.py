"""
Backend functions for the AggieFit message board.
"""
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
    for msg in messages:
        print(msg)
    return list(messages)


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

class Listener(threading.Thread):
    """
    A stoppable listener thread that relies on redis's pubsub feature.

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

    def __init__(self, redis_db, channel):
        """
        Contructs the thread, making it stoppable with an event and also
        connects to redis as a subscriber to the channel.
        """
        # allow the thread to stop itself with an threading.Event()
        super(Listener, self).__init__()
        self.shutdown_flag = threading.Event()

        # subscribe to the redis channel
        self.channel = channel
        self.redis = redis_db
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channel)

    def listen(self):
        """
        Uses redis's pubsub to print new data.
        """
        for item in self.pubsub.listen():
            line = "listen[{}]: {}"
            print(line.format(self.channel, item))

    def run(self):
        while not self.shutdown_flag.is_set():
            self.listen()

        self.pubsub.unsubscribe()

def listen(redis_db, channel, quit_str='quit'):
    """
    A **blocking** listen() that uses redis to subscribe to a message board
    (channel).

    See the resource links from the Listener class for my learning sources.
    """
    listener = Listener(redis_db, channel)
    listener.start()

    input_str = input("Type {} to stop listening.".format(quit_str))
    if input_str == quit_str:
        listener.shutdown_flag.set()
        listener.join()
