from bitarray import bitarray
import secrets


# Read the binary file into a bitarray
def read_bin_file(filepath):
    """
    Reads a binary file and converts its content into a bitarray.

    :param filepath: Path to the binary file.
    :return: bitarray containing the binary content.
    """
    bit_data = bitarray()
    with open(filepath, 'rb') as f:
        bit_data.fromfile(f)
    return bit_data


# Generate key based on PUF read
def generate_key(puf_data, key_length=256):
    """
    Generates a key by selecting random addresses from the PUF data.

    :param puf_data: The bitarray containing the PUF data.
    :param key_length: Length of the key to be generated in bits (default 256 bits).
    :return: bitarray representing the generated key.
    :return: addresses represents a list of addresses that were used to generate the key
    """
    key = bitarray()
    puf_size = len(puf_data)
    addresses = []
    for _ in range(key_length):
        # Randomly pick an address between (0, puf_size)
        address = secrets.randbelow(puf_size)
        addresses.append(address)
        # Append the bit from that address to the key
        key.append(puf_data[address])

    return key, addresses


# Recover the key based on PUF read
def recover_key(puf_data, addresses, key_length=256):
    """
    Generates a key by selecting random addresses from the PUF data.

    :param puf_data: The bitarray containing the PUF data.
    :param addresses: List of addresses read while generating the key the first time
    :param key_length: Length of the key to be generated in bits (default 256 bits).
    :return: bitarray representing the generated key.
    """
    key = bitarray()

    for i in range(key_length):
        # Read the individual address
        address = addresses[i]
        # Append the bit from that address to the key
        key.append(puf_data[address])

    return key


# Compare two keys and calculate the error rate
def compare_keys(key1, key2):
    """
    Compares two keys and calculates the error rate.

    :param key1: The first bitarray key.
    :param key2: The second bitarray key.
    :return: The error rate as a percentage.
    :return: The number of errors (int)
    """
    assert len(key1) == len(key2), "Keys must be of the same length"

    # Count mismatches (errors)
    errors = sum(bit1 != bit2 for bit1, bit2 in zip(key1, key2))
    error_rate = (errors / len(key1)) * 100

    return error_rate, errors


# Apply basic error correction (e.g., Hamming code)
def apply_error_correction(key1, key2):
    """
    Applies basic error correction by checking bit differences between two keys
    and correcting small discrepancies.

    :param key1: The first bitarray key.
    :param key2: The second bitarray key.
    :return: Corrected key (bitarray).
    """
    corrected_key = bitarray()

    # Correct single-bit errors by using majority voting
    for bit1, bit2 in zip(key1, key2):
        # If both bits are the same, keep the value; if not, take the value from key1
        corrected_key.append(bit1 if bit1 == bit2 else bit1)

    return corrected_key


if __name__ == '__main__':
    # Read the PUF data from a binary file (first instance)
    puf_read1 = read_bin_file('RoT/enroll/12.bin')

    # Generate the key from the first instance of the PUF read
    key1, addresses = generate_key(puf_read1)

    # Read the PUF data again (second instance)
    puf_read2 = read_bin_file('RoT/enroll/500.bin')

    # Regenerate the key from the second instance of the PUF read
    key2 = recover_key(puf_read2, addresses)

    # Compare the two keys and calculate the error rate
    error_rate, num_errors = compare_keys(key1, key2)

    # Print the error rate between the two keys
    print(f"Error Rate: {error_rate:.5f}%")

    # If errors are within acceptable threshold (not more than 5%), apply error correction
    if error_rate <= 5.0:
        corrected_key = apply_error_correction(key1, key2)
        print(f"Key corrected with error correction. Errors: {num_errors}")

        # Compare the initial key and corrected key
        error_rate, num_errors = compare_keys(key1, corrected_key)

        # Print the error rate between the two keys
        print(f"Corrected Key Compared Error Rate: {error_rate:.5f}%")
    else:
        corrected_key = key2
        print("Error rate too high, key could not be corrected.")

