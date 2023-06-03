import heapq
import numpy as np
import MDAnalysis as mda
from numpy.linalg import norm
from scipy.spatial.transform import Rotation as R

type_to_name = {
  "1": "Si",
  "2": "O",
  "3": "H"
}

def generate_names(system):
    names = []
    for type in system.types:
        name = type_to_name[type]
        names.append(name)
    return np.array(names)

type_to_charge = {
  "1": 1.87,
  "2": -0.93,
  "3": 0.1
}

def generate_charges(system, rescale_charges=True, verbose=True):
    charges = []
    for type in system.types:
        charge = type_to_charge[type]
        charges.append(charge)
    charges = np.array(charges)
    if rescale_charges:
        Qp = np.sum(charges[charges>0])
        Qm = np.sum(charges[charges<0])
        effect_rescaling = []
        for rescaling in np.linspace(-1,1,100000):
            Qpr = Qp*rescaling
            Qmr = Qm*(1-rescaling)
            net_charge = Qpr+Qmr
            effect_rescaling.append([rescaling, net_charge, Qpr, Qmr])
        effect_rescaling = np.array(effect_rescaling)
        required_rescaling = effect_rescaling[effect_rescaling.T[1] == closest(effect_rescaling.T[1], 0)][0][0]
        charges[charges<0] *= (1-required_rescaling)
        charges[charges>0] *= required_rescaling
    if verbose:
        if np.abs(np.sum(charges))>0.1:
            print("Warning, the charge is", np.sum(charges))
    return charges

def change_atom_type(u, atom_name, atom_id, atom_type):
    if u.atoms.names[u.atoms.indices == atom_id] == atom_name:
        types = u.atoms.types
        types[u.atoms.indices == atom_id] = atom_type
        v = mda.Universe.empty(len(u.atoms.positions), trajectory=True) # necessary for adding coordinates
        v.atoms.positions = u.atoms.positions
        v.add_TopologyAttr('names', generate_names(u.select_atoms("all")))
        v.add_TopologyAttr('charges', generate_charges(u.select_atoms("all"),verbose=False))
        v.add_TopologyAttr('type', types)
        v.dimensions = u.dimensions
        return v
    else:
        return u

def Hgroup():
    Hcoor = np.array([[0.000, 0.000, 0.000], # graft center
                        [ 0.000, 1.12, 0.000]]) # H
    XH = mda.Universe.empty(len(Hcoor), trajectory=True)
    XH.atoms.positions = Hcoor
    XH.add_TopologyAttr('name', ["X","H"])
    XH.add_TopologyAttr('type', ["X","3"])
    return XH

def defect_report(system, g_subject="name Si", g_neighbor="name O",  expected_neighbor = 4, cutoff_distance = 2.5):
    '''Detect missing or extra neighbor'''
    # detect the Si with anomalous neighbor number
    actual_box=system.dimensions[:3]
    group_i = system.select_atoms(g_subject)
    group_j = system.select_atoms(g_neighbor)
    id_neigbor = []
    for i_indice, i_position, i_charge in zip(group_i.indices, group_i.positions, group_i.charges):
        # for each atom of group i, look at the distances with group j
        distances = norm(np.remainder(group_j.atoms.positions - i_position + actual_box/2., actual_box) - actual_box/2.,axis=1)
        number_neighbor = np.sum(distances<cutoff_distance)
        id_neigbor.append([i_indice, number_neighbor, i_charge])
    return np.array(id_neigbor)

def generate_random_orientation(XYZ_initial):
    """
    Generate 3D aleatory rotation for molecule coordinate
    """
    rotation_radians = np.radians(np.random.rand()*180)
    rotation_axis = np.array([np.random.rand()*2-1, 
                              np.random.rand()*2-1, 
                              np.random.rand()*2-1])
    rotation_axis /= np.linalg.norm(rotation_axis)
    rotation_vector = rotation_radians * rotation_axis
    rotation = R.from_rotvec(rotation_vector)
    XYZ_rotated = rotation.apply(XYZ_initial)
    return XYZ_rotated

def closest(lst, K):
    #using heapq.nsmallest() to find the element in the list with the smallest absolute difference with K
    return heapq.nsmallest(1, lst, key=lambda x: abs(x-K))[0]

def insert_group(u, center_position, center_id, group, max_attempt=50, cut_off_energy = 0.01, verbose=True, replace=False):
    # find a proper orientation
    box = u.dimensions[:3]
    min_energy = 10
    nattempt = 0
    while (nattempt < max_attempt) & (min_energy>cut_off_energy):
        group_coor = generate_random_orientation(group.atoms.positions)
        insertion_energy = 0 # no units
        for group_coor_i in group_coor[1:]+center_position:
            all_d = np.remainder(u.atoms.positions[u.atoms.indices != center_id] - group_coor_i + box/2., box) - box/2.
            all_n = norm(all_d, axis= 1)
            insertion_energy += np.sum((1.2/all_n)**12)
        group_position = group_coor+center_position
        min_energy = np.min([min_energy, insertion_energy])
        nattempt += 1
    if min_energy < cut_off_energy:
        if verbose:
            print("successfull insert, energy",min_energy)
        # add the groupo to the MDA universe
        xgroup = group
        xgroup.atoms.positions = group_position
        v = mda.Merge(u.atoms, xgroup.atoms[1:])
        v.dimensions = u.dimensions
        return v
    else: # dont place any group
        if verbose:
            print("failled insert")
        return u