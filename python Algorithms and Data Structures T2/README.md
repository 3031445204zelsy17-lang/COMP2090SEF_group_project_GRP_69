# Heap Sort Implementation

## Project Introduction
This project implements the classic **Heap Sort algorithm** in Python, using a Max-Heap structure to sort an array in ascending order. The code supports interactive input of numbers (integers/decimals), includes input validity verification, empty input handling, and other features to ensure robust operation.

## Algorithm Principles
The core idea of Heap Sort is to leverage the properties of a heap (the root node of a Max-Heap is the maximum value in the current heap) to complete sorting, which is mainly divided into two steps:
1. **Build a Max-Heap**: Convert an unordered array into a Max-Heap structure, where the value of each parent node is greater than or equal to its child nodes.
2. **Extract the Heap Top Element**: Swap the maximum value at the heap top to the end of the array one by one, then re-heapify the remaining elements to finally get an ascending array.

## Usage Instructions

### 1. Run the Code
Execute the Python script directly to start the interactive program:
```bash
python heap_sort.py
```

### 2. Input Description
- After the program starts, you will be prompted to enter numbers one by one (integers/decimals are both acceptable);
- Press **Enter (empty input)** to end the input process after completion;
- If non-numeric content is entered, the program will prompt "Invalid input" and require re-entry.

### 3. Output Description
- If no numbers are entered, output "No numbers entered!";
- If valid numbers are entered, the **original input array** and the **ascending array after Heap Sort** will be output.

## Code Explanation
The code is divided into three parts: core sorting functions, interactive input, and result output. The core functions are explained as follows:

### 1. `heapify(arr, heap_size, root_idx)`
- **Function**: Adjust the subtree rooted at `root_idx` to maintain the Max-Heap property;
- **Time Complexity**: O(log n) (n = number of elements in the heap, only traverses the height of the complete binary tree);
- **Logic**: Compare the root node, left child node, and right child node, find the maximum value and swap (if needed), and recursively adjust the affected subtree.

### 2. `build_max_heap(arr)`
- **Function**: Convert an unordered array into a Max-Heap;
- **Time Complexity**: O(n) (the total time for heapifying all non-leaf nodes is linear);
- **Logic**: Start from the last non-leaf node, traverse in reverse order and call `heapify` to adjust each subtree.

### 3. `heap_sort(arr)`
- **Function**: Complete ascending sorting of the array based on Max-Heap;
- **Time Complexity**: O(n log n) (heap building O(n) + n heapify operations O(log n));
- **Space Complexity**: O(1) (in-place sorting, no extra array space required);
- **Logic**: First build a Max-Heap, then swap the maximum value at the heap top to the end of the array one by one, and re-heapify the remaining heap.

## Complexity Analysis
| Metric         | Complexity   | Explanation                                                                 |
|----------------|--------------|-----------------------------------------------------------------------------|
| Time Complexity| O(n log n)   | Heap building O(n) + n heapify operations (O(log n) per operation)          |
| Space Complexity| O(1)        | In-place sorting, only constant-level extra space is used                   |
| Stability      | Unstable     | Swap operations during heapification may disrupt the relative order of equal elements |

## Running Examples
### Example 1: Normal Input
```
==================================================
Please enter numbers one by one, press ENTER to finish input
==================================================
Please enter a number: 5
Please enter a number: 2.8
Please enter a number: 9
Please enter a number: 1
Please enter a number: 

Original input array: [5.0, 2.8, 9.0, 1.0]
✅ Heap sorted result (Ascending order): [1.0, 2.8, 5.0, 9.0]
```

### Example 2: Invalid Input + Empty Input
```
==================================================
Please enter numbers one by one, press ENTER to finish input
==================================================
Please enter a number: abc
❌ Invalid input! Please enter a valid number.
Please enter a number: 7
Please enter a number: 

Original input array: [7.0]
✅ Heap sorted result (Ascending order): [7.0]
```

### Example 3: No Input
```
==================================================
Please enter numbers one by one, press ENTER to finish input
==================================================
Please enter a number: 

⚠️ No numbers entered!
```

## Notes
1. Only numbers (integers/decimals) are supported for input; non-numeric content will be judged as invalid input;
2. The sorting result is in **ascending order**. If descending order is needed, modify the swap logic of the `heap_sort` function or reverse the result;
3. A copy operation is performed on the input array in the code to avoid modifying the original input data during the sorting process;
4. Heap Sort is suitable for sorting large-scale data, with a stable time complexity of O(n log n) and no need for extra space.

## Extension Notes
- You can modify the comparison logic of the `heapify` function (change `>` to `<`) to build a Min-Heap for descending order sorting;
- You can extend the batch input function (e.g., read a list of numbers from a file);
- A performance testing module can be added to compare the sorting time consumption under different data volumes.
