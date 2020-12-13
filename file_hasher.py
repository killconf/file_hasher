import urllib.request as request
from pathlib import Path
import hashlib
import wget
import argparse

example = '''
python file_hasher.py -f \\temp\\evil.exe --sha256
python file_hasher.py -u <url> --sha1
python file_hasher.py -d <url>
'''

hash_options = []


class Hasher:

    def __init__(self, options, file=None, url=None, download=None):
        self.options = options
        if file:
            self.file = Path(file)
        self.url = url
        self.download = download

        if len(self.options) == 0:
            self.algo = 'md5'
            self.hasher = hashlib.md5()
        elif self.options[0] == 'md5':
            self.algo = 'md5'
            self.hasher = hashlib.md5()
        elif self.options[0] == 'sha1':
            self.algo = 'sha1'
            self.hasher = hashlib.sha1()
        elif self.options[0] == 'sha256':
            self.algo = 'sha256'
            self.hasher = hashlib.sha256()

    def get_filehash(self):
        """hash file on disk"""
        try:
            with self.file.open('rb') as fh:
                for chunk in iter(lambda: fh.read(4096), b''):
                    self.hasher.update(chunk)

            print(f'\n{self.algo}: {self.hasher.hexdigest()}')
        except Exception as e:
            print(f'Something went wrong: {e}')

    def get_urlhash(self):
        """hash remote file from url"""
        try:
            req = request.Request(self.url)
        except Exception as e:
            print(f'Error requesting URL: {e}')

        else:
            try:
                with request.urlopen(req) as response:
                    for chunk in iter(lambda: response.read(4096), b''):
                        self.hasher.update(chunk)
                print(f'\n{self.url} \n{self.algo}: {self.hasher.hexdigest()}')
            except Exception as e:
                print(f'\nSomething went wrong: {e}')

    def write_remote(self):
        """download remote file to disk"""
        out = Path.home() / 'Downloads'

        try:
            print(f'\nDownloading: {self.download}')
            wget.download(self.download, str(out))
            print('\n\nFile written to: {}'.format(str(out) + '\\' + self.download.split('/')[-1]))
        except Exception as e:
            exit(f'\nwget error: {e}')


def main():
    h = Hasher(hash_options, args.file, args.url, args.download)
    if args.file:
        h.get_filehash()
    if args.url:
        h.get_urlhash()
    if args.download:
        h.write_remote()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hash local files or web files', epilog=example,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--file', help='Full path to file on disk')
    parser.add_argument('-u', '--url', help='URL of file')
    parser.add_argument('-d', '--download', help='Download remote file from URL')

    hashers = parser.add_argument_group('hash algorithms')
    hashers.add_argument('--md5', action='store_true', help='Use md5 hash algorithm (default)')
    hashers.add_argument('--sha1', action='store_true', help='Use sha1 hash algorithm')
    hashers.add_argument('--sha256', action='store_true', help='Use sha256 hash algorithm')

    args = parser.parse_args()

    downloads = Path.home() / 'Downloads'
    for arg in vars(args):
        if getattr(args, arg):
            if arg in ['md5', 'sha1', 'sha256']:
                hash_options.append(arg)

    main()
