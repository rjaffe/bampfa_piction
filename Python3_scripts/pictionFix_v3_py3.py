__author__ = 'rjaffe'
# python 3.4.2

import os, csv, sys, re, shutil, logging
from datetime import datetime

logfiledate = datetime.now().strftime("%Y%m%d-%H%M%S")
logging.basicConfig(filename='./logs/piction-reupload-fix_' + logfiledate + '.log', level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(message)s')

namepattern = re.compile('([^a-zA-Z0-9/_\.\-])')
rhbasepath = '/Company Home/Sites/bampfa/documentLibrary/Media'

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    logging.info('\tcreated dirs %s' % d)


def swap_by_char(phrase):
    """
    Accepts string. Replaces characters thought to have caused Piction upload failures with
    ASCII substitutes designed to maintain fidelity, readability of values

    Returns a string which is a modified version of the provided phrase
    :param : phrase
    :rtype :  str
    :return : phrase
    """
    # These are the characters being replaced (keys) and their replacements (values)
    sw = {'&' : '-', ' & ' : '-', '\'' : '', '@' : 'a', ',' : '-', '$' : '', '…' : '-', '—' : '-',
          '!' : '', '#' : '', '%':'-', ' ':'-', '˜':'-', 'ă':'a', 'á':'a', 'à':'a', 'ä':'a', 'Á':'A', 'ç':'c',
          'é':'e', 'è':'e', 'í':'i', 'ï':'i', 'ö':'o', 'ó':'o', 'ô':'o', 'ß':'ss', 'ü': 'u', 'ú':'u'  }
    repl = ''
    for c in phrase:
        if c in sw:
            c = sw[c]
        repl=repl+c
    phrase = repl
    return phrase


def filter_and_copy(row, extractedvars, newmetadata):
    """
    Filter out this row of metadata if no newmetadata is passed in (i.e., the path and filename do not match
    any of the files on disk to be uploaded. If newmetadata is passed in, filter out files that are
    0 in size or are .DS_Store files. Copy the remaining files to re-upload directory.

    :param : row
    :param : extractedvars
    :param : newmetadata
    :return :
    """
    # Now copy the files on disk to a new file structure. But first...
    # filter out files on disk that we don't want to reupload:
    # empty files (corrupted to, in or from Research Hub) and .DS_Store files.
    # NOTE that folders, like empty files, have a size of 0, and yet we must copy folders
    # to keep the integrity of the tree, so we can't just filter out all items with size = 0.
    # NOTE, too, that for dev purposes we copy all the files -- we pass the ones we want
    # to a 'reupthese-files' directory and the others to a 'dontreupthese-files' directory.
    localpath, name, mimetype, size = extractedvars
    newpath, newname = newmetadata
    # TODO: Combine if and else into one code block?
    if (size != '0' and newname != '.DS_Store') or mimetype == 'FOLDER':
        # Eventually, this will be the path on the Piction servers, passed in as argument.
        # During dev, use 'reupthese-files'
        reupbasepath =  sys.argv[3] + rhbasepath
        # Replace local path, i.e. '../working-files', '../working-files-test-set', etc.
        newpath = reupbasepath + newpath.replace(sys.argv[2], '')
        #logging.info('\tchanged:    %s\t%s' % (localpath, newpath))
        row[0] = newpath
        row[2] = newname
        # Output modified metadata to new .csv file
        outputwriter.writerow(row)
        # Copy file to new destination, i.e., re-upload it to Piction servers.
        try:
            ensure_dir(newpath)
        except:
            #pass
            logging.info('\tCould not ensure directory at %s' % newpath)
        try:
            shutil.copy2(localpath, newpath)
            logging.info('\treupload - copy succeeded %s' % newpath)
        except:
            #pass
            logging.info('\tcould not copy %s' % newpath)

    else:
        # Directory to catch files that failed to upload - passed in as argument
        dontreupbasepath = sys.argv[4] + rhbasepath
        # Replace local path ../working-files', '../working-files-test-set', etc.
        newpath = dontreupbasepath + newpath.replace(sys.argv[2], '')
        #logging.info('\tchanged:    %s\t%s' % (localpath, newpath))
        row[0] = newpath
        row[2] = newname
        # Output modified metadata to new .csv file even if file has failed re-upload.
        outputwriter.writerow(row)
        # Copy file to catch-basin for files that failed re-upload.
        try:
            ensure_dir(newpath)
        except:
            #pass
            logging.info('\tCould not ensure directory at %s' % newpath)
        try:
            shutil.copy2(localpath, newpath)
            logging.info('\tdont reupload - copy succeeded %s' % newpath)
        except:
            #pass
            logging.info('\tcould not copy %s' % newpath)

def read_mod_reup(csvsrc):
    """
    Open a new csv file to which to write modified metadata. Read each row of Research Hub metadata
    from existing csv file. Pass each row to the ensuing functions to modify the metadata and copy
    the file. Need to fully process each row of Research Hub metadata before moving on to the next.

    Yields 'myrow', a list of comma-separated values
    """
    global outputwriter
    with open('metadata_REUPLOAD1.csv', 'w', newline='') as outputcsvfile:
        outputwriter = csv.writer(outputcsvfile, delimiter=",", quoting=csv.QUOTE_ALL)

        with open(csvsrc, newline='') as csvfile:
            for row in csv.reader(csvfile, delimiter=","):
                assert isinstance(row, object)
                myrow = row

                # From row of Research Hub metadata, extract the RH_PATH, RH_NAME, RH_MIMETYPE and RH_SIZE
                # fields to variables. Modify Research Hub basepath to point to files on current storage device.
                # Local path to files passed in as second argument with no trailing slash
                localpath = row[0].replace(rhbasepath, sys.argv[2])
                logging.info('\tLocal path: ' + localpath)
                name = row[2]
                mimetype = row[3]
                size = row[4]
                extractedvars = (localpath, name, mimetype, size)

                # If file name at localpath is among the smaller set of files on disk that need to be
                # re-uploaded, replace the characters in localpath and name that might have caused
                # the upload to fail, and store cleaned values in variables newpath and newname.
                if os.path.exists(localpath):
                    newpath = swap_by_char(localpath)  # Try character by character
                    newpath = re.sub(namepattern, "_", newpath) # Catch any bad chars we missed
                    newname = swap_by_char(name)  # Try character by character
                    newname = re.sub(namepattern, "_", newname)  # Catch any bad chars we missed
                    logging.info('\tnewpath: ' + newpath)
                    logging.info('\tnewname: ' + newname)
                    newmetadata = [newpath, newname]

                else:
                    if row[0] == 'RH_PATH':   # Keep header row, modified to reflect changes to RH_PATH and RH_NAME
                        row[0] = row[0] + ' (MODIFIED)'
                        row[2] = row[2] + ' (MODIFIED)'
                        outputwriter.writerow(row)
                        logging.info('\tNot among working-files:  %s' % localpath)
                        continue
                    else:
                        continue

                # For those files that do need to be reuploaded, add newmetadata and other file metadata to new csv,
                # and reupload using newmetadata as path and filename
                filter_and_copy(myrow, extractedvars, newmetadata)


# Location of file 'all-metadata_REUPS.csv' passed in as argument
csvsrc = sys.argv[1]

read_mod_reup(csvsrc)
