import numpy as np
from astropy.io import fits
import heracles as hera

print("--- Analyzing Catalog with HERACLES Context ---")

try:
    print("Loading catalog.fits safely...")
    with fits.open('catalog.fits', memmap=True) as hdul:
        data = hdul[1].data
        
        #from. 0.6 to 0.65)
        z_min = 0.6
        z_max = 0.65
        
        print(f"Applying redshift mask: {z_min} < z < {z_max}...")
        mask = (data['ZTRUE'] > z_min) & (data['ZTRUE'] < z_max)
        
      
        sub_z = data['ZTRUE'][mask]
        sub_e1 = data['E1'][mask]
        
        
        mean_z = np.mean(sub_z)
        mean_e1 = np.mean(sub_e1)
        
        print(f"\n=== Dataset Statistics (Redshift Slice) ===")
        print(f"Number of galaxies found: {len(sub_z)}")
        print(f"Mean Redshift (ZTRUE): {mean_z:.4f}")
        print(f"Mean Ellipticity (E1): {mean_e1:.4f}")
        
        print("\nHERACLES readiness test: Complete!")

except Exception as e:
    print(f"\n[ERROR] An error occurred: {e}")

input("\n=== PRESS ENTER TO CLOSE THIS WINDOW ===")
