import pymongo
import threading
import time

MONGO_URI = "mongodb+srv://ahnafkhan414_db_user:nrq5G4bq75YxQMpk@cluster0.k3zfgbs.mongodb.net/?appName=Cluster0"
DB_NAME = "test_db"



class DCLMongo:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if DCLMongo._instance is not None:
            raise Exception("Use get_instance()")

        print("Creating DCL instance")
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    @staticmethod
    def get_instance():
   
        if DCLMongo._instance is None:
            with DCLMongo._lock:
               
                if DCLMongo._instance is None:
                    DCLMongo._instance = DCLMongo()
        return DCLMongo._instance

    def get_database(self):
        return self.db

    def get_collection(self, name):
        return self.db[name]

    def close_connection(self):
        self.client.close()



# ================= TESTS =================


def instance_test():
    print("\n=== Instance Test ===")

    a = DCLMongo.get_instance()
    b = DCLMongo.get_instance()

    print("ID A:", id(a))
    print("ID B:", id(b))
    print("Same instance:", a is b)



def thread_test():
    print("\n=== Thread Test ===")

    DCLMongo._instance = None  

    barrier = threading.Barrier(10)
    results = []

    def worker():
        barrier.wait()
        inst = DCLMongo.get_instance()
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

    DCLMongo._instance = None

    start = time.perf_counter()
    DCLMongo.get_instance()
    init_time = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    for _ in range(100000):
        DCLMongo.get_instance()
    access_time = (time.perf_counter() - start) / 100000 * 1e6

    print(f"Init time (ms): {init_time:.4f}")
    print(f"Avg access time (µs): {access_time:.4f}")


if __name__ == "__main__":
    instance_test()
    thread_test()
    performance_test()