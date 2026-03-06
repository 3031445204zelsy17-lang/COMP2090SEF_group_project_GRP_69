# Task 2: Heap Data Structure and Heap Sort Algorithm

## Project Information
- Course: COMP2090SEF 
- Data Structure: **Heap**
- Algorithm: **Heap Sort**

## Rationale
Course covered: Stack, Queue, Linked List, Binary Search Tree, Bubble/Selection/Merge/Pigeonhole Sort. This project selects Heap and Heap Sort which are not covered. BST is for searching while Heap is for max/min retrieval. Merge Sort needs O(n) space but Heap Sort uses O(1) in-place.

## File Description
| File | Content |
|------|---------|
| `heap.py` | Heap data structure implementation + interactive test code |

## How to Run
Run `python heap.py` then enter numbers in terminal, type `q` to finish:
Please enter numbers, type 'q' to finish
50
Current heap: [50]
30
Current heap: [50, 30]
80
Current heap: [80, 50, 30]
q
Final heap: [80, 50, 30]
Sorted result: [30, 50, 80]
plain



## Core Implementation
**Heap Definition**: A complete binary tree implemented with array, satisfying parent ≥ children (Max Heap).

**ADT Operations**:
- `insert(item)`: Insert element, O(log n)
- `extract_max()`: Remove and return maximum, O(log n)
- `size()`: Get heap size, O(1)

**Key Implementation**: Parent-child relationship via index calculation: Parent `(i - 1) // 2`, Left child `2 * i + 1`, Right child `2 * i + 2`. Sift up maintains heap property when inserting. Sift down maintains heap property after extracting max.

**Heap Sort Steps**: (1) Build heap by inserting n elements, O(n log n). (2) Perform n extract_max operations to get descending order, O(n log n). (3) Reverse to get ascending order, O(n).

**Complexity**: Time O(n log n), Space O(n). Best/worst case always O(n log n), better than Quick Sort's O(n²) worst case.

## Code Structure
`heap.py` contains class MaxHeap with `__init__()`, `_parent(i)`, `_left_child(i)`, `_right_child(i)`, `insert(item)`, `_sift_up(i)`, `extract_max()`, `_sift_down(i)`, `size()`. Test code creates calng heap, uses while loop for input, displays current heap, and outputs sorted result.

## Usage Example
```python
from heap import MaxHeap
calng = MaxHeap()
calng.insert(50)
calng.insert(30)
calng.insert(80)
print(calng.heap)      # [80, 30, 50]
max_val = calng.extract_max()  # Returns 80
sorted_result = []
while calng.size() > 0:
    sorted_result.append(calng.extract_max())
print(sorted_result[::-1])  # [30, 50, 80] ascending
Pre-submission Status

[x] Complete heap data structure (MaxHeap class)
[x] Core operations: insert, extract_max, size
[x] Heap sort algorithm implemented
[x] Interactive test code
[x] Time/space complexity analysis
[ ] Final report PDF (due April 12)
Comparison: BST vs Heap




Feature	BST	Heap
Primary Use	Search any value	Quick max/min retrieval
Ordering	Left < Root < Right	Parent ≥ Children
Find maximum	O(n)	O(1)
Insert/Delete	O(log n) ~ O(n)	O(log n)
Tree shape	Arbitrary	Complete binary tree
References

Course Notes Week 3: Binary Search Tree
Introduction to Algorithms (CLRS) Chapter 6: Heap Sort
GeeksforGeeks: Heap Data Structure
plain