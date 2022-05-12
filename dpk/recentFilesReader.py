import codecs, os.path

def rewriteConfigFile(files):
    with codecs.open('config/recentFiles.cfg', 'w', 'utf-8') as file:
        writeText = '\n'.join(files)
        file.write(writeText)

def readAllFiles():
    with codecs.open('config/recentFiles.cfg', 'r', 'utf-8') as file:
        recentFiles = file.read().split('\n')
    if recentFiles[0] == '' and len(recentFiles) == 1:
        recentFiles = None
        return recentFiles
    else:
        if recentFiles[0] == '':
            del(recentFiles[0])
    for index,recentFile in enumerate(recentFiles):
        if not os.path.exists(recentFile):
            del(recentFiles[index])
            rewriteConfigFile(recentFiles)


    return recentFiles


def addNewFile(name):
    recentFiles = readAllFiles()
    if not recentFiles is None and name in recentFiles:
        return
    else:
        with codecs.open('config/recentFiles.cfg', 'a', 'utf-8') as file:
            file.write('\n'+name)
            print('Added new file')
