# file_hasher
hash local or remote files. download remote files.

## example usage

hash file on disk

`file_hasher.py -f \temp\evil.exe --sha1`

hash remote file

`file_hasher.py -u file_hasher.py -u http://www.example.com/images/somefile.jpg --sha256`

download file

`file_hasher.py -d http://www.example.com/images/somefile.jpg`
