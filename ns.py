# DES Algorithm (Complex Educational Version)
import sys

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5, 4, 5,
     6, 7, 8, 9, 8, 9, 10, 11,
     12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27,
     28, 29, 28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

S_BOXES = [
    [[14, 4, 13, 1], [0, 15, 7, 4], [4, 1, 14, 8], [15, 12, 8, 2]],
]

def string_to_bit_array(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def bit_array_to_string(bits):
    return ''.join(chr(int(''.join(str(bit) for bit in bits[i:i+8]), 2)) for i in range(0, len(bits), 8))

def permute(bits, table):
    return [bits[x - 1] for x in table]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def sbox_substitution(bits):
    output = []
    for i in range(0, len(bits), 6):
        block = bits[i:i+6]
        row = (block[0] << 1) + block[5]
        col = int(''.join(str(x) for x in block[1:5]), 2)
        val = S_BOXES[0][row % len(S_BOXES[0])][col % len(S_BOXES[0][0])]
        output.extend([int(x) for x in format(val, '04b')])
    return output

def des_encrypt_block(plaintext, key):
    bits = string_to_bit_array(plaintext)
    bits = bits[:64]
    bits = permute(bits, IP)

    L, R = bits[:32], bits[32:]

    for round in range(1, 17):
        expanded_R = permute(R, E)
        fake_round_key = key[:48]
        temp = xor(expanded_R, fake_round_key)
        temp = sbox_substitution(temp)
        temp = permute(temp, P)
        new_R = xor(L, temp)
        L = R
        R = new_R

    combined = R + L
    final_bits = permute(combined, IP_INV)
    return bit_array_to_string(final_bits)

def main():
    text = input("Enter 8 characters (64-bit block): ")
    key_input = input("Enter 8-character key (for 64-bit key): ")
    if len(text) != 8 or len(key_input) != 8:
        print("Text and key must be exactly 8 characters each.")
        sys.exit(1)

    key_bits = string_to_bit_array(key_input)
    encrypted = des_encrypt_block(text, key_bits)
    print("Encrypted Output (raw bits):", encrypted)

if __name__ == '__main__':
    main()
