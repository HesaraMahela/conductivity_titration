import matplotlib.pyplot as plt

# Given data
initial_concentration_HCl = 1.00  # mol/L
initial_concentration_CH3COOH = 1.00  # mol/L
initial_concentration_NaOH = 1.00  # mol/L
volume_HCl = 5.00  # cm3
volume_CH3COOH = 5.00  # cm3

# Calculate moles of each species initially
moles_HCl_initial = initial_concentration_HCl * volume_HCl / 1000  # converting cm3 to L
moles_CH3COOH_initial = initial_concentration_CH3COOH * volume_CH3COOH / 1000  # converting cm3 to L
moles_NaOH_initial = initial_concentration_NaOH * volume_HCl / 1000  # assuming volume_NaOH = volume_HCl

volumes_NaOH = []
conductivities = {'H+': 349.6, 'OH-': 199, 'Cl-': 76.3, 'Na+': 50.1, 'CH3COO-': 40.9}

conductivity_values = []


def H_pluse_concentration(moles_HCl_initial, moles_NaOH_added, moles_CH3COOH_initial, total_volume):
    if (moles_HCl_initial > moles_NaOH_added):
        return (moles_HCl_initial - moles_NaOH_added) / total_volume
    elif (moles_HCl_initial + moles_CH3COOH_initial > moles_NaOH_added):
        moles_of_CH3COOH = moles_HCl_initial + moles_CH3COOH_initial - moles_NaOH_added
        moles_of_CH3COO_minus = moles_CH3COOH_initial - moles_of_CH3COOH
        if (moles_of_CH3COO_minus == 0):
            return 0

        return ((1.8 / 100_000) * moles_of_CH3COOH / moles_of_CH3COO_minus) / total_volume
    else:
        return 0


def Cl_minus_concentration(moles_HCl_initial, total_volume):
    return moles_HCl_initial / total_volume


def CH3COO_minus_concentration(moles_CH3COOH_initial, moles_NaOH_added, total_volume):
    if (moles_HCl_initial > moles_NaOH_added):
        return 0
    elif (moles_HCl_initial + moles_CH3COOH_initial > moles_NaOH_added):
        moles_of_CH3COOH = moles_HCl_initial + moles_CH3COOH_initial - moles_NaOH_added
        moles_of_CH3COO_minus = moles_CH3COOH_initial - moles_of_CH3COOH

        return moles_of_CH3COO_minus / total_volume
    else:
        return moles_CH3COOH_initial / total_volume


def Na_pulse_concentration(moles_NaOH_added, total_volume):
    return moles_NaOH_added / total_volume


def OH_minus_concentration(moles_HCl_initial, moles_NaOH_added, moles_CH3COOH_initial, total_volume):
    if (moles_HCl_initial + moles_CH3COOH_initial < moles_NaOH_added):
        OH_from_NaOH = moles_NaOH_added - moles_HCl_initial + moles_CH3COOH_initial
        OH_from_CH3COO_ = pow(
            1 / (1.8 * pow(10, 9)) * CH3COO_minus_concentration(moles_CH3COOH_initial, moles_NaOH_added,
                                                                total_volume), 0.5)

        return OH_from_NaOH + OH_from_CH3COO_
    else:
        return 0


print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
    "Volume_NaOH (L)", "C_H_plus", "C_OH_minus", "C_Na_pulse", "C_Cl_minus", "C_CH3COO_minus", "Conductivity"
))
conductivity_H_pulse = []
conductivity_OH_minus = []
conductivity_Na_pulse = []
conductivity_Cl_minus = []
conductivity_CH3COO_minus = []

for volume_NaOH in range(0, 100, 1):
    moles_NaOH_added = initial_concentration_NaOH * volume_NaOH / 1000  # converting cm3 to L
    total_volume = (volume_HCl + volume_NaOH + volume_CH3COOH) / 1000
    # print(moles_HCl_initial, moles_NaOH_added, moles_CH3COOH_initial, total_volume)

    C_H_plus = H_pluse_concentration(moles_HCl_initial, moles_NaOH_added, moles_CH3COOH_initial, total_volume)
    C_OH_minus = OH_minus_concentration(moles_HCl_initial, moles_NaOH_added, moles_CH3COOH_initial, total_volume)

    C_Cl_minus = Cl_minus_concentration(moles_HCl_initial, total_volume)

    C_CH3COO_minus = CH3COO_minus_concentration(moles_CH3COOH_initial, moles_NaOH_added, total_volume)

    C_Na_pulse = Na_pulse_concentration(moles_NaOH_added, total_volume)

    conductivity_H_pulse.append(conductivities['H+'] * C_H_plus)
    conductivity_OH_minus.append(conductivities['OH-'] * C_OH_minus)
    conductivity_Na_pulse.append(conductivities['Na+'] * C_Na_pulse)
    conductivity_Cl_minus.append(conductivities['Cl-'] * C_Cl_minus)
    conductivity_CH3COO_minus.append(conductivities['CH3COO-'] * C_CH3COO_minus)

    conductivity = conductivities['H+'] * C_H_plus + conductivities['OH-'] * C_OH_minus \
                   + conductivities['Na+'] * C_Na_pulse \
                   + conductivities['Cl-'] * C_Cl_minus + conductivities['CH3COO-'] * C_CH3COO_minus

    print("{:<15.3f} {:<15.6f} {:<15.6f} {:<15.6f} {:<15.6f} {:<15.6f} {:<15.6f}".format(
        volume_NaOH / 1000, C_H_plus, C_OH_minus, C_Na_pulse, C_Cl_minus, C_CH3COO_minus, conductivity
    ))
    # Append data to lists
    volumes_NaOH.append(volume_NaOH / 1000)  # converting cm3 to L
    conductivity_values.append(conductivity)

# Plot the titration curve


# Plot the titration curve
plt.plot(volumes_NaOH, conductivity_values, label='Total Conductivity')
plt.plot(volumes_NaOH, conductivity_H_pulse, label='H+ Contribution')
plt.plot(volumes_NaOH, conductivity_OH_minus, label='OH- Contribution')
plt.plot(volumes_NaOH, conductivity_Na_pulse, label='Na+ Contribution')
plt.plot(volumes_NaOH, conductivity_Cl_minus, label='Cl- Contribution')
plt.plot(volumes_NaOH, conductivity_CH3COO_minus, label='CH3COO- Contribution')

plt.xlabel("Volume of NaOH added (L)")
plt.ylabel("Conductivity (S/cm3)")
plt.title("Conductivity Vs NaOH volume")
plt.grid(True)
plt.legend()
plt.show()
