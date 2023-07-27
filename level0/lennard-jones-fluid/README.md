# Lennard Jones fluid

## A simulation with no thermostat

1) It is important to first bring the system to a proper temperature by running a
small NVT simulation, which is done here with the [first input](./a-simulation-with-no-thermostat/input.a.lammps).

2) Then, start the NVE simulation from the equilibrated configuration
Note that the equilibrated configuration contains the atoms velocities, i.e. it contains the temperature.

No thermostat such as temp/berendsen or langevin is used. For the atom positions to be updated
following Newton's law, the fix nve must be kept.

It can sometimes be better to reduce the timestep when using NVE system, as it gives better energy conservation?

The total energy of the system can be extracted using the internal LAMMPS variable etotal,
see the [second input](./a-simulation-with-no-thermostat/input.b.lammps).

## Do without the ‘minimize’ command

## Non-equilibrium simulation

## Dumbbell molecules
