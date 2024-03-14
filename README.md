# grclyify

grclyify wraps automatically generated python gnuradio flowgraphs, so you can override variables from the command line, and add a maximum runtime, without adding any code or modifying the generated flowgraph.

### example usage

```
$ grcc my_flowgraph.grc
$ grclyify.py my_flowgraph.py --set_somevar=1000 --runtime=10
```

### viewing possible overrides

```
$ grclyify.py my_flowgraph.py --help
```
