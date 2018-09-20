# Analogia

## Requirements
* Python 3.6
* Install these
```
pip install --upgrade --user git+git://github.com/zhijing-jin/efficiency.git
# many other packages as mentioned in code/parser
```


* CoreNLP Package
  * Download a java package onto the server, [Corenlp](https://stanfordnlp.github.io/CoreNLP/download.html)
  * Then install the [python api](https://github.com/smilli/py-corenlp)
  * 大致就是先download java的package，然后用python的api跑一下，其中需要开server的port 9000。
* Install NLTK with `sudo pip install -U nltk`

## Code
* Play with CoreNLP parser by
```
cd code/parse 
python corenlp.py
```

* Run Story_Matching examples by

```
cd code/parse 
python start.py -file success
```
