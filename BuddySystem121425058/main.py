import math

def initialize_memory(total_memory):

    #Initializes the memory blocks by dividing the total memory into powers of 2.
    #Total memory size provided by the user into a Dictionary of memory blocks and their  status.

    memory_blocks = {}
    block_size = 2
    address = 1

    # Divide memory into powers of 2 up to the given total memory, excluding total_memory itself
    while block_size <= total_memory:
        memory_blocks[f"address{address}"] = {
            "size": block_size,
            "status": 0
        }
        block_size *= 2
        address += 1

    return memory_blocks


def display_memory(memory_blocks):

    #Displays the memory blocks and their allocation status

    print("\nMemory Blocks:")
    for address, block in memory_blocks.items():
        status = "Free" if block["status"] == 0 else "Allocated"
        print(f"{address} (Size: {block['size']}): {status}")


def allocate_memory(memory_blocks, required_memory, total_memory):

    #Allocates the smallest available block that fit the required memory and updates the status.

    max_block_size = 0
    for block in memory_blocks.values():
        if block["size"] > max_block_size:
            max_block_size = block["size"]

    if required_memory > max_block_size:
        print("\nPlease Deallocate. Insufficient memory.")
        return total_memory, False

    for address in memory_blocks:
        block = memory_blocks[address]
        if block["status"] == 0 and block["size"] >= required_memory:
            block["status"] = 1
            print(f"\nMemory block {address} (Size: {block['size']}) allocated successfully.")
            total_memory -= block["size"]
            break
    else:
        print("\nPlease Deallocate. Insufficient memory.")
        return total_memory, False

    # Reinitialize memory blocks with the remaining total_memory
    return total_memory, True


def deallocate_memory(memory_blocks, address):

    #Deallocates the specified memory block by setting its status to free.

    if address in memory_blocks:
        if memory_blocks[address]["status"] == 1:
            memory_blocks[address]["status"] = 0
            print(f"\nMemory block {address} deallocated successfully.")
        else:
            print(f"\nMemory block {address} is already free.")
    else:
        print(f"\nInvalid address: {address}")


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
        total_memory, success = allocate_memory(memory_blocks, required_memory, total_memory)
        if not success:
            address = input("\nEnter the address of the memory block to deallocate: ")
            deallocate_memory(memory_blocks, address)

        # Reinitialize memory blocks with the remaining total_memory
        memory_blocks = initialize_memory(total_memory)
        display_memory(memory_blocks)

if __name__ == "__main__":
    main()
