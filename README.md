<!-- Lien vers le dépot https://etulab.univ-amu.fr/p21205661/sae203  -->
## Name
[RSS Feed Aggregator](https://etulab.univ-amu.fr/p21205661/sae203)

## Description
This python program can fetch multiple rss flow (eg. rss.xml) from multiple urls and aggregate them in one place into an html clean website.

## Installation
1. open "config_example.yaml" file for an exemple of configuration:

| Field | Explanation |
| ------ | ------ |
| sources: | A yaml list of your urls (see "config_example.yaml") |
| rss-name: | The name of your rss flow (if you've set rss.xml here and http://serveur1.net/ in sources your file must be in http://serveur1.net/rss.xml) |
| destination: | The output where the html/css/js files will be created |
| tri-chrono: | A chronological sorting feature, if it's true you will have the latest events first |

You can edit the lines with what you want, then if you don't want to specify the config file when runnning aggreg.py you need to rename the file to "config.yaml" and move it to /etc/config.yaml, it must be exactly "config.yaml" in /etc/config.yaml otherwise it won't detect your config.

An other way you can set up the config file is just by renaming it with what you want and specify it in the terminal like so: python3 aggreg.py myconfig.yaml

Note that each item of your RSS feed must contain a title, a category (MINOR,MAJOR or CRITICAL for color support), a publication date, a link and a description in order for it to work.

## Usage
1. run aggreg.py with "python3 ./aggreg.py" or "python3 ./aggreg.py customconfig.yaml" if you want a custom config in a custom dir.

2. Done! Open your website

## Troubleshooting
 If it doesn't work:
	<br>&ensp;&ensp;&ensp;&ensp;- check if "config.yaml" is in /etc/config.yaml in the case you use the default config file"
	<br>&ensp;&ensp;&ensp;&ensp;- check if you've made a mistake when writing your config

 If you have a permission denied when creating the website just delete all the files created (script.js,index.html...) in the destination folder


## License

![alt text](https://upload.wikimedia.org/wikipedia/commons/1/12/Cc-by-nc-sa_icon.svg)
