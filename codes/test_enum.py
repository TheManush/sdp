import pymongo
import threading
import time
from enum import Enum

class MongoDBConnection:
    def __init__(self):
        self._client = pymongo.MongoClient(
            "mongodb+srv://ahnafkhan414_db_user:nrq5G4bq75YxQMpk@cluster0.k3zfgbs.mongodb.net/?appName=Cluster0"
        )

    def get_database(self, db_name="testdb"):
        return self._client[db_name]

    def get_collection(self, db_name, col_name):
        return self._client[db_name][col_name]

    def close_connection(self):
        self._client.close()


class EnumSingletonMongoDB(Enum):
    INSTANCE = MongoDBConnection()


# ================= TESTS =================


def instance_test():
    print("\n=== Instance Test ===")

    a = EnumSingletonMongoDB.INSTANCE.value
    b = EnumSingletonMongoDB.INSTANCE.value

    print("ID A:", id(a))
    print("ID B:", id(b))
    print("Same:", a is b)

def thread_test():
    print("\n=== Thread Test ===")

    results = []
    barrier = threading.Barrier(10)

    def worker():
        barrier.wait()
        results.append(id(EnumSingletonMongoDB.INSTANCE.value))

    threads = [threading.Thread(target=worker) for _ in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Unique instances:", set(results))
    print("Thread-safe:", len(set(results)) == 1)


def performance_test():
    print("\n=== Performance Test ===")

    start = time.perf_counter()
    _ = EnumSingletonMongoDB.INSTANCE.value
    init_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    for _ in range(100000):
        _ = EnumSingletonMongoDB.INSTANCE.value
    access_time = (time.perf_counter() - start) / 100000 * 1e6

    print(f"Init time (ms): {init_time:.4f}")
    print(f"Avg access (µs): {access_time:.4f}")

if __name__ == "__main__":
    instance_test()
    thread_test()
    performance_test()