import math
from typing import Dict, Optional


class SimpleBuddySystem:
    def __init__(self, total_size: int):
        """Initialize buddy system with given total memory size."""
        if not self._is_power_of_two(total_size):
            raise ValueError("Memory size must be a power of 2")

        self.total_size = total_size
        # Dictionary to track memory blocks: {start_address: block_size}
        self.memory_blocks: Dict[int, int] = {0: total_size}
        # Dictionary to track which blocks are free: {start_address: is_free}
        self.free_blocks: Dict[int, bool] = {0: True}

    def allocate(self, size: int) -> Optional[int]:
        """Allocate a block of memory of given size."""
        # Round up size to next power of 2
        actual_size = self._next_power_of_two(size)

        # Find suitable free block
        for start_addr, block_size in sorted(self.memory_blocks.items()):
            if self.free_blocks[start_addr] and block_size >= actual_size:
                # Split block if necessary
                while block_size > actual_size:
                    block_size //= 2
                    new_addr = start_addr + block_size

                    # Add new block to our tracking dictionaries
                    self.memory_blocks[new_addr] = block_size
                    self.free_blocks[new_addr] = True
                    self.memory_blocks[start_addr] = block_size

                # Mark block as allocated
                self.free_blocks[start_addr] = False
                return start_addr

        return None  # No suitable block found

    def deallocate(self, addr: int):
        """Deallocate a block of memory at given address."""
        if addr not in self.memory_blocks:
            raise ValueError("Invalid address")

        # Mark block as free
        self.free_blocks[addr] = True

        # Try to merge with buddy blocks
        while True:
            buddy_addr = self._get_buddy_address(addr)
            block_size = self.memory_blocks[addr]

            # Check if buddy exists and is free
            if (buddy_addr in self.free_blocks and
                    self.free_blocks[buddy_addr] and
                    self.memory_blocks[buddy_addr] == block_size):

                # Merge blocks
                start_addr = min(addr, buddy_addr)
                self.memory_blocks[start_addr] = block_size * 2

                # Remove buddy block from tracking
                del self.memory_blocks[max(addr, buddy_addr)]
                del self.free_blocks[max(addr, buddy_addr)]

                # Continue with merged block
                addr = start_addr

                # Stop if we've reached maximum block size
                if block_size * 2 == self.total_size:
                    break
            else:
                break

    def print_memory_map(self):
        """Print current state of memory."""
        print("\nMemory Map:")
        for addr in sorted(self.memory_blocks.keys()):
            status = "Free" if self.free_blocks[addr] else "Allocated"
            size = self.memory_blocks[addr]
            print(f"Address: {addr}, Size: {size}, Status: {status}")

    def _is_power_of_two(self, n: int) -> bool:
        """Check if a number is a power of 2."""
        return n > 0 and (n & (n - 1)) == 0

    def _next_power_of_two(self, n: int) -> int:
        """Get next power of 2 for a number."""
        return 1 if n == 0 else 2 ** math.ceil(math.log2(n))

    def _get_buddy_address(self, addr: int) -> int:
        """Calculate buddy address for a given address."""
        block_size = self.memory_blocks[addr]
        return addr ^ block_size


# Example usage
def main():
    # Initialize buddy system with 16 units of memory
    buddy = SimpleBuddySystem(16)

    print("Initial state:")
    buddy.print_memory_map()

    # Allocate some memory
    addr1 = buddy.allocate(3)  # Will allocate 4 units
    print("\nAfter allocating 3 units (rounded up to 4):")
    buddy.print_memory_map()

    addr2 = buddy.allocate(2)  # Will allocate 2 units
    print("\nAfter allocating 2 units:")
    buddy.print_memory_map()

    # Deallocate memory
    buddy.deallocate(addr1)
    print("\nAfter deallocating first block:")
    buddy.print_memory_map()


if __name__ == "__main__":
    main()