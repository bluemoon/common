import csv
import os
import codecs
import glob

DIRECTORY = '/home/bluemoon/'
SUN_DATA = glob.glob(DIRECTORY + '[!modified]*.csv')
def read_data(file):
    if 'modified' in file:
        return
    
    file_handle = codecs.open(file, "r", "utf-16", errors='ignore' )
    reader = csv.reader(file_handle)
    for idx, row in enumerate(reader):
        if idx >= 19:
            ## excluding 4, 6, 8, 10, 12, 14, 16, 18, 20, 22
            ## minus 1 because the count starts at 0
            to_delete = [3,5,7,9,11,13,15,17,19,21]
            if len(row) == 22:
                for idx, x in enumerate(to_delete):
                ## offset it by the index because every time we delete one
                ## it shifts it by the amount we have deleted
                    del row[x-idx]
                    
            filename, ext = os.path.splitext(file)
            Writer = csv.writer(open(filename + 'modified' + ext, 'a'))
            Writer.writerow(row)
        

if __name__ == "__main__":
    for x in SUN_DATA:
        read_data(x)
