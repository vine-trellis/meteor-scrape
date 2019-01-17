import urllib.request

url = "https://n5eil01u.ecs.nsidc.org/DP5/MOST/MOD10A1.006/2016.04.04/MOD10A1.A2016095.h23v06.006.2016104071619.hdf"

file_name = url.split('/')[-1]
u = urllib.request.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print("Downloading: {} Bytes: {}".format(file_name, file_size))

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (
        file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print(status)

f.close()
