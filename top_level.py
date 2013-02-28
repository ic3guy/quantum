#filenames = ['simplePendulum4.py','simplePendulum3.py','simplePendulum2.py','simplePendulum4b.py','simplePendulum3b.py','simplePendulum2b.py']
#filenames = ['simplePendulum','simplePendulumbad','simplePendulum1','simplePendulum1b']
#filenames = ['simplePendulum4.py']
#filenames = ['bounceBallsin2a','bounceBallsin2b','bounceBallsin','bounceBallsinb']
#filenames = ['bounceBallsin2a']

#filenames = ['simplePendulum', 'simplePendulum2', 'simplePendulum3', 'simplePendulum4', 'bounceBallsin', 'bounceBallsin2a']

#filenames = ['simplePendulum-new']
#filenames = ['bounceBall-2states']
#filenames = ['bounceBall-work']
filenames = ['heater-new']
#filenames = ['bounceBall-plat2b']

#filenames = ['bounceBallsin-new']
#filenames = ['bounceBallsin-new5']


#globals() modifies the global level

for file_name in filenames:             
    exp_name = file_name + '.py'        
    execfile('quantum6.py',globals())
        
#for i in *; do mv "$i" "$i".tptp; done
#sed -i 's/PX<3.14 & PX>-3.14 & PX<0/S^2+C^2=1/g' ./*
#sed -i 's/PX,/S,C,/g' ./*

