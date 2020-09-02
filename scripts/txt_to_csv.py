import os


def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        change_filename = full_filename.replace('csv', 'txt')

        os.rename(full_filename, change_filename)
        print(change_filename)


def run():
    search('C:/Users/daeun/Desktop/openAPI/202007_주소DB_변동분')