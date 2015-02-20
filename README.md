# xmlE2SC3
### Convert ElarmS modules E2 and DM event xml to SeisComP3 event xml.
Created by Ran Novitsky Nof (http://ran.rnof.info), 2015 @ BSL
#### DEPENDENCIES:
Python modules:
* datetime
* argparse
* sys
* os
* xml

#### USAGE:
<pre>
E2SC.py [-h] [-o OutXML] [-i InXML [InXML ...]] [-t]

optional arguments:
  -h, --help            show this help message and exit
  -o OutXML             Output xml file (Seiscomp3).
  -i InXML [InXML ...]  input xml file(s) (Elarms).
  -t                    Test mode (ignors input parameter if applicable)
</pre>

Seiscomp3 xml can be fed to Seicomp3 database using scdb.  
_Examples:_
```
   E2SC.py -i events_20150214.log -o SCXML   
   scdb -i SCXML -d mysql://sysop:sysop@localhost/seiscomp3  
```   
or:
```
   cat [ELARMSXMLFILE] | E2SC.py | scdb -i - -d mysql://sysop:sysop@localhost/seiscomp3  
```   
or:
```
   E2SC.py -i events_*.log | scdb -i - -d mysql://sysop:sysop@localhost/seiscomp3  
```

#### LICENSE:
```
Copyright (C) by Ran Novitsky Nof                                            
                                                                              
E2SC.py is free software: you can redistribute it and/or modify              
it under the terms of the GNU Lesser General Public License as published by  
the Free Software Foundation, either version 3 of the License, or            
(at your option) any later version.                                          
                                                                                 
This program is distributed in the hope that it will be useful,              
but WITHOUT ANY WARRANTY; without even the implied warranty of               
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                
GNU Lesser General Public License for more details.                          

You should have received a copy of the GNU Lesser General Public License     
along with this program.  If not, see <http://www.gnu.org/licenses/>. 
```
