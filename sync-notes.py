import os
import sys
import psutil
import shutil

USER_PROFILE_PATH = os.environ["USERPROFILE"]
SOURCE_PATH = USER_PROFILE_PATH + "\\Documents\\Simple Sticky Notes\\"
BACKUP_PATH = USER_PROFILE_PATH + "\\Documents\\Synced Notes\\"
FILE_NAME = "Notes.db"
APP_PATH = "C:\\Program Files (x86)\\Simnet\\Simple Sticky Notes\\"
APP_EXE_NAME = "ssn.exe"


def kill_app(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            proc.kill()


def save():
    print("Saving...")
    try:
        # If "Synced Notes" directory does not exist, create it
        if not os.path.exists(BACKUP_PATH):
            os.makedirs(BACKUP_PATH)

        # Copy "Notes.db" file from SOURCE_PATH directory to BACKUP_PATH directory
        shutil.copy2(SOURCE_PATH + FILE_NAME, BACKUP_PATH + FILE_NAME)
        print("Save successful!")
    except IOError as e:
        print("Save failed: " + e)


def load():
    print("Loading...")
    try:
        # Close the Simple Sticky Notes application
        os.system("taskkill /f /im " + APP_EXE_NAME)
        # Backup: Copy and rename the "Notes.db" file in SOURCE_PATH directory to "Notes.db.bak"
        shutil.copy2(SOURCE_PATH + FILE_NAME, SOURCE_PATH + FILE_NAME + ".bak")
        # Copy "Notes.db" file from BACKUP_PATH directory to SOURCE_PATH directory
        shutil.copy2(BACKUP_PATH + FILE_NAME, SOURCE_PATH + FILE_NAME)
        # Open the Simple Sticky Notes application again
        os.startfile(APP_PATH + APP_EXE_NAME)
        print("Load successful!")
    except IOError as e:
        print("Load failed: " + e)


def restore_backup():
    print("Restoring backup...")
    try:
        # Close the Simple Sticky Notes application
        os.system("taskkill /f /im " + APP_EXE_NAME)
        # Copy and rename the "Notes.db.bak" file in SOURCE_PATH directory to "Notes.db"
        shutil.copy2(SOURCE_PATH + FILE_NAME + ".bak", SOURCE_PATH + FILE_NAME)
        # Open the Simple Sticky Notes application again
        os.startfile(APP_PATH + APP_EXE_NAME)
        print("Backup restore successful!")
    except IOError as e:
        print("Backup restore failed: " + e)


# Receive parameter from command line; "save", "load" or "restore" and call the appropriate function
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "save":
            save()
        elif sys.argv[1] == "load":
            load()
        elif sys.argv[1] == "restore":
            restore_backup()
        else:
            print("Invalid parameter. Please use 'save', 'load' or 'restore'")
    else:
        print("No parameter received. Please use 'save', 'load' or 'restore'")
