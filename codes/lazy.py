from pymongo import MongoClient
import threading
import time

MONGO_URI = "mongodb+srv://ahnafkhan414_db_user:nrq5G4bq75YxQMpk@cluster0.k3zfgbs.mongodb.net/?appName=Cluster0"
DB_NAME = "test_db"


class LazyMongo:
    _instance = None
    _lock = threading.Lock()  

    def __init__(self):
        if LazyMongo._instance is not None:
            raise Exception("Use get_instance()")
        print("Creating Lazy instance")
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    @staticmethod
    def get_instance():
       
        if LazyMongo._instance is None:
            LazyMongo._instance = LazyMongo()
        return LazyMongo._instance

    def get_database(self):
        return self.db

    def get_collection(self, name):
        return self.db[name]

    def close_connection(self):
        self.client.close()


# ================= TESTS =================

def instance_test(get_instance_fn, name):
    print(f"\n=== Instance Test: {name} ===")
    a = get_instance_fn()
    b = get_instance_fn()

    print("ID A:", id(a))
    print("ID B:", id(b))
    print("Same instance:", a is b)


def thread_test(get_instance_fn, name):
    print(f"\n=== Thread Test: {name} ===")


    LazyMongo._instance = None

    barrier = threading.Barrier(10)
    ids = []

    def worker():
        barrier.wait()
        inst = get_instance_fn()
        ids.append(id(inst))

    threads = [threading.Thread(target=worker) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Unique instances:", set(ids))
    print("Thread-safe?", len(set(ids)) == 1)


def performance_test(get_instance_fn, name):
    print(f"\n=== Performance Test: {name} ===")

   
    LazyMongo._instance = None
    start = time.perf_counter()
    get_instance_fn()
    init_time = (time.perf_counter() - start) * 1000

    
    start = time.perf_counter()
    for _ in range(100000):
        get_instance_fn()
    access_time = (time.perf_counter() - start) / 100000 * 1e6  # microseconds per call

    print(f"Init time (ms): {init_time:.4f}")
    print(f"Avg access time (µs): {access_time:.4f}")


if __name__ == "__main__":
    instance_test(LazyMongo.get_instance, "Lazy")
    thread_test(LazyMongo.get_instance, "Lazy")
    performance_test(LazyMongo.get_instance, "Lazy")