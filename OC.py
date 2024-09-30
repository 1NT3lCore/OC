class MemoryManager:
    def __init__(self, size, block_size):
        self.memory = [None] * size
        self.free_blocks = [True] * ((size + block_size - 1) // block_size)
        self.total_free = self.free_blocks.count(True)
        self.occupied_blocks = 0
        self.occupied_memory = 0
        self.block_size = block_size

    def allocate(self, size):
        if size > len(self.memory):
            print("Not enough memory")
            return None, 0

        blocks_needed = (size + self.block_size - 1) // self.block_size

        if blocks_needed > self.total_free:
            print("Not enough free blocks")
            return None, 0

        # Ищем свободные блоки
        free_blocks = []
        for i in range(len(self.free_blocks)):
            if self.free_blocks[i]:
                free_blocks.append(i)

        # Проверяем, есть ли непрерывные свободные блоки
        for i in range(len(free_blocks) - blocks_needed + 1):
            if all(free_blocks[i + j] == free_blocks[i] + j for j in range(blocks_needed)):
                start = free_blocks[i]
                break
        else:
            print("Not enough contiguous free blocks")
            return None, 0

        self.total_free -= blocks_needed
        self.occupied_blocks += blocks_needed
        self.occupied_memory += size

        for i in range(blocks_needed):
            self.free_blocks[start + i] = False

        return start * self.block_size, blocks_needed

    def deallocate(self, ptr, blocks):
        if ptr is None:
            print("Cannot deallocate: memory was not allocated")
            return

        start, _ = divmod(ptr, self.block_size)

        if start + blocks >= len(self.free_blocks):
            print("Error: Out of vector free_blocks range")
            return

        end = start + blocks - 1

        for i in range(start, end + 1):
            self.free_blocks[i] = True

        self.total_free += blocks
        self.occupied_blocks -= blocks
        self.occupied_memory -= blocks * self.block_size

    def get_info(self):
        for i, is_free in enumerate(self.free_blocks):
            address = i * self.block_size
            status = "Free" if is_free else "Occupied"
            print(f"Block {i}: Address - {address}, Status - {status}, Size - {self.block_size} bytes")

    def get_bit_map(self):
        bit_map = ''
        for is_free in self.free_blocks:
            bit_map += '1' if is_free else '0'
        return bit_map


def main():
    size = int(input("Enter the total size of memory: "))
    block_size = int(input("Enter the block size: "))
    manager = MemoryManager(size, block_size)

    while True:
        print("\n1. Allocate memory")
        print("2. Deallocate memory")
        print("3. Get memory info")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            memory_size = int(input("Enter the size of memory to allocate: "))
            ptr, blocks = manager.allocate(memory_size)
            if ptr is not None:
                print(f"Memory allocated successfully at address {ptr} ({blocks} blocks)")
            else:
                print("Memory allocation failed")

        elif choice == "2":
            ptr = int(input("Enter the starting address of the memory to deallocate: "))
            blocks = int(input("Enter the number of blocks to deallocate: "))
            manager.deallocate(ptr, blocks)
            print("Memory deallocated successfully")


        elif choice == "3":

            manager.get_info()

            print("Битовая карта:")

            print(manager.get_bit_map())

        elif choice == "4":
            print("Exiting the program")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()


