from PIL import Image

def lengthOfListOfList(inputList):
    total = 0
    for i in inputList:
        for j in i:
            total += 1
    return total

def loadImage(path):
    i = Image.open(path)
    imageData = i.getdata()
    i.close()
    return imageData

def payloadToBinaryList(payload):
    characterList = []
    payloadBitList = []
    
    for char in payload:
        characterList.append(ord(char))
    characterList.append(ord(" ")) #last number can sometimes become jumbled.
    
    #Add length of list to start.
    payloadByteLength = len(characterList)

    #3 bytes to store size of message. 16,777,215 bytes(ASCII characters) max
    binaryLength = payloadByteLength | (1<<24) #Binary representation of length, need the 1 to keep in onder

    j = 0
    for i in bin(binaryLength):
        if j > 2: #To Ignore 0b1.... 
            payloadBitList.append(int(i))
        j += 1
        
    for char in characterList:
        for i in range(8):
            filter = 1 << (7-i) #Creating a filter starting with leftmost digit.
            result = char & filter #Getting leftmost digit with filter
            bit = result >> (7-i) #Removing trailing 0s
            payloadBitList.append(bit)
    return payloadBitList

def replaceData(imageData, payload):
    payloadBitList = payloadToBinaryList(payload)
    
    if len(payloadBitList) <= lengthOfListOfList(imageData): #Todo, just *3 remove method
        j = 0
        for i in range(len(payloadBitList)//3):
            for rgb in range(3):
                imageData[i][rgb] &= 0b11111110 #0 the least significant bit
                imageData[i][rgb] |= payloadBitList[j] #Replace with new bit.
                j = j+1
        return(imageData)
    else:
        print("The input string is too long for the image")
        return None
        

def saveImage(data, size, mode):
    secretImage = Image.new(mode, size)
    secretImage.putdata(data)
    secretImage.save("secret.bmp", "BMP")



def lsbToCharacters(inList): 
    messageLength = 0
    tempList = []
    for i in range(24):
        #tempList.append(inList[i])
        # Can do something like x = x << 0 |i for each iteration. So don't have to think about strings. Can also do this below I believe. 
        messageLength = (messageLength << 1) | inList[i] 
        
    bitCount = 0
    outList = []
    byte = 0
    for bit in range(24, (messageLength*8) + 24): #TODO use length 
        if bitCount < 8:
            byte = (byte << 1) | inList[bit]
            bitCount += 1
        if bitCount == 8:
            outList.append(chr(byte))
            byte = 0
            bitCount = 0
    return(outList)

def decode(path): #Supposed to store length
    data = loadImage(path)
    dataList = list(map(list, data)) #Python has funky tuple rules
    extractedList = []
    
    for i in range(len(dataList)):
        for rgb in range(3):
            extractedList.append(dataList[i][rgb] & 1)
            
    byteList = lsbToCharacters(extractedList)
    
    message = ''
    for i in range(len(byteList)):
        message += byteList[i]
    print(message)
    
    
if __name__ == "__main__":
    imageData = loadImage("glasgow.bmp")
    size = imageData.size
    mode = imageData.mode
    dataList = list(map(list, imageData)) #Python has funky tuple rules
        
    newData = replaceData(dataList, "Hello")

    dataTuples = list(map(tuple,newData))
    saveImage(dataTuples, size, mode)

    decode("secret.bmp")
