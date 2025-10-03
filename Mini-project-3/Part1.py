#compare extraterrestrial to blackbody.py
# Overlay a 5800 K blackbody on the Kurucz spectrum, with correct units.
# Notes:
# - The file's spectral irradiance values look like W m^-2 μm^-1 (not per nm).
#   We'll convert them to per-nm for plotting/consistency with many references.
# - We scale the 5800 K blackbody so that its integral over the same wavelength
#   range equals the integrated solar constant from the file (shape comparison).


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import trapz

# NB! You need to link up to your location
from pathlib import Path

local_path = Path(__file__).parent
path = local_path / "kurudz_0.1nm.dat"
# Robust read: whitespace-delimited, ignore comment lines (starting with '#')
df = pd.read_csv(
    path,
    delim_whitespace=True,
    comment="#",
    header=None,
    engine="python"
)

df = df.rename(columns={df.columns[0]: "wavelength_nm"})
df = df.rename(columns={df.columns[1]: "spectral_irradiance_mW_m2_nm"})
# Add a column with corrected units W/m^2 nm
df["spectral_irradiance_W_m2_nm"] = df["spectral_irradiance_mW_m2_nm"] /1000

# Compute an integral estimate of the solar constant over the file's wavelength span
wl_nm = df["wavelength_nm"].to_numpy()
E_nm = df["spectral_irradiance_W_m2_nm"].to_numpy()



# Plot the spectrum
plt.subplots(figsize=(12/2.54, 8/2.54))  # 15 cm × 8 cm
plt.plot(wl_nm, E_nm)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Spectral irradiance (W m$^{-2}$ nm$^{-1}$)")
plt.title("Kurucz extraterrestrial solar spectrum (from file)")
plt.xlim([280,3000])
plt.show()

def nm_to_rgb(wavelength,alpha):
    gamma = 0.80
    intensity_max = 255
    factor = 0.0
    red = green = blue = 0.0
    if 380 <= wavelength < 440:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif 440 <= wavelength < 490:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif 490 <= wavelength < 510:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif 580 <= wavelength < 645:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    elif 645 <= wavelength < 781:
        red = 1.0
        green = 0.0
        blue = 0.0
    else:
        red = green = blue = 0.0
    # Intensitet nær synsgrensene
    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 <= wavelength < 701:
        factor = 1.0
    elif 701 <= wavelength < 781:
        factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 700)
    else:
        factor = 0.0
    def adjust(color):
        if color == 0.0:
            return 0
        return round(intensity_max * pow(color * factor, gamma))
    r = adjust(red)/255
    g = adjust(green)/255
    b = adjust(blue)/255
    return (r, g, b,alpha)


# ---- Physical blackbody scaling ----
h = 6.62607015e-34     # J s
c = 2.99792458e8       # m s^-1
k = 1.380649e-23       # J K^-1
R_sun = 6.957e8        # m
AU = 1.495978707e11    # m

def planck_B_lambda(lam_m, T):
    """Planck spectral radiance B_lambda [W m^-2 sr^-1 m^-1]."""
    x = (h*c)/(lam_m*k*T)
    return (2*h*c**2)/(lam_m**5) / (np.exp(x) - 1.0)

def solar_irradiance_at_earth_per_nm(wl_nm, T):
    lam_m = wl_nm * 1e-9
    B = planck_B_lambda(lam_m, T)                   # W m^-2 sr^-1 m^-1
    E_per_m = np.pi * B * (R_sun/AU)**2            # W m^-2 m^-1
    E_per_nm = E_per_m / 1e9                       # W m^-2 nm^-1
    return E_per_nm

BB5880=solar_irradiance_at_earth_per_nm(wl_nm, 5880.0)
# Solar constant from the Kurucz spectrum (numerical integral)
solar_constant_kurucz = np.trapezoid(E_nm, wl_nm)  # W/m^2
print(f"Solar constant from Kurucz data = {solar_constant_kurucz:.2f} W/m^2")

# Solar constant from the 5880 K blackbody (same wavelength range)
solar_constant_bb = np.trapezoid(BB5880, wl_nm)  # W/m^2
print(f"Solar constant from 5880 K blackbody = {solar_constant_bb:.2f} W/m^2")

# Plot
plt.figure()
# Plot the rainbow colors in the visible part of the spectrum
for lam in np.linspace(380,770,195):
    plt.axvspan(lam, lam+2, facecolor=nm_to_rgb(lam,0.25), linewidth=0)

plt.plot(wl_nm, E_nm, label="Kurucz TOA spectrum (per nm)")
plt.plot(wl_nm, BB5880, "-",color='blue',linewidth=2,label="Blackbody 5880 K ")
plt.xlim(wl_nm.min(), wl_nm.max())
plt.xlabel("Wavelength (nm)")
plt.ylabel("Spectral irradiance (W m$^{-2}$ nm$^{-1}$)")
plt.title("Kurucz solar spectrum with and Black Body overlay")
plt.legend()
plt.xlim([280,3000])
plt.show()

