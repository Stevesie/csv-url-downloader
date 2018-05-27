import requests
import csv
import io
import os
import errno
import pathlib

from urllib.parse import urlparse
from time import sleep

from argparse import ArgumentParser

DEFAULT_DESTINATION = '.'

def execute(
    source_csv, 
    url_columns, 
    destination=DEFAULT_DESTINATION, 
    file_name_column=None, 
    identity_column=None,
    ssl_insecure=False):

    do_ssl_verification = not ssl_insecure

    source_url = urlparse(source_csv)
    if source_url.scheme in ['http', 'https']:
        print('Downloading {}'.format(source_url.geturl()))
        r = requests.get(source_url.geturl(), verify=do_ssl_verification)
        csv_content = r.text
        if r.status_code != 200:
            raise Exception('Could not download CSV, received response code {} with body: {}'.format(r.status_code, csv_content))

    elif source_url.path:
        with open(source_csv) as f:
            csv_content = f.read()
    else:
        raise Exception('Resource type {} is not supported.'.format(source_csv))

    reader = csv.reader(io.StringIO(csv_content))
    headers = next(reader)
    for row in reader:
        obj = dict(zip(headers, row))

        if url_columns is None:
            url_columns = [k for k, v in obj.items() if v.startswith('http')]

        for url_column in url_columns:
            download_url = obj[url_column]
            if download_url:
                if file_name_column is not None:
                    file_name = obj[file_name_column]
                    file_suffix = pathlib.Path(urlparse(download_url).path).suffix
                    if file_suffix:
                        file_name += file_suffix
                else:
                    file_name = os.path.basename(urlparse(download_url).path)

                desintation_dir_fragments = [destination]

                if identity_column:
                    desintation_dir_fragments.append(obj[identity_column])

                desintation_dir_fragments.append(url_column)
                desintation_dir = os.path.join(*desintation_dir_fragments)

                try:
                    os.makedirs(desintation_dir)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise e

                destination_file_path = os.path.join(desintation_dir, file_name)

                print('Downloading {} -> {}'.format(download_url, destination_file_path))

                with open(destination_file_path, 'wb') as f:
                    r = requests.get(download_url, verify=do_ssl_verification)
                    f.write(r.content)

                sleep(0.5) # be nice - don't hammer remote service

def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('source_csv', type=str)
    parser.add_argument('-c', '--url_columns', type=str, action='append', required=False)
    parser.add_argument('-d', '--destination', type=str, required=False, default=DEFAULT_DESTINATION)
    parser.add_argument('-f', '--file_name_column', type=str, required=False)
    parser.add_argument('-i', '--identity_column', type=str, required=False)
    parser.add_argument('-k', '--ssl_insecure', action='store_true', default=False, required=False)
    return parser

def run_command_line():
    parser = arg_parser()
    args = vars(parser.parse_args())
    execute(**args)

if __name__ == '__main__':
    run_command_line()
