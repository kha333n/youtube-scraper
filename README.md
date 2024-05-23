# YouTube Scraper and Player

### Scrap the YouTube video links from a given YouTube channel and play the video in the browser.

Better to use Virtual Machines to run this code, so that IP and system change and YouTube can register it as actual
traffic.
Running on your own system may not be beneficial as YouTube may consider it as watching own videos and don't count it.

### Prerequisites

Python 3.2

### Installing

```
pip install -r requirements.txt
```

### Running the code

For gathering the video links from the YouTube channel, run the following command:

```
python3 scraper.py
```

For playing the video in the browser, run the following command:

```
python3 player.py
```

Update .py files with your own data.
in scraper.py, update the channel url with your own channel url. videos page should end in /videos

in player.py, update the file name with the text file name output from scraper.py

### Authors

* **[kha333n](github.com/kha333n)**