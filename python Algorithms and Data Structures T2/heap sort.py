def heapify(arr, heap_size, root_idx):
    """
    Heapify Function: Adjust the subtree rooted at root_idx to maintain max-heap property
    Time Complexity: O(log n) (n = number of elements in heap, only traverses the height of the complete binary tree)
    """
    largest = root_idx  # Initialize largest element as root
    left_child = 2 * root_idx + 1  # Index of left child (complete binary tree formula)
    right_child = 2 * root_idx + 2  # Index of right child

    # Find the largest value among root, left child, and right child
    if left_child < heap_size and arr[left_child] > arr[largest]:
        largest = left_child
    if right_child < heap_size and arr[right_child] > arr[largest]:
        largest = right_child

    # If largest element is not root, swap and recursively heapify the affected subtree
    if largest != root_idx:
        arr[root_idx], arr[largest] = arr[largest], arr[root_idx]
        heapify(arr, heap_size, largest)

def build_max_heap(arr):
    """
    Build Max-Heap: Convert an unsorted array into a max-heap structure
    Time Complexity: O(n) (Total time for heapifying all non-leaf nodes is linear)
    """
    n = len(arr)
    last_non_leaf = n // 2 - 1  # Index of the last non-leaf node
    # Traverse all non-leaf nodes in reverse order and heapify each
    for i in range(last_non_leaf, -1, -1):
        heapify(arr, n, i)

def heap_sort(arr):
    """
    Heap Sort (Ascending Order): Implemented based on max-heap
    Overall Time Complexity: O(n log n) (Heap building O(n) + n heapify operations O(log n))
    Space Complexity: O(1) (In-place sorting, no extra array space needed)
    """
    n = len(arr)
    # Step 1: Build max-heap from input array - O(n)
    build_max_heap(arr)
    
    # Step 2: Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Swap root (max element) with the last element of current heap
        arr[i], arr[0] = arr[0], arr[i]
        # Heapify the reduced heap (heap size = i) - O(log n) per operation
        heapify(arr, i, 0)
    
    return arr

# ==================== Interactive Number Input ====================
print("=" * 50)
print("Please enter numbers one by one, press ENTER to finish input")
print("=" * 50)

number_list = []  # Store user-input numbers
while True:
    user_input = input("Please enter a number: ")
    # Empty input = end input process
    if user_input == "":
        break
    # Exception handling: Only valid numbers (integers/decimals) allowed
    try:
        num = float(user_input)
        number_list.append(num)
    except ValueError:
        print("❌ Invalid input! Please enter a valid number.")

# ==================== Heap Sort & Result Output ====================
if not number_list:
    print("\n⚠️ No numbers entered!")
else:
    print(f"\nOriginal input array: {number_list}")
    array_copy = number_list.copy()  # Copy array to avoid modifying original data
    sorted_array = heap_sort(array_copy)
    print(f"✅ Heap sorted result (Ascending order): {sorted_array}")
    
