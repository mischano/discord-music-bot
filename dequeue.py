from collections import deque

max_len = 20
queue = deque([], maxlen=max_len)


def add_right(elem):
    queue.append(elem)


def add_left(elem):
    queue.appendleft(elem)


def pop_left():
    return queue.popleft()


def pop_right():
    return queue.pop()


def size():
    return len(queue)


def clear_all():
    queue.clear()


def insert(index, elem):
    queue.insert(index, elem)


def remove(value):
    queue.remove(value)


def shuffle():
    pass
