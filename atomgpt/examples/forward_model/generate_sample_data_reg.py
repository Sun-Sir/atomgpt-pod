"""Module to generate example dataset.

This script downloads a subset of the ``dft_3d`` dataset and writes the
structures in ``POSCAR`` format together with the corresponding target
properties.  In some environments the cached dataset can become corrupted
which results in a ``zipfile.BadZipFile`` error when calling
``jarvis.db.figshare.data``.  To make the example more robust we download
the dataset to a local cache directory and, if necessary, remove the
corrupted file and re-download it.
"""

import os
import zipfile

from jarvis.core.atoms import Atoms
from jarvis.db.figshare import data as jdata, get_db_info


def load_dataset(dataset="dft_3d"):
    """Load a dataset from Figshare with basic corruption handling."""

    cache_dir = os.path.join(os.path.dirname(__file__), "dataset_cache")
    os.makedirs(cache_dir, exist_ok=True)

    js_tag = get_db_info()[dataset][1]
    zip_path = os.path.join(cache_dir, js_tag + ".zip")

    try:
        return jdata(dataset, store_dir=cache_dir)
    except zipfile.BadZipFile:
        # Remove the corrupted download and try again.
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return jdata(dataset, store_dir=cache_dir)


dft_3d = load_dataset()
prop = "optb88vdw_bandgap"
max_samples = 50

with open("id_prop.csv", "w") as f:
    count = 0
    for i in dft_3d:
        atoms = Atoms.from_dict(i["atoms"])
        jid = i["jid"]
        poscar_name = "POSCAR-" + jid + ".vasp"
        target = i[prop]
        if target != "na":
            atoms.write_poscar(poscar_name)
            f.write("%s,%6f\n" % (poscar_name, target))
            count += 1
            if count == max_samples:
                break
