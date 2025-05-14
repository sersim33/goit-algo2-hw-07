import time
import random
import builtins
from collections import OrderedDict

# === Функції ===

def range_sum_no_cache(array, L, R):
    return builtins.sum(array[L:R + 1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, L, R, cache):
    key = (L, R)
    result = cache.get(key)
    if result != -1:
        return result
    result = builtins.sum(array[L:R + 1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value, cache):
    array[index] = value
    cache.invalidate_keys(lambda k: isinstance(k, tuple) and k[0] <= index <= k[1])

# === Реалізація LRU Cache ===

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate_keys(self, condition_fn):
        keys_to_delete = [k for k in self.cache if condition_fn(k)]
        for k in keys_to_delete:
            del self.cache[k]

# === Генерація даних ===

# N = 100_000
# Q = 50_000
# arr = [random.randint(1, 100) for _ in range(N)]
# queries = []

# for _ in range(Q):
#     if random.random() < 0.5:
#         L = random.randint(0, N - 2)
#         R = random.randint(L, N - 1)
#         queries.append(('Range', L, R))
#     else:
#         index = random.randint(0, N - 1)
#         value = random.randint(1, 100)
#         queries.append(('Update', index, value))



N = 100_000
Q = 50_000
arr = [random.randint(1, 100) for _ in range(N)]

# Частина запитів, які будуть повторюватися
repeated_ranges = [(random.randint(0, N-1000), random.randint(0, N-1)) for _ in range(100)]
repeated_ranges = [(min(l, r), max(l, r)) for l, r in repeated_ranges]

queries = []
for _ in range(Q):
    if random.random() < 0.7:
        # 70% Range-запитів
        if random.random() < 0.3:
            # 30% з них будуть повторювані
            L, R = random.choice(repeated_ranges)
        else:
            L = random.randint(0, N - 1)
            R = random.randint(0, N - 1)
            L, R = min(L, R), max(L, R)
        queries.append(('Range', L, R))
    else:
        # 30% Update-запитів
        index = random.randint(0, N - 1)
        value = random.randint(1, 100)
        queries.append(('Update', index, value))


# === Вимірювання часу ===

# Без кешу
arr_no_cache = arr.copy()
range_no_cache_time = 0
update_no_cache_time = 0

for q in queries:
    if q[0] == 'Range':
        _, L, R = q
        start = time.time()
        range_sum_no_cache(arr_no_cache, L, R)
        range_no_cache_time += time.time() - start
    else:
        _, index, value = q
        start = time.time()
        update_no_cache(arr_no_cache, index, value)
        update_no_cache_time += time.time() - start

# З кешем
arr_with_cache = arr.copy()
cache = LRUCache(1000)
range_with_cache_time = 0
update_with_cache_time = 0

for q in queries:
    if q[0] == 'Range':
        _, L, R = q
        start = time.time()
        range_sum_with_cache(arr_with_cache, L, R, cache)
        range_with_cache_time += time.time() - start
    else:
        _, index, value = q
        start = time.time()
        update_with_cache(arr_with_cache, index, value, cache)
        update_with_cache_time += time.time() - start

# === Результати ===

print(f"[виконання без кешування] Час Range: {range_no_cache_time:.4f} сек")
print(f"[виконання без кешування] Час Update: {update_no_cache_time:.4f} сек")
print(f"[З LRU-кешем] Час Range: {range_with_cache_time:.4f} сек")
print(f"[З LRU-кешем] Час Update: {update_with_cache_time:.4f} сек")
