__author__ = 'rjaffe'
# python 3.4.5

import os, csv, sys, re, shutil

namepattern = re.compile('([^a-zA-Z0-9\/\.\-])')


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    print 'created dirs %s' % d


# Replace sys.argv[1] with 'all-metadata_REUPS.csv' when running in pyCharm
outputcsvfile = open('rewrite' + sys.argv[1], 'w', newline= '')
outputwriter = csv.writer(outputcsvfile, delimiter=",", quoting=csv.QUOTE_ALL)

# Read each row of metadata from Research Hub. Extract the RH_PATH,RH_NAME, RH_MIMETYPE and RH_SIZE to variables
# Replace sys.argv[1] with 'all-metadata_REUPS.csv' when running in pyCharm
with open(sys.argv[1], newline='') as csvfile:
    for row in csv.reader(csvfile, delimiter=","):
        originalbasepath = '/Company Home/Sites/bampfa/documentLibrary/Media'
        # Use '/Volumes/My Book/bampfa_Piction_bad-matches/working-files' or '...-test-set' when working locally
        originalpath = row[0].replace(originalbasepath, 'working-files')
        print 'originalpath: ' + originalpath
        originalname = row[2]
        # print 'original name: ' + originalname
        mimetype = row[3]
        # print 'mimetype: ' + mimetype
        size = row[4]
        # print 'size: ' + size
        # Now see if file named in row is actually among the smaller set of files on disk that need to be reuploaded.
        # For those files, get rid of the characters that might have caused the upload to fail
        if os.path.exists(originalpath):
            newpath = re.sub(namepattern, "_", originalpath)
            newname = re.sub(namepattern, "_", originalname)
            print 'newpath: ' + newpath
            print 'newname: ' + newname
            # Now copy the files on disk to a new file structure
            # But first... filter out files on disk that we don't want to reupload:
            # empty files (corrupted in or from Research Hub) and .DS_Store files.
            # Folders, like empty files, have a size of 0, and we must copy folders to keep the integrity of the tree,
            # so we can't just look for rows with size = 0.
            # NOTE that, for dev purposes, we copy all the files --
            # we pass the ones we want to a 'reupthese-files' directory and the others to 'dontreupthese-files'
            if (size is not '0' or mimetype == 'FOLDER') and originalname is not '.DS_Store':
                reupbasepath = 'reupthese-files/Company Home/Sites/bampfa/documentLibrary/Media'
                # Use '/Volumes/My_Book/bampfa_Piction_bad-matches/working-files' or '...-test-set' when working locally
                newpath = reupbasepath + newpath.replace('working-files', '')
                print "changed:    %s\t%s" % (originalpath, newpath)
                row[0] = newpath
                row[2] = newname
                outputwriter.writerow(row)
                # continue
                try:
                    # pass
                    ensure_dir(newpath)
                except:
                    print 'Could not ensure directory at %s' % newpath
                try:
                    shutil.copy(originalpath, newpath)
                    print 'reupload - copy succeeded %s' % newpath
                except:
                    print 'could not copy %s' % newpath
            else:
                dontreupbasepath = 'dontreupthese-files/Company Home/Sites/bampfa/documentLibrary/Media'
                newpath = dontreupbasepath + newpath.replace('working-files', '')
                print "changed:    %s\t%s" % (originalpath, newpath)
                row[0] = newpath
                row[2] = newname
                outputwriter.writerow(row)
                # continue
                try:
                    # pass
                    ensure_dir(newpath)
                except:
                    print 'Could not ensure directory at %s' % newpath
                try:
                    shutil.copy(originalpath, newpath)
                    print 'dont reupload - copy succeeded %s' % newpath
                except:
                    print 'could not copy %s' % newpath
        else:
            # pass
            print 'Not among working-files:  %s' % originalpath

