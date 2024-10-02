# Using Scherbius Token as the Root of Trust (RoT)

## Overview
This project simulates Castle Shield's **Scherbius Token** using software, replicating the behavior of its **Physical Unclonable Function (PUF)**. The Scherbius Token relies on **SRAM memory chips** to enhance security, utilizing the natural variance in startup values of the SRAM cells. Binary readings from the SRAM are stored as files, simulating the power cycling of the SRAM in the hardware.

### Key Concepts:
- **SRAM-based PUF**: A hardware feature that generates unique and unpredictable binary outputs each time it powers on, due to the random nature of SRAM's startup behavior.
- **Stable and Unstable Cells**:
  - **Stable Cells**: ~75% of SRAM cells maintain a consistent value (either 0 or 1) after each power cycle. These cells are crucial for cryptographic key generation, ensuring that keys can be recovered reliably.
  - **Unstable (Ternary) Cells**: ~25% of SRAM cells fluctuate between 0 and 1 on each power cycle. These cells are used for true random number generation due to their unpredictability.

## Path Overview
The simulation code introduces a files in path, `RoT/enroll`, which serves as the **Root of Trust (RoT)** for the system. The path reads random binary data from the Scherbius Token, simulating a fresh power cycle of the SRAM PUF.

- **Location**: `RoT/enroll`
- **Purpose**: To simulate the behavior of the hardware PUF by accessing pre-recorded SRAM power cycle data.

## How the Simulation Works
Each binary file in the `RoT/enroll` directory represents the state of the SRAM PUF after a power cycle. Here's how the simulation functions:

1. **Binary Files**: Each file contains 1,048,576 bits (1MB) representing the state of the SRAM cells after powering on.
2. **Stable Cells**: ~75% of the cells consistently produce the same value (0 or 1) with each power cycle. These are used for secure key generation.
3. **Unstable (Ternary) Cells**: ~25% of the cells fluctuate between 0 and 1. These cells are considered fuzzy and are ideal for true random number generation.

### Key Generation and Error Correction
When using the stable cells for **cryptographic key generation**, slight fluctuations in the SRAM readings between power cycles may result in small discrepancies between keys generated from the same addresses. To ensure consistency:
- The **maximum error** between generated keys should not exceed 0.05% of the total key length. If the error rate exceeds this threshold, the key should be rejected, and a new one generated.
- To correct minor errors (0.05% or less), an **Error Correction Code (ECC)** can be employed. The ECC ensures that small deviations in key bits are corrected automatically, allowing for consistent key recovery despite slight variations in the SRAM's output.

### Using the Simulation
To simulate the Scherbius Token in your application, read one of the binary files from the `RoT/enroll` path. The binary data can be used for two primary purposes:
- **Cryptographic Key Generation**: Utilize the stable cells to reliably generate a secure cryptographic key.
- **True Random Number Generation**: Leverage the fluctuating cells to produce high-quality random numbers for security functions.

### Example Use Cases:
1. **Key Generation**: Extract the stable cells (those that do not fluctuate) across power cycles to generate secure cryptographic keys.
2. **Random Number Generation**: Use the ternary (unstable) cells as a source of entropy for generating true random numbers.

## Conclusion
This software-based simulation of the Scherbius Token provides an accessible way to explore the behavior of hardware tokens using SRAM PUFs. By utilizing the binary files in the `RoT/enroll` path, developers can simulate the Scherbius Token's behavior for cryptographic key generation, true random number generation, and key recovery, complete with error correction mechanisms for minor deviations in the readings.

## Test Code for Key generation:
This demo demonstrates how to generate and recover a 256-bit key without storing it. Innovators must use various techniques to select the most stable SRAM cells for key generation, ensuring that the error rate between the generated and recovered keys remains below 3%.

`
python main.py
`
---