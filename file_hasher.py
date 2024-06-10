"""file_hasher.py: Hash local or web files and download files from the web"""
import argparse
import hashlib
import urllib.request as request
from pathlib import Path
from tqdm import tqdm

EXAMPLES = '''
Examples:
---------
python file_hasher.py -f \\temp\\evil.exe -a sha256
python file_hasher.py -u <url> -a sha1
python file_hasher.py -d <url>
'''


class Hasher:
    """Hash local or web files and download files from the web"""
    HASH_OPTIONS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha256': hashlib.sha256,
    }

    def __init__(self, algorithm, file=None, url=None, download=None):
        """initialize hasher object
        Args:
            algorithm (str): hash algorithm
            file (str): file path
            url (str): url of file
            download (str): url to download file
        """
        self.algorithm = algorithm
        self.file = Path(file) if file else None
        self.url = url
        self.download = download
        self.hasher = self.HASH_OPTIONS[self.algorithm]()
        
    def _read_chunks(self, fh):
        """read file in chunks"""
        for chunk in iter(lambda: fh.read(4096), b''):
            yield chunk

    def get_filehash(self):
        """hash file on disk"""
        if not self.file.exists():
            print(f'File not found: {self.file}')
            return
        try:
            with self.file.open('rb') as fh:
                for chunk in self._read_chunks(fh):
                    self.hasher.update(chunk)

            print(f'\n{self.algorithm}: {self.hasher.hexdigest()}\n')
        except Exception as e:
            print(f'Error getting file hash: {e}')

    def get_urlhash(self):
        """hash remote file from url"""
        if not self.url:
            print('No URL provided.')
            return
        try:
            req = request.Request(self.url)
            with request.urlopen(req) as response:

                for chunk in self._read_chunks(response):
                    self.hasher.update(chunk)

            print(f'\n{self.url} \n{self.algorithm}: {self.hasher.hexdigest()}\n')
        except Exception as e:
            print(f'Error hashing file from URL: {e}')
        
    def downloader(self):
        """download file from web"""
        out = Path.cwd() / f"{self.download.split('/')[-1]}"

        try:
            req = request.Request(self.download)
            with request.urlopen(req) as response:
                # get content length
                content_length = int(response.headers['Content-Length'])
                total = int(content_length) if content_length > 0 else None

                with out.open('wb') as fh:
                    # create progress bar
                    progress = tqdm(total=total, unit='B', unit_scale=True)

                    for chunk in self._read_chunks(response):
                        fh.write(chunk)
                        progress.update(len(chunk))
                    # close progress bar
                    progress.close()
            print(f'\nDownloaded: {out}\n')
        except Exception as e:
            print(f'Error downloading file: {e}')

def get_args():
    parser = argparse.ArgumentParser(description='Hash local files or web files', epilog=EXAMPLES,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--file', help='Full path to file on disk')
    parser.add_argument('-u', '--url', help='URL of file')
    parser.add_argument('-d', '--download', help='Download remote file from URL')

    hashers = parser.add_argument_group('hash algorithms')
    hashers.add_argument('-a', '--algorithm', choices=['md5', 'sha1', 'sha256'], help='Hash algorithm (default is md5)')
    return parser.parse_args()
    

def main():
    args = get_args()
    
    algorithm = args.algorithm if args.algorithm else 'md5'

    if args.file and Path(args.file).exists():
        hasher = Hasher(algorithm, file=args.file)
        hasher.get_filehash()

    elif args.url:
        hasher = Hasher(algorithm, url=args.url)
        hasher.get_urlhash()
    elif args.download:
        hasher = Hasher(algorithm, download=args.download)
        hasher.downloader()

if __name__ == '__main__':
    main()
