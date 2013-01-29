#filenames = ['simplePendulum4.py','simplePendulum3.py','simplePendulum2.py','simplePendulum4b.py','simplePendulum3b.py','simplePendulum2b.py']
filenames = ['simplePendulum','simplePendulumbad','simplePendulum1','simplePendulum1b']
#filenames = ['simplePendulum4.py']
#filenames = ['bounceBallsin2a.py','bounceBallsin2b.py','bounceBallsin.py','bounceBallsinb.py']
#filenames = ['bounceBallsin.py']

for file_name in filenames:
    exp_name = file_name + '.py'
    #execfile('/Users/will/Research/quantum/quantum4-log.py')
    execfile('quantum5.py')
