import codecs


def readAllFiles():
    with codecs.open('config/recentFiles.cfg', 'r', 'utf-8') as file:
        recentFiles = file.read().split('\n')
    if recentFiles[0] == '' and len(recentFiles) == 1:
        recentFiles = None
    else:
        if recentFiles[0] == '':
            del(recentFiles[0])

    return recentFiles


def addNewFile(name):
    recentFiles = readAllFiles()
    if not recentFiles is None and name in recentFiles:
        return
    else:
        with codecs.open('config/recentFiles.cfg', 'a', 'utf-8') as file:
            file.write('\n'+name)
            print('Added new file')
