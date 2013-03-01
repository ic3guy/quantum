import experiment

#filenames = ['heater-new']
filenames = ['bounceBallsin-new5c']

#globals() modifies the global level

for file_name in filenames:             
    cur_exp = experiment.Experiment(file_name)        
    #execfile('quantum6.py',globals())

print cur_exp.system_def

    
#for i in *; do mv "$i" "$i".tptp; done
#sed -i 's/PX<3.14 & PX>-3.14 & PX<0/S^2+C^2=1/g' ./*
#sed -i 's/PX,/S,C,/g' ./*

