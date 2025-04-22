import math
import random


def cacheArchitecture():
    nominalSize = input("Please Input the Nominal Size of your Cache (Ex. 128 KB): ")
    wordsPerBlock = int(float(input("Please Input the Words per Block in your Cache (Powers of 2): ")))
    
    nomSize, blocks = numOfBlocks(nominalSize, wordsPerBlock)
    if (blocks is not None):
        blocksExponent = int(math.log2(blocks))
        if (blocksExponent > 9):
            print(f"Block Count: 2^{blocksExponent} Blocks")
        else:
            print(f"Block Count: {blocks} Blocks")
    else:
        print("Failed!")

    mappingPolicy = input("Please Select your Cache's Mapping Policy (Direct Mapping or Set Associative): ")
    match mappingPolicy.strip().upper():
        case "DIRECT MAPPING":
            print("Direct Mapping Does Not Use Sets.")
            sets = 1
        case "SET ASSOCIATIVE":
            blocksPerSet = input("Please Input the Blocks per Set that Matches your Associativity (Powers of 2: Direct Mapping = 1, 2-Way = 2, Etc.): ")
            sets = numOfSets(blocks, blocksPerSet)
            if (sets is not None):
                setsExponent = int(math.log2(sets))
                if (setsExponent > 9):
                    print(f"Set Count: 2^{setsExponent} Sets")
                else:
                    print(f"Set Count: {sets} Sets")
            else:
                print("Failed!")
        case _:
            print("Invalid Input Format: Please Select One of the Declared Option! Please Try Again Later!")

    offset, index, tag = partitioning(wordsPerBlock, blocks, sets)
    print(f"The Addressing Within the Cache is as Follows: \n\tOffset: {offset}\n\tIndex: {index}\n\tTag: {tag}")

    size = realSize(nomSize, blocks, tag)
    powerOfRealSize = math.log2(size)
    if (powerOfRealSize < 10):
        print(f"The Real Size of the Cache is: {size} B")
    elif (powerOfRealSize >= 10):
        baseOutput = powerOfRealSize % 10
        baseTransformation = powerOfRealSize - baseOutput

        match baseTransformation:
            case 10:
                print(f"The Real Size of the Cache is: {(2 ** baseOutput) // 1} KB")
            case 20:
                print(f"The Real Size of the Cache is: {(2 ** baseOutput) // 1} MB")
            case 30:
                print(f"The Real Size of the Cache is: {(2 ** baseOutput) // 1} GB")
            case 40:
                print(f"The Real Size of the Cache is: {(2 ** baseOutput) // 1} TB")
            case 50:
                print(f"The Real Size of the Cache is: {(2 ** baseOutput) // 1} PB")
            case _:
                print(f"If The Cache is More Than a Petabyte, You Are Going to Have a Bad Time!")

    manual_access(wordsPerBlock, blocks, sets, mappingPolicy)

    if input("\nWould you like to run the automatic simulation mode? ") == "yes":
        numAccesses = int(input("How many accesses would you like to simulate? "))
        maxWords = int(input("What is the maximum address you would like to allow? "))

        simulate_mode(wordsPerBlock, blocks, sets, mappingPolicy, numAccesses, maxWords)
    else:
        print("Goodbye!")



def numOfBlocks(nominalSize, wordsPerBlock):
    nomSizeParts = nominalSize.strip().split()
    
    if len(nomSizeParts) == 2:
        nomSizeNum = int(float(nomSizeParts[0]))
        nomSizeByting = nomSizeParts[1].upper()
    else:
        print("Invalid Input Format: Please Try Again Later!")
        nomSizeNum = None
        nomSizeByting = None
        return None
    
    match nomSizeByting:
        case "B":
            byting = 2 ** 0
        case "KB":
            byting = 2 ** 10
        case "MB":
            byting = 2 ** 20
        case "GB":
            byting = 2 ** 30
        case "TB":
            byting = 2 ** 40
        case _:
            print("Invalid Input: The Program Does Not Calculate Nominal Sizes that High! Please Try Again Later!")
            return None
    
    bytesPerBlock = wordsPerBlock * 4
    powerOfNomSize = math.log2(nomSizeNum) + math.log2(byting)
    nomSize = (2 ** powerOfNomSize)
    blocks = nomSize / bytesPerBlock

    return nomSize, blocks



