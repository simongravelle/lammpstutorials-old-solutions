# Breaking a carbon nanotube

## Isolated nanotube

Simply remove the thermostat and print the temperature in 
a file using the fix ave/time, see my 
[input](./stetching-isolated-nanotube/input.lammps) here.

## Deforming membrane

Starting from the data file given in the tutorial, 
one can rescale the box and then replicate it using the 
replicate command, see the [input](./deforming-membrane/input.lammps).

The *change_box all triclinic* command is used to convert the 
box into triclinic, allowing for deformations along the xy plane,
which is done using the fix deform.

## Decorate the CNT

The decoration of the CNT is done by randomly adding hydrogen atoms 
using create_atoms command, see [input](./decorating-the-CNT/input.lammps).
The pair_coeff must be adapted to allow for both carbon and hydrogen
atoms C H. The number of atom type must also be changed in the cnt.data file,
from 1 to 2.
