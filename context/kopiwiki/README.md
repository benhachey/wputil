Run
===

Create and activate a virtual environment:
```
virtualenv ve
source ve/bin/activate
```

Install sklearn:
```
pip install -U numpy
pip install -U scipy
pip install -U scikit-learn
```

Set data path and run the extract script:
```
export KOPI_ROOT=/path/to/dir/containing/kopiwiki/download/dir
./extract.sh > context.txt 2> context.log
```
