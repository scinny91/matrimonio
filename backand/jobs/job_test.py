
from matrimonio.backand.bo import base

def main(params):
    print('ciao, io devo inviare la mail')


    for famiglia in base.Famiglia.objects.filter():
        print(famiglia.__dict__)