__author__ = 'rjaffe'
# -*- coding: utf-8 -*-
# Python 3.4.2

import csv, sys, codecs

# Read in csv file to a dictionary.
# Key = everything in col 1 that follows "Company Home/.../Media/"
# Value = entire row.
# Then, read working-files_fileList.txt
# For each line, if txt == a key in the dictionary, copy the value of that dictionary item to a match list.
# When done, print the match list to a file.

# Two functions for handling unicode input. From Python documentation at:
# https://docs.python.org/2/library/csv.html#examples


# def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
#     # csv.py doesn't do Unicode; encode temporarily as UTF-8:
#     csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
#                             dialect=dialect, **kwargs)
#     for row in csv_reader:
#         # decode UTF-8 back to Unicode, cell by cell:
#         yield [unicode(cell, 'utf-8') for cell in row]
#
# def utf_8_encoder(unicode_csv_data):
#     for line in unicode_csv_data:
#         yield line.encode('utf-8')

# Replace sys.argv[1] with 'all-metadata_REUPS.csv' when running in pyCharm
def cleanKeys(dict):
    """
    Strips the path segment in prefix from the head of each key in the input dictionary.

    Returns a new dictionary.
    :param dict:
    :return dict2:
    """
    dict2 = {}
    prefix = '/Company Home/Sites/bampfa/documentLibrary/Media/'
    for k,v in dict.items():
        if k.startswith(prefix):
            k2 = k[len(prefix):]
            dict2.update({k2:v})
    return dict2

def makeDictFromCsv(f):
    """
    Reads .csv file and creates a dictionary.
    Passes initial dictionary to cleanKeys() to strip leading path segments from keys.

    Returns a dictionary
    :param f:
    :return mycleandict:
    """
    with open(f, newline='') as csvfile:
        reader = csv.reader(csvfile)
        mydict = dict((rows[0], rows) for rows in reader)
        mycleandict = cleanKeys(mydict)
        output = str(mycleandict)
        with open('cleanDict.txt', 'w') as dictfile:
            dictfile.write(output)
    return mycleandict

def filterMetadataUsingFiles(fileList):
    """
    Takes text file with list of file names.
    Filters .csv file to return only the rows in the .csv file that correspond to the files in the list.

    Prints new .csv file.
    :param fileList:
    :return:
    """
    # Replace sys.argv[1] with 'all-metadata_REUPS.csv' when running in pyCharm
    outputcsvfile = open('filtered_' + 'all-metadata_REUPS_unicode_py3.csv', 'w', newline='')
    outputwriter = csv.writer(outputcsvfile, delimiter=",", quoting=csv.QUOTE_ALL)

    mycleandict = {}
#    myFilteredList = []

    # Replace sys.argv[1] with 'all-metadata_REUPS.csv' when running in pyCharm
    mycleandict = makeDictFromCsv('../all-metadata_REUPS.csv')

    with codecs.open(fileList, 'r', 'utf-8' ) as f:
        myfiles = [line.rstrip('\n') for line in f]
        for myfile in myfiles:
            if myfile in mycleandict:
#                myFilteredList.append(mycleandict[myfile])
                row = mycleandict[myfile]
                outputwriter.writerow(row)

#    DEBUG = "Uncomment this line to pause here before finishing"

# TODO: Refactor to allow user to pass in files list as argument.
filterMetadataUsingFiles('../working-files-file-list.txt')
#filterMetadataUsingFiles('reupthese-files_fileList.txt')
