# grclyify

grclyify wraps automatically generated python gnuradio flowgraphs, so you can override variables from the command line, and add a maximum runtime, without adding any code or modifying the generated flowgraph.

## example

1. generate gnuradio python script from flowgraph definition (.grc)

This included example flowgraph, sends a cosine signal to a UHD sink (both GUI and non GUI versions are supported).

```
$ grcc cosine.grc
<<< Welcome to GNU Radio Companion Compiler 3.10.7.0 >>>

Block paths:
	/usr/share/gnuradio/grc/blocks
	/usr/local/share/gnuradio/grc/blocks

>>> Loading: cosine.grc
>>> Generating: cosine.py

```
2. Run grclyify --help to identify out to reset any of the variables defined in the graph.

$ ./grclyify.py cosine.py --help
usage: grclyify.py [-h] [--runtime RUNTIME] [--randomize_interval RANDOMIZE_INTERVAL] [--set_freq SET_FREQ] [--rand_set_freq RAND_SET_FREQ] [--set_samp_rate SET_SAMP_RATE] [--rand_set_samp_rate RAND_SET_SAMP_RATE]
                   [--set_sig_freq SET_SIG_FREQ] [--rand_set_sig_freq RAND_SET_SIG_FREQ]
                   fg_file

positional arguments:
  fg_file               Path to flow graph python file

options:
  -h, --help            show this help message and exit
  --runtime RUNTIME     Runtime limit, in seconds
  --randomize_interval RANDOMIZE_INTERVAL
                        Time to re-randomize parameters, in seconds
  --set_freq SET_FREQ
  --rand_set_freq RAND_SET_FREQ
  --set_samp_rate SET_SAMP_RATE
  --rand_set_samp_rate RAND_SET_SAMP_RATE
  --set_sig_freq SET_SIG_FREQ
  --rand_set_sig_freq RAND_SET_SIG_FREQ
```

3. Run grclyify to run the graph for 10s, setting freq to 101e6, and randomizing sig_freq to 10 to 200 every 2s.

```
$ ./grclyify.py cosine.py --runtime 10 --set_freq=101e6 --rand_set_sig_freq="random.randint(10,200)" --randomize_interval=2
[INFO] [UHD] linux; GNU C++ version 11.2.0; Boost_107400; UHD_4.1.0.5-3
[INFO] [B200] Detected Device: B200mini
[INFO] [B200] Operating over USB 3.
[INFO] [B200] Initialize CODEC control...
[INFO] [B200] Initialize Radio control...
[INFO] [B200] Performing register loopback test...
[INFO] [B200] Register loopback test passed
[INFO] [B200] Setting master clock rate selection to 'automatic'.
[INFO] [B200] Asking for clock rate 16.000000 MHz...
[INFO] [B200] Actually got clock rate 16.000000 MHz.
[INFO] [B200] Asking for clock rate 32.000000 MHz...
[INFO] [B200] Actually got clock rate 32.000000 MHz.
[INFO] [MULTI_USRP]     1) catch time transition at pps edge
[INFO] [MULTI_USRP]     2) set times next pps (synchronously)
overriding freq to 101e6
will exit in 10.0s
Press Enter to quit: sig_freq -> 61
sig_freq -> 116
sig_freq -> 109
sig_freq -> 102
sig_freq -> 146
exiting
```

