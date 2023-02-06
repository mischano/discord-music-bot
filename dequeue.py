from collections import deque

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


def remove(value):
    queue.remove(value)


def size():
    return len(queue)


def is_empty():
    return True if len(queue) == 0 else False


def get_all():
    res = '\n'.join(f'{idx+1}. ' + i['title'] for idx, i in enumerate(queue))
    return res


def clear_all():
    queue.clear()


def shuffle():
    pass
