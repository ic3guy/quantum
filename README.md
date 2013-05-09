***********************************************************
QUANTUM - Qualitative Abstractions of Non-Polynomial Models
***********************************************************

9th May 2013

Abandon hope all ye who enter here! This is a research tool for the
automatic qualitative abstraction of dynamical systems that contain
transcendental functions. I will try my best to describe how to run
it, but bear in mind that you will probably need my help to do
anything useful.

You will need at a minimum to have installed MetiTarski (with
Poly/ML), along with an appropriate decision procedure (QEPCAD,
Mathematica or Z3). Please contact me if you need help with
isntallation of MetiTarski, we have a binary version available for
certain architectures.

William Denman - william.denman@gmail.com

***

The main program loop is contained in 'quantum.py'. A list of example
files that are to be analysed can be specified in the filenames
string list. Each of these filenames correspond to different .py files
located in the examples directory.

The abstraction algorithm is then attempted on each file in the list
of filenames with the MetiTarski timeouts in the meti_timeout
field. The current timeouts are 10, 100, 1000 and 4000 milliseconds.

A directory named 'experiments' will be created after running the
experiments that will contain proved and unproved Metitarski tptp
files that have been generated during the qualitative abstraction
process.

A text file named 'log.txt' will be generated containing timing
statistics as well as various quantitative results regarding the size
of the abstraction created as well as the number of proved and
unproved MetiTarski problems.