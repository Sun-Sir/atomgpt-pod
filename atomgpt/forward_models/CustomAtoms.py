from __future__ import annotations

from jarvis.core.atoms import Atoms


class CustomAtoms(Atoms):
    """Atom structure with simplified description output.

    Inherits from :class:`jarvis.core.atoms.Atoms` but overrides the
    :meth:`describe` method so that it returns only material attributes
    concatenated by underscores. This is useful when a compact,
    description-free representation is required for downstream models.
    """

    @classmethod
    def from_poscar(cls, filename: str = "POSCAR") -> "CustomAtoms":
        """Read a POSCAR/CONTCAR file and return a ``CustomAtoms`` object."""
        from jarvis.io.vasp.inputs import Poscar

        base_atoms = Poscar.from_file(filename).atoms
        return cls(
            lattice_mat=base_atoms.lattice_mat,
            coords=base_atoms.frac_coords,
            elements=base_atoms.elements,
            props=base_atoms.props,
            cartesian=False,
        )

    def describe(self, *args, **kwargs):
        """Return only material attributes joined by underscores.

        This method calls the parent ``describe`` to obtain the structured
        information (chemical and structural properties) and then flattens
        those properties into a single underscore-separated string without
        any natural-language descriptions.
        """
        info = super().describe(*args, **kwargs)
        attrs = []
        for section in ("chemical_info", "structure_info"):
            data = info.get(section, {})
            for value in data.values():
                if isinstance(value, dict):
                    part = ",".join(f"{k}:{v}" for k, v in value.items())
                    attrs.append(part)
                else:
                    attrs.append(str(value))
        attr_str = "_".join(a.replace(" ", "") for a in attrs)
        return {"desc_1": attr_str, "desc_2": attr_str, "desc_3": attr_str}
