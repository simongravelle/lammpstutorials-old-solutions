


Post-mortem analysis
--------------------


In today research, most data analyses are
done after the simulation is over, and it is important for
LAMMPS users to know how to do it.

Import the trajectory using Python, and re-extract the
end-to-end distance.

You can import *lammpstrj* file using *MDAnalysis* in *Python*:

..  code-block:: bw

    u = mda.Universe("dump.lammpstrj", format = "LAMMPSDUMP")
