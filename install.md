*****************************
Running and Installing QUATUM
*****************************

The backend decision procedure used by QUANTUM is the automated theorem prover MetiTarski. You will need to compile my branched version from source, because it supports millisecond timeouts, rather than the default second timeouts in the master branch.

The code is available at:

http://code.google.com/r/williamdenman-metitarski/source/checkout

And you can directly clone it with Mercurial using: 

hg clone https://william.denman@code.google.com/r/williamdenman-metitarski/ 

Once MetiTarski is up and running, you will need several Python modules, including

sympy (for symbolically computing derivatives and differential equation handling)
termcolor (for nice coloured output)
pydot (for generating nice graphical representation of abstractions)