def numOfSets(blocks, associativity):
    associativity = int(associativity)
    sets = blocks // associativity
    return sets



def partitioning(wordsPerBlock, blocks, sets):
    bytesPerBlock = wordsPerBlock * 4
    offset = math.log2(bytesPerBlock)

    if (sets > 1):
        index = math.log2(sets)
    else:
        index = math.log2(blocks)
    
    tag = 32 - (offset + index)
    
    return offset, index, tag



def realSize(nomSize, blocks, tag):
    multiplier = (tag + 1) / 8
    increase = blocks * multiplier
    size = nomSize + increase
    return size



# Cache simulation variables
cache = {}              # Stores the cache blocks based on mapping policy
access_table = []       # Keeps track of access history for reporting

# Resets the cache and access history
def clear_cache():
    global cache, access_table
    cache.clear()
    access_table.clear()
    print("Cache and access history cleared.")

# Prints the current contents of the cache in a readable format
def print_cache_table(mappingPolicy, blocks, sets, wordsPerBlock):
    if mappingPolicy.upper() == "DIRECT MAPPING":
        print("\nCache Content (Direct Mapped):")
        print(f"{'Index':<6} | {'Block Info':<18}")
        print("-" * 28)
        for i in range(int(blocks)):
            block = cache.get(i)
            if block is not None:
                # Calculate word range for each block
                w_start = block * wordsPerBlock
                w_end = w_start + wordsPerBlock - 1
                value = f"b{block}(w{w_start}-{w_end})"
            else:
                value = "Empty"
            print(f"{i:<6} | {value:<18}")
    else:
        # Set-associative formatting
        ways = int(blocks) // int(sets)
        print(f"\nCache Content ({ways}-way Set Associative):")
        header = "Set | " + " | ".join(f"{w}" for w in range(ways))
        print(header)
        print("-" * len(header))
        for s in range(int(sets)):
            row = f"{s:<3} |"
            for w in range(ways):
                block = cache.get((s, w))
                if block is not None:
                    w_start = block * wordsPerBlock
                    w_end = w_start + wordsPerBlock - 1
                    val = f"b{block}(w{w_start}-{w_end})"
                else:
                    val = "Empty"
                row += f" {val:<18}|"
            print(row)

# Simulates user access to cache and performs hit/miss logic
def manual_access(wordsPerBlock, blocks, sets, mappingPolicy):
    while True:
        user_input = input("\nEnter a word address (or type 'clear' to reset cache, 'exit' to quit): ").strip()

        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'clear':
            clear_cache()
            continue

        try:
            word_address = int(user_input)
        except ValueError:
            print("Invalid Input Format: Please Try Again!")
            continue

        # Determine the block number the word belongs to
        block_number = word_address // wordsPerBlock

        # DIRECT MAPPING policy
        if mappingPolicy.upper() == "DIRECT MAPPING":
            index = block_number % int(blocks)
            cache_key = index
            is_hit = cache.get(cache_key) == block_number
            if not is_hit:
                cache[cache_key] = block_number  # Replace block in case of miss

        # SET ASSOCIATIVE policy
        else:
            ways = int(blocks) // int(sets)
            set_index = block_number % int(sets)
            is_hit = False
            empty_way = None

            # Search all ways for a hit or an empty slot
            for way in range(ways):
                key = (set_index, way)
                if cache.get(key) == block_number:
                    is_hit = True
                    break
                if cache.get(key) is None and empty_way is None:
                    empty_way = way

            # If miss, place in empty slot or replace way 0 (no LRU used)
            if not is_hit:
                way_to_fill = empty_way if empty_way is not None else 0
                cache[(set_index, way_to_fill)] = block_number

        # Record access
        access_table.append({
            "Word": word_address,
            "Set/Index": set_index if mappingPolicy.upper() != "DIRECT MAPPING" else index,
            "Block": block_number,
            "Hit": is_hit,
        })

        # Report results of access
        print(f"\nAccessing Address: {word_address}")
        print(f"Located in Cache at: {'Set ' + str(set_index) if mappingPolicy.upper() != 'DIRECT MAPPING' else 'Index ' + str(index)}")
        print(f"{'HIT' if is_hit else 'MISS'}")

        # Display full access history
        print("\nAccesses:")
        for entry in access_table:
            loc = f"Set {entry['Set/Index']}" if mappingPolicy.upper() != "DIRECT MAPPING" else f"Index {entry['Set/Index']}"
            block = entry['Block']
            w_start = block * wordsPerBlock
            w_end = w_start + wordsPerBlock - 1
            print(f"Word {entry['Word']}: {loc}, b{block}(w{w_start},{w_end}) -> {'HIT' if entry['Hit'] else 'MISS'}")

        # Display current cache content
        print_cache_table(mappingPolicy, blocks, sets, wordsPerBlock)


