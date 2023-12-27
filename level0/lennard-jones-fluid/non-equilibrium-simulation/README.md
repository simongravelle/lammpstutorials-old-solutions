
Non-equilibrium simulation
--------------------------

So far, atoms were freely diffusing without contraint or external force.
Add an external force to induce a net flow of atoms in one
direction. The magnitude of the force must be chosen so
that the system is not *too far* from equilibrium.

LAMMPS offers several option to add external force to a system, one 
being the fix addforce.

Note: If the system is too far from equilibrium, it enters the non-linear response 
regimes and its properties and parameters will differ from its equilibrium values.
In general, this is something that you must avoid (unless you are studying
non-linear effects). 
