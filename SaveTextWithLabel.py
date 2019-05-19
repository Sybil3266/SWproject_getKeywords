fp = open("C:\\users\\user\Desktop\SWProject\SWproject_getKeywords\CrawlingData_pebble.txt", "r", encoding = "utf-8")
writefp = open("C:\\users\\user\Desktop\SWProject\SWproject_getKeywords\MyLabeledData_pebble.txt", "w", encoding = "utf-8")
while True:
    line = fp.readline()
    line = '__label__' + str(line)
    writefp.write(str(line))
    if not fp.readline(): break

fp.close()
writefp.close()
