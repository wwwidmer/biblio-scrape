# Biblio-scrape


Quickly written, fast, and dirty way to scrape some images off a website and transport into a pdf

run simply with

`python3 main.py`

There is no config and no API keys.

Its smart enough to not re-download a file if it exists.
It runs on 10 threads so most books tested on were done within a minute but that can be edited.

Output

```
path/biblio-scrape/
	...
	schriften-messinglinein-usw/
		...
		1.jpg
		2.jpg
		...
		{n.jpg}
	schriften-messinglinein-usw.pdf
```

