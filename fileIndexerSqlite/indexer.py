import os, sys, sqlite3, time

# make file index and save to sqlite ((empty) folders are not part of index)

def main():
    connection = sqlite3.connect("fileindex.db")
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE IF EXISTS filetable;""")
    cursor.execute("""CREATE TABLE filetable(filename VARCHAR(255), path VARCHAR(255), filesize INTEGER, filedate DATE);""")

    for subdir, dirs, files in os.walk(rootdir):
        for filename in files:
            print(os.path.join(subdir, filename))
            try:
                filedate=time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(os.path.getmtime(os.path.join(subdir, filename))))
                cursor.execute("""INSERT INTO filetable VALUES (?,?,?,?);""",(filename,os.path.join(subdir, filename),os.path.getsize(os.path.join(subdir, filename)),filedate))
            except:
                cursor.execute("""INSERT INTO filetable VALUES (?,?,NULL,NULL);""", (
                filename, os.path.join(subdir, filename)))
            #if filename.endswith(".asm") or filename.endswith(".py"):
                # print(os.path.join(directory, filename))
            #    continue

    connection.commit()
    connection.close()

if(len(sys.argv) > 1):
    rootdir = sys.argv[1]
    main()
else:
    print("Not enough arguments (add path)")