def simulate_mode(wordsPerBlock, blocks, sets, mappingPolicy, num_accesses, max_word_address):
    clear_cache()  # Reset cache before simulation
    print(f"\n--- Starting Simulation Mode ---")
    print(f"Generating {num_accesses} accesses (max word address: {max_word_address})...\n")

    hit_count = 0
    miss_count = 0

    for _ in range(num_accesses):
        word_address = random.randint(0, max_word_address)

        block_number = word_address // wordsPerBlock

        if mappingPolicy.upper() == "DIRECT MAPPING":
            index = block_number % int(blocks)
            cache_key = index
            is_hit = cache.get(cache_key) == block_number
            if not is_hit:
                cache[cache_key] = block_number
        else:
            ways = int(blocks) // int(sets)
            set_index = block_number % int(sets)
            is_hit = False
            empty_way = None

            for way in range(ways):
                key = (set_index, way)
                if cache.get(key) == block_number:
                    is_hit = True
                    break
                if cache.get(key) is None and empty_way is None:
                    empty_way = way

            if not is_hit:
                way_to_fill = empty_way if empty_way is not None else 0
                cache[(set_index, way_to_fill)] = block_number

        access_table.append({
            "Word": word_address,
            "Set/Index": set_index if mappingPolicy.upper() != "DIRECT MAPPING" else index,
            "Block": block_number,
            "Hit": is_hit,
        })

        if is_hit:
            hit_count += 1
        else:
            miss_count += 1

    total = hit_count + miss_count
    hit_rate = (hit_count / total) * 100
    miss_rate = (miss_count / total) * 100

    print_cache_table(mappingPolicy, blocks, sets, wordsPerBlock)

    print("\n--- Simulation Results ---")
    print(f"Total Accesses: {total}")
    print(f"Hits: {hit_count}")
    print(f"Misses: {miss_count}")
    print(f"Hit Rate: {hit_rate:.2f}%")
    print(f"Miss Rate: {miss_rate:.2f}%")

    # Ask user if they want to see detailed access logs
    show_accesses = input("Would you like to print the full access list? ")
    if show_accesses:
        print("\n--- Access List ---")
        print(f"{'#':<4} {'Word':<8} {'Set/Index':<12} {'Block':<8} {'Range':<15} {'Result':<6}")
        print("-" * 65)
        for i, entry in enumerate(access_table, start=1):
            loc = f"Set {entry['Set/Index']}" if mappingPolicy.upper() != "DIRECT MAPPING" else f"Index {entry['Set/Index']}"
            block = entry['Block']
            w_start = block * wordsPerBlock
            w_end = w_start + wordsPerBlock - 1
            result = "HIT" if entry['Hit'] else "MISS"
            print(f"{i:<4} {entry['Word']:<8} {loc:<12} b{block:<7} w{w_start}-{w_end:<7} {result:<6}")






cacheArchitecture()
