from pykeepass import PyKeePass, create_database


def createNewFile(path:str,name:str,password, key_file=None):
    """Function for creation new KDBX file"""

    create_database(path, password,keyfile=key_file)
    print('Database created.')

def openDatabase(path:str,password=None,keyfile=None):
    """Function for open database"""
    open_db = PyKeePass(filename=path,password=password,keyfile=keyfile)
    return open_db

def getGroups(keepassExam:PyKeePass):
    """Returning all groups"""
    return keepassExam.groups

def entriesByGroup(keepassExam:PyKeePass, group_name):
    """Return all entries in group"""
    group = keepassExam.find_groups_by_name(group_name)[0]
    return group.entries

def groupByName(keepassExam:PyKeePass, group_name):
    group = keepassExam.find_groups_by_name(group_name)[0]
    return group

def addNewGroup(keepassExam:PyKeePass, title, notes):
    keepassExam.add_group(destination_group=keepassExam.root_group, group_name=title, notes=notes)
    keepassExam.save()

def addNewEntry(keepassExam:PyKeePass, title, link, username, password, notes, group):
    entry = keepassExam.add_entry(group, title, username,password, link, notes)
    keepassExam.save()
    return entry

def removeEntry(keepassExam:PyKeePass, entry):
    keepassExam.delete_entry(entry)
    keepassExam.save()

def changeParams(keepassExam:PyKeePass, entry, title, link, username, password, notes):
    entry.title = title
    entry.url = link
    entry.url = link
    entry.username = username
    entry.password = password
    entry.notes = notes
    keepassExam.save()