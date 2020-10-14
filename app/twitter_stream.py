import tweepy
import threading
import time

#the buffer is the number of seconds between each update
def twitter_stream(buffer):
    buffer_point = buffer
    start_time = time.time()
    
    while True:
        elapsed_time = time.time() - start_time
        start_time = time.time()
        buffer_point -= elapsed_time
        if buffer_point<=0:
            buffer_point=buffer
            #twitter stream update goes under here
            

#main thread
if __name__ == "__main__":
    #the buffer argument should be in the args() parameter
    streamThread = threading.Thread(target=twitter_stream, args=(int(1),))
    streamThread.start()


