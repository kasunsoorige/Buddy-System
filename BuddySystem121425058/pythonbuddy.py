import math


class BuddySystem:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.free_list = [None] * memory_size
        self.order_max = int(math.log2(memory_size))

    def allocate(self, size):
        order = int(math.log2(size))
        index = self.find_free_block(order)
        if index == -1:
            return None

        self.split_block(index, order)
        self.free_list[index] = False
        return index

    def deallocate(self, index):
        if self.free_list[index]:
            return

        order = self.get_order(index)
        self.free_list[index] = True
        while order < self.order_max:
            buddy_index = index ^ (1 << order)
            if self.free_list[buddy_index]:
                self.merge_blocks(index, buddy_index, order)
                order += 1
            else:
                break

    def find_free_block(self, order):
        for i in range(self.memory_size):
            if self.free_list[i] and self.get_order(i) >= order:
                return i
        return -1

    def split_block(self, index, order):
        while order < self.order_max:
            left_child = index * 2
            right_child = index * 2 + 1
            self.free_list[left_child] = True
            self.free_list[right_child] = True
            index = left_child
            order += 1

    def merge_blocks(self, index1, index2, order):
        parent_index = index1 // 2
        self.free_list[parent_index] = True

    def get_order(self, index):
        return self.order_max - int(math.log2(index + 1))

    def print_memory_map(self):
        for i in range(self.memory_size):
            if self.free_list[i]:
                print(f"{i}: Free")
            else:
                print(f"{i}: Allocated")


if __name__ == "__main__":
    memory_size = int(input("Enter the total memory size: "))
    bs = BuddySystem(memory_size)

    while True:
        block_size = int(input("Enter the block size required (0 to exit): "))
        if block_size == 0:
            break

        allocated_index = bs.allocate(block_size)
        if allocated_index is not None:
            print(f"Block allocated at index: {allocated_index}")
        else:
            print("Memory allocation failed. Insufficient memory.")

        bs.print_memory_map()