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

### randomize parameters

Extra set options are generated automatically, and the value is python eval'd to obtain a result.

```--randomize_interval <n>``` sets how often parameters are re-randomized.

```
$ grclyify.py my_flowgraph.py --rand_set_somevar="random.randint(0, 10)"
$ grclyify.py my_flowgraph.py --rand_set_somevar="random.choice([1, 2, 3, 4])"
```
