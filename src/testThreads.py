import multiprocessing
import time

def fonction1(q_out):
    i = 0
    while True:
        q_out.put(f"IMU {i}")
        i+=1
        # q_out.put(None)  # signal de fin
        time.sleep(0.1)

def fonction2(q_out):
    j = 0
    while True:
        q_out.put(f"GPS {j}")
        j+=1
        # q_out.put(None)  # signal de fin
        time.sleep(1)


if __name__ == '__main__':
    # Queues pour communication inter-processus
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()

    # Création des processus
    p1 = multiprocessing.Process(target=fonction1, args=(q1,))
    p2 = multiprocessing.Process(target=fonction2, args=(q2,))
    # Lancement
    p1.start()
    p2.start()
    y = "GPS"
    while True:
        u = q1.get()
        if not q2.empty():
            y = q2.get()
        print(u, y)
        print(f"--------------------\n")
        time.sleep(0.01)

    print("FIN")
