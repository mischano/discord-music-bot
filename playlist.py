from collections import deque
from random import shuffle

max_len = 100
queue = deque([], maxlen=max_len)


def add_right(elem):
    queue.append(elem)


def add_left(elem):
    queue.appendleft(elem)


def pop_right():
    return queue.pop()


def pop_left():
    return queue.popleft()


def insert(index, elem):
    queue.insert(index, elem)

def remove(elem):
    try:
        # print(queue[elem])
        # deque.remove(elem)
        del queue[elem]
    except IndexError:
        return False
    else:
        return True

def size():
    return len(queue)


def is_empty():
    return True if len(queue) == 0 else False


def get_all():
    res = '\n'.join(f'{idx}. ' + i['title'] for idx, i in enumerate(queue, start=1))
    return res

def shuffle_all():
    shuffle(queue)

def clear_all():
    queue.clear()

