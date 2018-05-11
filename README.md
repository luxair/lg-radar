## ADSB Flight Tracker

### Blacklist kernel modules

The receiver usb key will trigger kernel modules used to TV reception.
They must be disabled to allow rtl_adsb to work.

Create a file /etc/modprobe.d/adsb.conf

```
blacklist i2c_mux
blacklist rtl2832
blacklist rtl2832_sdr
blacklist dvb_core
blacklist dvb_usb_v2
blacklist dvb_usb_rtl28xxu
blacklist dvb_usb_v2
```

### Install rtl-sdr

#### On Ubuntu Linux

A standard package exists and can be installed:

```
> sudo apt install rtl-sdr
```

#### On other systems

See [rtl-sdr quick start guide](https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/)


### Install Python pre-requisites

```
pip install -r requirements.txt
```

### Online resources

* [The 1090MHz Riddle](http://mode-s.org/decode/adsb/introduction.html)
* [pyModeS - The Python Mode-S Decoder](https://github.com/junzis/pyModes)
* [World Aircraft DB](https://junzis.com/adb/)
* [rtl-sdr quick start guide](https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/)
* [rtl-sdr project project at osmocom.org](sdr.osmocom.org/trac/wiki/rtl-sdr)