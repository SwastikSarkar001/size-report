import os
from datetime import datetime
import pandas as pd
import time
import cursor
import matplotlib.pyplot as plot
from functools import lru_cache
import threading

class SizeReport:
  
    def __init__(self, path:str):
        self.path = path
        self.contentdetails = self.compute(self.path)
        self.df = pd.DataFrame(self.contentdetails)
        self.vrsn = '0.1.1'
        self.date = 'August 11, 2023'
    
    def version(self):
        print('Size Report Analyser')
        print("Version: {self.vrsn}")
        print("Released on: {self.date}")
    
    def __print(self, line):
        print('\r' + ' '*self.__n, end='\r')
        print('\r'+line, end='')
        self.__n = len(line)
    
    @lru_cache()
    def compactsize(self, size):
        st = str()
        if size < 1024:
            st = str(size) + 'B'
        elif size >= 1024 and size < 1024**2:
            s = size/1024
            st = str(float('%.2f' % s)) + "KB"
        elif size >= 1024**2 and size < 1024**3:
            s = size/(1024*1024)
            st = str(float('%.2f' % s)) + "MB"
        elif size >= 1024**3 and size < 1024**4:
            s = size/(1024*1024*1024)
            st = str(float('%.2f' % s)) + "GB"
        elif size >= 1024**4 and size < 1024**5:
            s = size/(1024*1024*1024*1024)
            st = str(float('%.2f' % s)) + "TB"
        return st

    @lru_cache()
    def getsize(self, path):
        r = 0
        try:
            c = os.listdir(path)
        except:
            return 0
        c = [path + "\\" + cn for cn in c]
        for f in c:
            # print(f)
            if os.path.isdir(f):
                a = self.getsize(f)
                if a is None:
                    a = 0
                r += a
            if os.path.isfile(f):
                s = 0
                try:
                    s = os.path.getsize(f)
                except:
                    pass
                r += s
        return r

    def compute(self, path):
        self.__n = 0
        cursor.hide()
        self.__print("\nInitialising...")
        time.sleep(3)
        path = path + '\\'
        contents = os.listdir(path)
        contents = [path + content for content in contents]
        # print(contents)
        contentdetails = list()
        threads = []
        for content in contents:
            fpath = content
            self.__print(f"Analyzing {fpath} ...")
            details = dict()
            date = float()
            try:
                date = os.path.getmtime(fpath)
                date = datetime.fromtimestamp(date).strftime("%b %d, %Y %I:%S %p")
            except:
                pass
                date = "Invalid"
            size = 0
            type = ""
            if os.path.isdir(fpath):
                size = self.getsize(fpath)
                type = 'dir'
            if os.path.isfile(fpath):
                try:
                    size = os.path.getsize(fpath)
                except:
                    size = 0
                type = 'file'
            
            details['Name'] = content
            details['Type'] = type
            details['Date'] = date
            details['Size (in B)'] = size
            details['Size'] = self.compactsize(size)
            
            contentdetails.append(details)
            
            self.__print(f"Appending {details['Name']} ...")
        
        self.__print("Scanning completed!!\n\n")
        cursor.show()
        self.__n = 0
        return contentdetails

    def write_csv(self):
        self.df.to_csv('Report.csv', index=False, header=True)
        print("Report.csv is written successfully!!")

    def write_xlsx(self):
        writer = pd.ExcelWriter('Report.xlsx')
        self.df.to_excel(writer, index=False, header=True)
        
    def plot_data(self):
        plot.pie(self.df['Size (in B)'],labels=self.df['Name'], autopct='%.2f%%')
        plot.show()