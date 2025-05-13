import multiprocessing
import time
from GPS.Button import Button

def fonction1(q_out, q_arret):
    i = 0
    while q_arret.empty():
        q_out.put(f"IMU {i}")
        i+=1
        # q_out.put(None)  # signal de fin
        time.sleep(0.5)
    print("end 1")

def fonction2(q_out, q_arret):
    j = 0
    while q_arret.empty():
        q_out.put(f"GPS {j}")
        j+=1
        # q_out.put(None)  # signal de fin
        time.sleep(1)
    print("End 2")


if __name__ == '__main__':
    # Queues pour communication inter-processus
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    q_arret = multiprocessing.Queue()

    # Création des processus
    p1 = multiprocessing.Process(target=fonction1, args=(q1,q_arret,))
    p2 = multiprocessing.Process(target=fonction2, args=(q2,q_arret,))
    # Lancement 
    p1.start()
    p2.start()

    b = Button(17)
    def press():
        q_arret.put("bree")
    
    b.on_press(press)
    y = "GPS"
    u = "test"
    while q_arret.empty():
        if not q1.empty():
            u = q1.get()
        if not q2.empty():
            y = q2.get()
        print(u, y)
        print(f"--------------------\n")
        time.sleep(0.5)

    print("FIN")
