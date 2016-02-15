__author__ = 'rjaffe'
# -*- coding: utf-8 -*-
# Python 3.4.2

import csv, sys, codecs

# Read in csv file to a dictionary.
# Key = everything in col 1 that follows "Company Home/.../Media/"
# Value = entire row.
# Then, read working-files_fileList.txt
# For each line, if txt == a key in the dictionary, copy the value of \
# that dictionary item to a match list.
# When done, print the match list to a file.

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
        with open('cleanDict_py3.txt', 'w') as dictfile:
            dictfile.write(output)
    return mycleandict

def filterMetadataUsingFiles(fileList):
    """
    Takes text file with list of file names.
    Filters .csv file to return only the rows in the .csv file that correspond to
    the files in the list.



    Prints new .csv file, plus a .txt file listing files not included in .csv
    :param fileList:
    :return:
    """
    # Replace sys.argv[1] with 'all-metadata_REUPS.csv' when running in pyCharm
    outputcsvfile = open('filtered_' + 'all-metadata_REUPS_py3.csv', 'w', newline='')
    outputwriter = csv.writer(outputcsvfile, delimiter=",", quoting=csv.QUOTE_ALL)

    # Try this instead:
    # global outputwriter
    #    # Replace sys.argv[1] with 'all-metadata_REUPS.csv' when running in pyCharm
    #    with open('filtered_' + 'all-metadata_REUPS_py3.csv', 'w', newline='') as outputcsvfile:
    #        outputwriter = csv.writer(outputcsvfile, delimiter=",", quoting=csv.QUOTE_ALL)


    mycleandict = {}

    # Replace sys.argv[1] with 'all-metadata_REUPS.csv' when running in pyCharm
    mycleandict = makeDictFromCsv('../all-metadata_REUPS.csv')

    with codecs.open(fileList, 'r', 'utf-8' ) as f:
        with open('notInCSV.txt', 'w') as f_not:
            myfiles = [line.rstrip('\n') for line in f]
            for myfile in myfiles:
                if myfile in mycleandict:
                    row = mycleandict[myfile]
                    outputwriter.writerow(row)
                else:
                    notInCsv = str(myfile + '\n')
                    f_not.write(notInCsv)


# TODO: Refactor to allow user to pass in files list as argument (sysargv[2]?).
filterMetadataUsingFiles('../working-files-file-list.txt')

