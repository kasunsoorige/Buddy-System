import math

def initialize_memory(total_memory):
    """
    Initializes the memory blocks by dividing the total memory into powers of 2.
    :param total_memory: Total memory size provided by the user.
    :return: Dictionary of memory blocks and their allocation status.
    """
    memory_blocks = {}
    block_size = 2
    address = 1

    # Divide memory into powers of 2 up to the given total memory, excluding total_memory itself
    while block_size <= total_memory:
        memory_blocks[f"address{address}"] = {
            "size": block_size,
            "status": 0  # All blocks are initially free (0)
        }
        block_size *= 2
        address += 1

    return memory_blocks


def display_memory(memory_blocks):
    """
    Displays the memory blocks and their allocation status.
    :param memory_blocks: Dictionary of memory blocks.
    """
    print("\nMemory Blocks:")
    for address, block in memory_blocks.items():
        status = "Free" if block["status"] == 0 else "Allocated"
        print(f"{address} (Size: {block['size']}): {status}")


def allocate_memory(memory_blocks, required_memory, total_memory):
    """
    Allocates the smallest available block that can fit the required memory and updates the memory blocks.
    :param memory_blocks: Dictionary of memory blocks.
    :param required_memory: Memory size required for a process.
    :param total_memory: Total memory currently available for allocation.
    :return: Updated total_memory after allocation.
    """
    max_block_size = 0
    for block in memory_blocks.values():
        if block["size"] > max_block_size:
            max_block_size = block["size"]

    if required_memory > max_block_size:
        print("\nPlease Deallocate. Insufficient memory.")
        return total_memory

    for address in memory_blocks:
        block = memory_blocks[address]
        if block["status"] == 0 and block["size"] >= required_memory:
            block["status"] = 1
            print(f"\nMemory block {address} (Size: {block['size']}) allocated successfully.")
            total_memory -= block["size"]
            break
    else:
        print("\nPlease Deallocate. Insufficient memory.")

    # Reinitialize memory blocks with the remaining total_memory
    return total_memory


def main():
    print("Buddy System Memory Block Initialization")
    total_memory = int(input("Enter the total memory size (in units): "))

    # Initialize memory
    memory_blocks = initialize_memory(total_memory)

    # Display the initialized memory blocks
    display_memory(memory_blocks)

    # Allocate memory based on user input
    while True:
        required_memory = int(input("\nEnter the memory size required for a process (or 0 to exit): "))
        if required_memory == 0:
            print("Exiting the program.")
            break
        total_memory = allocate_memory(memory_blocks, required_memory, total_memory)
        memory_blocks = initialize_memory(total_memory)
        display_memory(memory_blocks)

if __name__ == "__main__":
    main()
