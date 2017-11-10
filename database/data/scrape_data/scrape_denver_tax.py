from Queue import Queue
from threading import Thread
import json

from denver_tax_scraper import denverTax

def get_pins():
    with open('remaining_pins.csv', 'r') as f:
        # pins = [_.strip('\n') for _ in f.readlines()]
        pins = f.readlines()[0].split(',')
    return sorted(pins)

def scrapper_worker(q):
    while not q.empty():
        print '\n{} pins remaining in queue'.format(q.qsize())
        pin = q.get()
        tax_scraper = denverTax(pin)
        q.task_done()

pins = get_pins()
q = Queue()
map(q.put, pins)

for i in range(20):
    t = Thread(target=scrapper_worker, args=(q, ))
    t.start()

q.join()
