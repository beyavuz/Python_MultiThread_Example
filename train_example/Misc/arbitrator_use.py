import threading
import time

controller = threading.Condition()


def requested_intersections_free(intersections_to_lock):
    for it in intersections_to_lock:
        if it.locked_by > -1:  # if locked by another train
            return False
    return True


def lock_intersections_in_distance_arbitrator(train_uid, reverse_start, reserve_end, crossings, mutex_condition):
    intersections_to_lock = []
    for crossing in crossings:
        if reserve_end >= crossing.position >= reverse_start and crossing.intersection.locked_by != train_uid:
            intersections_to_lock.append(crossing.intersection)

    mutex_condition.acquire()
    while not requested_intersections_free(intersections_to_lock):
        mutex_condition.wait()

    for intersection in intersections_to_lock:
        intersection.locked_by = train_uid  # marking the intersections as "not free"
        time.sleep(0.01)

    mutex_condition.release()


def move_train_arbitrator(train, distance, crossings, mutex_condition):
    while train.front < distance:
        train.front += 1
        for crossing in crossings:
            if train.front == crossing.position:
                print(f"Train:{train.uid}  , intersection:{crossing.intersection.uid}")
                lock_intersections_in_distance_arbitrator(train.uid, crossing.position,
                                                          crossing.position + train.train_length,
                                                          crossings, mutex_condition)
            back = train.front - train.train_length
            if back == crossing.position:
                controller.acquire()
                crossing.intersection.locked_by = -1
                controller.notify_all()
                controller.release()
        time.sleep(0.01)
