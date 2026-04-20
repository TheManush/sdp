import pymongo
import threading
import time

MONGO_URI = "mongodb+srv://ahnafkhan414_db_user:nrq5G4bq75YxQMpk@cluster0.k3zfgbs.mongodb.net/?appName=Cluster0"
DB_NAME = "testdb"


class BillPughMongo:

    class _Holder:
        instance = None

    _lock = threading.Lock()

    def __init__(self):
        if BillPughMongo._Holder.instance is not None:
            raise Exception("Use get_instance()")

        print("Creating Bill Pugh instance")
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    @staticmethod
    def get_instance():
        # first check (fast)
        if BillPughMongo._Holder.instance is None:
            with BillPughMongo._lock:
                # second check (safe)
                if BillPughMongo._Holder.instance is None:
                    BillPughMongo._Holder.instance = BillPughMongo()
        return BillPughMongo._Holder.instance

    def get_database(self):
        return self.db

    def get_collection(self, name):
        return self.db[name]

    def close_connection(self):
        self.client.close()

# ================= TESTS =================


def instance_test():
    print("\n=== Instance Test ===")

    a = BillPughMongo.get_instance()
    b = BillPughMongo.get_instance()

    print("ID A:", id(a))
    print("ID B:", id(b))
    print("Same:", a is b)


def thread_test():
    print("\n=== Thread Test ===")

    BillPughMongo._Holder.instance = None

    barrier = threading.Barrier(10)
    results = []

    def worker():
        barrier.wait()
        inst = BillPughMongo.get_instance()
        results.append(id(inst))

    threads = [threading.Thread(target=worker) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Unique instances:", set(results))
    print("Thread-safe:", len(set(results)) == 1)


def performance_test():
    print("\n=== Performance Test ===")

    BillPughMongo._Holder.instance = None

    start = time.perf_counter()
    BillPughMongo.get_instance()
    init_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    for _ in range(100000):
        BillPughMongo.get_instance()
    access_time = (time.perf_counter() - start) / 100000 * 1e6

    print(f"Init time (ms): {init_time:.4f}")
    print(f"Avg access (µs): {access_time:.4f}")


if __name__ == "__main__":
    instance_test()
    thread_test()
    performance_test()
