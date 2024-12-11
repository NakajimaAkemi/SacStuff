# Setup commands 
This readme assumes you have a functioning setup for Omnetpp and we're working in the `samples/queuenet` directory.
```bash
. setenv
```

## Generate the .ini file and the runfile
After creating our .ned file we run these commands.
```bash
update_template.py
make_runfile.py -f MM1.ini
make -j $(nproc) -f runfile
```

## Generate the `.db` file
After setting up the config***.json file we generate our sqlite db.
```bash
parse_data.py -c configMM1.json -d MM1.db -r results/MM1_rho*.sca
analyze_data.py -d MM1.db -c configMM1.json
```
