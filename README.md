# file_hasher
file_hasher is a Python script for hashing local files and hashing/downloading files hosted on a web server via HTTP.

## Requirements
Python 3.6 or higher and tqdm
```bash
pip install -r requirements.txt
```
## Features
- Hash local files with your choice of algorithm (md5, sha1, sha256)
- Hash files hosted on a web server without downloading
- Download remote files via HTTP

## example usage

hash file on disk

`file_hasher.py -f \temp\evil.exe -a sha1`

hash remote file

`file_hasher.py -u http://www.example.com/images/somefile.jpg -a sha256`

download remote file

`file_hasher.py -d http://www.example.com/images/somefile.jpg`

## License
```
MIT License

Copyright (c) 2024 killconf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.