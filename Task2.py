import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# Fibonacci with LRU Cache
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

# Splay Tree Node
class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

# Splay Tree
class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root

            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left is not None else root
        else:
            if root.right is None:
                return root

            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)

            return self._rotate_left(root) if root.right is not None else root

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            return

        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def search(self, key):
        if self.root is None:
            return None
        self.root = self._splay(self.root, key)

        return self.root.value if self.root.key == key else None

# Fibonacci with Splay Tree
def fibonacci_splay(n, tree):
    if n < 2:
        return n

    fib_n_minus_1 = tree.search(n-1)
    if fib_n_minus_1 is None:
        fib_n_minus_1 = fibonacci_splay(n-1, tree)
        tree.insert(n-1, fib_n_minus_1)

    fib_n_minus_2 = tree.search(n-2)
    if fib_n_minus_2 is None:
        fib_n_minus_2 = fibonacci_splay(n-2, tree)
        tree.insert(n-2, fib_n_minus_2)

    return fib_n_minus_1 + fib_n_minus_2

# Measure execution time for both approaches
n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in n_values:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10.0
    lru_times.append(lru_time)

    splay_tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=10) / 10.0
    splay_times.append(splay_time)

# Plot the results
plt.plot(n_values, lru_times, label='LRU Cache')
plt.plot(n_values, splay_times, label='Splay Tree')
plt.xlabel('Fibonacci Number (n)')
plt.ylabel('Average Execution Time (seconds)')
plt.legend()
plt.title('Fibonacci Calculation: LRU Cache vs Splay Tree')
plt.show()

# Print the results in a table format

print(f"{'n':<15}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
for i in range(len(n_values)):
    print(f"{n_values[i]:<15}{lru_times[i]:<25}{splay_times[i]:<25}")
