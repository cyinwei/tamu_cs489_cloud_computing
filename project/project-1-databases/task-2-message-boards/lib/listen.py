"""
Implements the listen feature for the prototype of AggieFit message boards.
"""

import threading

class Listener(threading.Thread):
    """
    A stoppable listener thread that relies on redis's pubsub feature.
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
    Starts and runs Listener and exits via the quit string.
    """
    listener = Listener(redis_db, channel)
    listener.start()

    input_str = input("Type {} to stop listening.".format(quit_str))
    if input_str == quit_str:
        listener.shutdown_flag.set()
        listener.join()
