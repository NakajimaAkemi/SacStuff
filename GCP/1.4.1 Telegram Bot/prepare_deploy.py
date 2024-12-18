#!/usr/bin/python3
import re
import os

fin_name='app_template.yaml'
fout_name='app.yaml'
with open(fin_name, 'r') as fin:
    with open(fout_name, 'wt') as fout:
        for l in fin.readlines():
            #l = l.strip('\n')
            m = re.search('\\$\\{(?P<var>\\w+)\\}', l)
            if m:
                var=m.group('var')
                val=os.environ[var] if (var in os.environ.keys()) else ''
                l=re.sub('\\$\\{\\w+\\}', val, l)
            fout.write(l)
