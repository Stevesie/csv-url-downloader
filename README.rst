# CSV URL Downloader

Download content from URLs in CSVs.

**Under Development - BE CAREFUL**

I wrote this in an hour and there are probably issues I don't know about yet. Use at your own risk!

Please [contact me](https://stevesie.com/contact) if something bad happens or you'd like to contribute.

## Installation

Make sure you have Python 3 installed please, then you just need to download the [Python Script](https://raw.githubusercontent.com/Stevesie/csv-url-downloader/master/csv_url_downloader/csv_url_downloader.py) somewhere until we make this a tool you can actually install.

Download the file to your current directory:

`curl https://raw.githubusercontent.com/Stevesie/csv-url-downloader/master/csv_url_downloader/csv_url_downloader.py > csv_url_downloader.py`

## Usage

Suppose we have a CSV file laying around our computer in `~/Desktop/friends.csv` that looks like this (yes, suppose we have a CSV to keep track of our friends):

Suppose the CSV looks like this:

| Name          | Photo         | Video  |
|:------------- |:-------------|:-----|
| Aaron      | https://site.com/photo1.jpg | https://site.com/video1.mp4 |
| Betty      | https://site.com/photo2.jpg | https://site.com/video2.mp4 |
| Claire      | https://site.com/photo3.jpg | https://site.com/video3.mp4 |

### Default Behavior

Let's say we just want to download all of the linked content from the CSV, we can just run this (it will automatically detect links if they begin with `http`):

`python csv_url_downloader.py ~/friends.csv`

This will write the following files to our current directory (creating directories as needed):

- `Photo/`
    - `photo1.jpg`
    - `photo2.jpg`
    - `photo3.jpg`
- `Video/`
    - `video1.mp4`
    - `video2.mp4`
    - `video3.mp4`

### Download Columns

Now, let's suppose that downloading videos is creepy (but images are OK), so we'd like to stop downloading them. Fortunately we can whitelist the columns from our CSV to download with the `-c` or `--url_columns` flag:

`python csv_url_downloader.py -c Photo ~/friends.csv`

Will now only download:

- `Photo/`
    - `photo1.jpg`
    - `photo2.jpg`
    - `photo3.jpg`

You can specify as many columns as you want, e.g. running the following would be equivalent to the first exmaple where we downloaded both columns:

`python csv_url_downloader.py -c Photo -c Video ~/friends.csv`

### Destination

Specify the directory to write the files with the `-d` or `--destination` flag. E.g. the following will write the files to `~/Desktop` regardless of where you run the script from:

`python csv_url_downloader.py -d ~/Desktop ~/friends.csv`

You can reuse the same destination over and over, and the script will keep appending to your destination.

### File Names

As wonderful as `photo1.jpg` sounds, it's not quite the same as our friend's name and it would be nice if we could save the files based on their names.

Specify the `-f` or `--file_name_column` flag to name each file after the respective value in this column. For eample, if we want our file names to match our friend's name, we would run:

`python csv_url_downloader.py -f Name ~/friends.csv`

And we would then save:

- `Photo/`
    - `Aaron.jpg`
    - `Betty.jpg`
    - `Claire.jpg`
- `Video/`
    - `Aaron.mp4`
    - `Betty.mp4`
    - `Claire.mp4`

## Advanced

Let's make things more interesting, and assume our CSV now contains daily "stories" of what our friends are up to.

This means that instead of having one row per friend, we now have one row per friend _and_ story date, so `Name` is no longer unique amongst the entire table.

| Name          | Photo         | Video  | Date |
|:------------- |:-------------|:-----|:---|
| Aaron      | https://site.com/photo1.jpg | https://site.com/video1.mp4 | 2018-01-01 |
| Betty      | https://site.com/photo2.jpg | https://site.com/video2.mp4 | 2018-01-01 |
| Claire      | https://site.com/photo3.jpg | https://site.com/video3.mp4 | 2018-01-01 |
| Aaron      | https://site.com/photo4.jpg | https://site.com/video4.mp4 | 2018-01-02 |
| Betty      | https://site.com/photo4.jpg | https://site.com/video5.mp4 | 2018-01-02 |
| Claire      | https://site.com/photo5.jpg | https://site.com/video6.mp4 | 2018-01-02 |

We'd like to still organize this content by name while also keeping multiple photos and videos per person (over time).

Fortunately we can use the `-i` or `--identity_column` flag to tell our script which column identifies users, and then this will build a top-level directory for which to write the files.

Now if we change `--file_name_column` flag to use the `Date` column, we can run this on the new CSV:

`python csv_url_downloader.py -f Date -i Name ~/friends.csv`

This will write the following to our local computer now, all nicely organized:

- `Aaron/`
    - `Photo/`
        - `2018-01-01.jpg`
        - `2018-01-02.jpg`
    - `Video/`
        - `2018-01-01.mp4`
        - `2018-01-02.mp4`
- `Betty/`
    - `Photo/`
        - `2018-01-01.jpg`
        - `2018-01-02.jpg`
    - `Video/`
        - `2018-01-01.mp4`
        - `2018-01-02.mp4`
- `Claire/`
    - `Photo/`
        - `2018-01-01.jpg`
        - `2018-01-02.jpg`
    - `Video/`
        - `2018-01-01.mp4`
        - `2018-01-02.mp4`
