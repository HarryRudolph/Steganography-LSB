from PIL import Image

def lengthOfListOfList(inputList):
    total = 0
    for i in inputList:
        for j in i:
            total += 1
    
    return total

def loadImageData(path):
    i = Image.open(path)
    data = i.getdata()
    i.close()
    
    return data

def stringToNumberList(string):
    outputList = []
    for i in string:
        outputList.append(ord(i))
    outputList.append(ord(" ")) #last number can sometimes become jumbled.
    return outputList

def listToBytes(inList, maxLength): 
    bitCount = 0
    
    outList = []
    byte = ''
    
    for bit in range(maxLength): #TODO Need to think about how long the message is. It isn't helpful to store everything in memory. 
        if bitCount < 8:
            byte += str(inList[bit])
            bitCount += 1
        if bitCount == 8:
            outList.append(byte)
            byte = ''
            bitCount = 0
    return(outList)
    
def decode(path, maxLength): #Supposed to store length
    data = loadImageData(path)
    dataList = list(map(list, data)) #Python has funky tuple rules
    extractedList = []
    
    for i in range(len(dataList)):
        for rgb in range(3):
            extractedList.append(dataList[i][rgb] & 1)
            
    byteList = listToBytes(extractedList, maxLength) # Can this be one loop
    
    message = ''
    for i in range(len(byteList)):
        message += chr(int(byteList[i],2))
    print(message)
    

def binaryDataToList(data):
    binaryDataList = []

    for char in data:
        for i in range(8):
            filter = 1 << (7-i) #Creating a filter starting with leftmost digit.
            result = char & filter #Getting leftmost digit with filter
            bit = result >> (7-i) #Removing trailing 0s
            binaryDataList.append(bit)
    return binaryDataList

def replaceData(imageData, payload):
    binaryDataList = binaryDataToList(payload) #Is this line necessary? 

    if len(binaryDataList) <= lengthOfListOfList(imageData): #Check that input is smaller than image length
        j = 0
        for i in range(len(binaryDataList)//3):
            for rgb in range(3):

                imageData[i][rgb] &= 0b11111110 #0 the least significant bit
                imageData[i][rgb] |= binaryDataList[j] #Replace with new bit.
                j = j+1
        return(imageData)
    else:
        print("The input string is too long for the image")
        return None
        

def saveImage(data, size, mode):
    secretImage = Image.new(mode, size)
    secretImage.putdata(data)
    secretImage.save("secret.bmp", "BMP")

if __name__ == "__main__":
    imageData = loadImageData("glasgow.bmp")
    size = imageData.size
    mode = imageData.mode
    dataList = list(map(list, imageData)) #Python has funky tuple rules
        
    newData = replaceData(dataList, stringToNumberList("Hello my name is Harry"))

    dataTuples = list(map(tuple,newData))
    saveImage(dataTuples, size, mode)

    decode("secret.bmp", 200)
