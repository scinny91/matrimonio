
from matrimonio.backand.bo import base
from datetime import datetime
def main(params):
    print('ciao, io devo inviare la mail')

    with open("file.txt", "w") as myFile:
        myFile.write(str(datetime.now()))