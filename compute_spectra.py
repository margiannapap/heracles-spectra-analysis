import numpy as np
import heracles
import heracles.ducc
from heracles.notebook import Progress
from astropy.io import fits

# 1. Basic parameters
lmax = 1024 

# 2. Setup the DiscreteMapper
mapper = heracles.ducc.DiscreteMapper(lmax)

# 3. Handle Visibility (Required by Heracles)
# Since you don't have a vmap.fits.gz, we load the catalog and create a dummy visibility
catalog = heracles.FitsCatalog("catalog.fits")

# Instead of loading an external vmap file, we set a uniform visibility
# to satisfy the requirement: "catalog.visibility = valm"
# We create a dummy harmonic array of zeros (representing a flat sky)
valm = np.zeros(mapper.alm_size, dtype=complex)
valm[0] = 1.0  # monopole
catalog.visibility = valm

# 4. Define fields
fields = {
    "POS": heracles.Positions(mapper, "RA", "DEC", mask="VIS"),
    "SHE": heracles.Shears(mapper, "RA", "DEC", "E1", "E2", mask="WHT"),
}

# 5. Mapping with Progress
# We use the catalog directly
catalogs = {1: catalog}

with Progress("mapping") as progress:
    data = heracles.map_catalogs(fields, catalogs, parallel=True, progress=progress)

# 6. Compute power spectra
cls = heracles.angular_power_spectra(data)

# 7. Save results
np.save('discrete_spectra_results.npy', cls)
print("Analysis completed successfully!")
