import time

# used in hierarchy
def lock_intersections_in_distance(train_uid, reverse_start, reserve_end, crossings):
    intersections_to_lock = []
    for crossing in crossings:
        if reserve_end >= crossing.position >= reverse_start and crossing.intersection.locked_by != train_uid:
            intersections_to_lock.append(crossing.intersection)

    intersections_to_lock = sorted(intersections_to_lock, key=lambda it: it.uid)

    for intersection in intersections_to_lock:
        intersection.mutex.acquire()
        intersection.locked_by = train_uid
        time.sleep(0.01)


# using hierarchy to solve deadlock
def move_train_hierarchy(train, distance, crossings):
    while train.front < distance:
        train.front += 1
        for crossing in crossings:
            if train.front == crossing.position:
                print(f"Train:{train.uid}  , intersection:{crossing.intersection.uid}")
                lock_intersections_in_distance(train.uid, crossing.position, crossing.position + train.train_length,
                                               crossings)
            back = train.front - train.train_length
            if back == crossing.position:
                crossing.intersection.locked_by = -1
                crossing.intersection.mutex.release()
        time.sleep(0.01)