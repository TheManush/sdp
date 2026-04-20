import pymongo
import threading
import time

MONGO_URI = "mongodb+srv://ahnafkhan414_db_user:nrq5G4bq75YxQMpk@cluster0.k3zfgbs.mongodb.net/?appName=Cluster0"
DB_NAME = "test_db"



class SyncMongo:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):

        if SyncMongo._instance is not None:
            raise Exception("Use get_instance()")

        print("Creating Sync instance")
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    @staticmethod
    def get_instance():
        with SyncMongo._lock: 
            if SyncMongo._instance is None:
                SyncMongo._instance = SyncMongo()
        return SyncMongo._instance

    def get_database(self):
        return self.db

    def get_collection(self, name):
        return self.db[name]

    def close_connection(self):
        self.client.close()


# =========================
#            TEST
# =========================

def instance_test(singleton_class, name):
    print(f"\n{'='*50}")
    print(f"Instance Test: {name}")

    a = singleton_class.get_instance()
    b = singleton_class.get_instance()

    print("ID A:", id(a))
    print("ID B:", id(b))
    print("Same instance:", a is b)



def thread_test(singleton_class, name):
    print(f"\n{'='*50}")
    print(f"Thread Safety Test: {name}")

    SyncMongo._instance = None  

    barrier = threading.Barrier(10)
    results = []

    def worker():
        barrier.wait()
        inst = singleton_class.get_instance()
        results.append(id(inst))

    threads = [threading.Thread(target=worker) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Unique instances:", set(results))
    print("Thread-safe:", len(set(results)) == 1)



def performance_test(singleton_class, name):
    print(f"\n{'='*50}")
    print(f"Performance Test: {name}")

   
    SyncMongo._instance = None

    start = time.perf_counter()
    singleton_class.get_instance()
    init_time = (time.perf_counter() - start) * 1000

  
    start = time.perf_counter()
    for _ in range(100000):
        singleton_class.get_instance()
    access_time = (time.perf_counter() - start) / 100000 * 1e6

    print(f"Init time (ms): {init_time:.4f}")
    print(f"Avg access time (µs): {access_time:.4f}")



if __name__ == "__main__":
    instance_test(SyncMongo, "Synchronized")
    thread_test(SyncMongo, "Synchronized")
    performance_test(SyncMongo, "Synchronized")