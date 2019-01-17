import os

INPUT_DATA_PATH_ = 'input/'


def get_file_name():
    pass


def main():
    with open('urls.txt', 'r') as urls:
        url_list = urls.read().split('\n')

    obj = {}
    for url in url_list:
        url = url.split('/')
        date = url[-2]
        filename = url[-1]
        if date not in obj.keys():
            obj[date] = []
        obj[date].append(filename)
    print(obj)
    make_folders(obj)
    copy_data(obj)


def make_folders(obj):
    for date in obj.keys():
        try:
            os.makedirs(date.split('.')[0]
                        + '/'
                        + date.split('.')[1]
                        + '/'
                        + date.split('.')[2]
                        + '/')
        except OSError:
            pass


def copy_data(obj):
    for date in obj.keys():
        for filename in obj[date]:
            os.rename(INPUT_DATA_PATH_ + filename,
                      date.split('.')[0]
                      + '/'
                        + date.split('.')[1]
                        + '/'
                        + date.split('.')[2]
                        + '/'
                        + filename)


if __name__ == '__main__':
    main()
