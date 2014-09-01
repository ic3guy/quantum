***********************************************************
QUANTUM - Qualitative Abstractions of Non-Polynomial Models
***********************************************************

1 Sep 2014

This is a research tool for the automatic qualitative abstraction of hybrid
dynamical systems that contain transcendental functions.

You will need at a minimum to have installed MetiTarski (with
Poly/ML), along with an appropriate decision procedure (QEPCAD,
Mathematica or Z3). Please contact me if you need help with
installation of MetiTarski.

William Denman - william.denman@gmail.com

***

To run QUANTUM, use your favourite python interpreter to run top_level.py

#> python -i top_level.py

At this point if you are missing any required python modules, you will get import errors. See the install file for a list of dependencies.

There are several benchmark problems in the 'examples' directory. I recommend you try 'heater-new.py' to ensure everything is working properly. To create an abstraction of that file invoke the 'abstract' command, with the name of the file in the examples directory, not including the file extension.

Quantum V0.1
(QUANTUM) > abstract heater-new

Once abstraction is complete, a finite state transition system will be output on
the screen in textual form. To generate a dot png file from this description use
the 'g' or 'graphiz' command.

(QUANTUM) > graphiz

This will output a file called 'test.png' in the main QUANTUM directory.

A sub-directory named 'experiments' will be created after running the
experiments that will contain proved and unproved Metitarski tptp files that
have been generated during the qualitative abstraction process.

A text file named 'log.txt' will be generated containing timing statistics as
well as various quantitative results regarding the size of the abstraction
created as well as the number of proved and unproved MetiTarski problems.