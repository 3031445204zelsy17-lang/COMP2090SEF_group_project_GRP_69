class MaxHeap:
    def __init__(self):
        self.heap = []
    
    def _parent(self, i):
        return (i - 1) // 2
    
    def _left_child(self, i):
        return 2 * i + 1
    
    def _right_child(self, i):
        return 2 * i + 2
    
    def insert(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)
    
    def _sift_up(self, i):
        while i > 0 and self.heap[i] > self.heap[self._parent(i)]:
            self.heap[i], self.heap[self._parent(i)] = self.heap[self._parent(i)], self.heap[i]
            i = self._parent(i)
    
    def extract_max(self):
        if not self.heap:
            return None
        
        max_val = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        if self.heap:
            self._sift_down(0)
        
        return max_val
    
    def _sift_down(self, i):
        max_index = i
        left = self._left_child(i)
        right = self._right_child(i)
        
        if left < len(self.heap) and self.heap[left] > self.heap[max_index]:
            max_index = left
        
        if right < len(self.heap) and self.heap[right] > self.heap[max_index]:
            max_index = right
        
        if i != max_index:
            self.heap[i], self.heap[max_index] = self.heap[max_index], self.heap[i]
            self._sift_down(max_index)
    
    def size(self):
        return len(self.heap)
    
    
    
from heap import MaxHeap


calng = MaxHeap()

print("请输入数字，输入 'q' 结束")

while True:
    user_input = input("> ")      # 这里会等待你输入
    
    if user_input == 'q':
        break
    
    try:
        num = int(user_input)
        calng.insert(num)
        print(f"当前堆: {calng.heap}")
    except:
        print("请输入数字！")

print(f"\n最终堆: {calng.heap}")
print(f"排序结果: ", end="")
sorted_list = []
while calng.size() > 0:
    sorted_list.append(calng.extract_max())
print(sorted_list[::-1])          # 升序