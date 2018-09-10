#!/usr/bin/env python
import ephem

Dawodang=ephem.Observer()
Dawodang.lat='25.652939'
Dawodang.lon='106.856594'
Dawodang.horizon='-18' # Astronomical twilight uses the value -18 degrees

Dawodang.date= '2017/12/10'

src = ephem.FixedBody()
src._ra = '09:22:14.022'  # J2000
src._dec = '+06:38:23.3'      # J2000

#M87  12:30:49.4  +12:23:28
#G192.54-11.56     82.868958    12.256222
#J1837+1221    18:37:07.1  +12:21:54.0
#J1916+1225    19:16:20.0  +12:25:53.9


src.compute()
trise=Dawodang.previous_rising(src)
print 'previous rise'
print src.alt,src.az,ephem.localtime(trise)
ttrans=Dawodang.next_transit(src)
print 'next transit'
print src.alt,src.az,ephem.localtime(ttrans)
tset=Dawodang.next_setting(src)
print 'next setting'
print src.alt,src.az,ephem.localtime(tset)
print src.ra,src.dec
