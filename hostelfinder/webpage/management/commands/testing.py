from django.core.management.base import BaseCommand
from webpage.models import User, HostelOwner, Student
import csv
import random

college = []

def evaluate_mae(predict_data,test_data):
    sum=0
    if len(predict_data)==len(test_data):
        for p in range(len(predict_data)):
            sum=sum+abs((float(predict_data[p])-float(test_data[p])))
        rma = sum/len(predict_data)
    return round(rma,2)

# def evaluate_average(test_data):
#     sum = 0
#     for t in range(len(test_data)):
#         sum = sum + float(test_data[t])
#     avg = sum / len(test_data)
#     return round(avg,2)

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('predict_data', type=str, help="hostel detail")
        parser.add_argument('test_data', type=str, help="hostel detail")

    def handle(self,*args,**kwargs):
        predict_data = kwargs['predict_data']
        test_data = kwargs['test_data']

        predict_data_values = []
        test_data_values = []

        with open(f'{predict_data}.csv', 'r') as file:
            predict_data_reader = csv.reader(file)
            next(predict_data_reader)

            for line in file:
                rate = line.split(',')

                for r in range(len(rate)-1):
                    predict_data_values.append(rate[r+1])

        with open(f'{test_data}.csv','r') as file:
            test_data_reader = csv.reader(file)
            next(test_data_reader)

            for line in file:
                rate = line.split(',')

                for r in range(len(rate) - 1):
                    test_data_values.append(rate[r + 1])

        mae = evaluate_mae(predict_data_values,test_data_values)
        print('mae = '+str(mae))

        # avg = evaluate_average(test_data_values)
        percent = mae*100

        print("error percentage = " + str(percent))