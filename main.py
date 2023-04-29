# Main file running all tests

import storjTest
import dropboxTest
import googledriveTest
import onedriveTest


def addNextline(filename):
    f = open(filename, 'a', encoding='utf-8')
    f.write("\n")
    f.close()


if __name__ == '__main__':
    f = open("AccessStats.txt", 'w', encoding='utf-8')
    f.write("Provider,UplFile5,DownlFile5,Provider,UplFile50,DownlFile50,\n")
    f.close()

    for x in range(10):

        storjTest.main("5MB.bin")
        storjTest.main("50MB.bin")

        addNextline("AccessStats.txt")

        dropboxTest.main("5MB.bin")
        dropboxTest.main("50MB.bin")

        addNextline("AccessStats.txt")

        googledriveTest.main("5MB.bin", '1xRb-nXRJpNsLfahsfchfk6qHryzmTndS')
        googledriveTest.main("50MB.bin", '1Z6Bj9T_NmKmROzfwkQUuPj4mz82OXSj-')

        addNextline("AccessStats.txt")

        onedriveTest.main("5MB.bin", "98117D10CBE992ED!117")
        onedriveTest.main("50MB.bin", "98117D10CBE992ED!118")

        addNextline("AccessStats.txt")
