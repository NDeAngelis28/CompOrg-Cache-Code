import math

def cacheArchitecture():
    nominalSize = input("Please Input the Nominal Size of your Cache (Ex. 128 KB): ")
    wordsPerBlock = int(float(input("Please Input the Words per Block in your Cache (Powers of 2): ")))
    
    blocks = numOfBlocks(nominalSize, wordsPerBlock)
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
            return 0
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
    blocks = (2 ** powerOfNomSize) / bytesPerBlock

    return blocks

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

def realSize():
    return 0

cacheArchitecture()