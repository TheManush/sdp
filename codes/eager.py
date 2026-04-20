from pymongo import MongoClient
import threading
import time

MONGO_URI = "mongodb+srv://ahnafkhan414_db_user:nrq5G4bq75YxQMpk@cluster0.k3zfgbs.mongodb.net/?appName=Cluster0"
DB_NAME = "test_db"

class EagerMongo:
    _instance = None

    def __init__(self):
        if EagerMongo._instance is not None:
            raise Exception("Use get_instance()")
        print("Creating Eager instance")
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    @staticmethod
    def get_instance():
        return EagerMongo._instance

    def get_database(self):
        return self.db

    def get_collection(self, name):
        return self.db[name]

    def close_connection(self):
        self.client.close()

# create at load time
EagerMongo._instance = EagerMongo()

# ================= TESTS =================

def instance_test():
    print("\nInstance Test")
    a = EagerMongo.get_instance()
    b = EagerMongo.get_instance()
    print("ID A:", id(a))
    print("ID B:", id(b))
    print("Same instance:", a is b)

def thread_test():
    print("\nThread Test")
    barrier = threading.Barrier(10)
    ids = []

    def worker():
        barrier.wait()
        ids.append(id(EagerMongo.get_instance()))

    threads = [threading.Thread(target=worker) for _ in range(10)]
    [t.start() for t in threads]
    [t.join() for t in threads]

    print("Unique instances:", len(set(ids)))


def performance_test():
    print("\n=== Performance Test: Eager ===")

    # Init time (already created, so simulate access)
    start = time.perf_counter()
    _ = EagerMongo.get_instance()
    init_time = (time.perf_counter() - start) * 1000

    # Access time
    start = time.perf_counter()
    for _ in range(100000):
        _ = EagerMongo.get_instance()
    access_time = (time.perf_counter() - start) / 100000 * 1e6

    print(f"Init time (ms): {init_time:.4f}")
    print(f"Avg access (µs): {access_time:.4f}")

if __name__ == "__main__":
    instance_test()
    thread_test()
    performance_test()