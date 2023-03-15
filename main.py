import re
import streamlit as st

# playfair
def generate_table(key):
    # Membuat tabel Playfair Cipher dengan menggunakan kunci
    key = re.sub(r'[^A-Za-z]', '', key.upper())
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key += alphabet
    table = []
    for char in key:
        if char not in table:
            table.append(char)
    table = ''.join(table)
    table = [table[i:i+5] for i in range(0,25,5)]
    return table

def get_position(table, char):
    # Mendapatkan posisi karakter di dalam tabel
    row = col = 0
    for i in range(5):
        for j in range(5):
            if table[i][j] == char:
                row = i
                col = j
                break
    return row, col

def encrypt_playfair(plaintext, key):
    # Enkripsi plaintext menggunakan Playfair Cipher
    table = generate_table(key)
    plaintext = re.sub(r'[^A-Za-z]', '', plaintext.upper())
    plaintext = re.sub(r'J', 'I', plaintext)
    if len(plaintext) % 2 == 1:
        plaintext += 'X'
    ciphertext = ''
    for i in range(0, len(plaintext), 2):
        row1, col1 = get_position(table, plaintext[i])
        row2, col2 = get_position(table, plaintext[i+1])
        if row1 == row2:
            ciphertext += table[row1][(col1+1)%5]
            ciphertext += table[row2][(col2+1)%5]
        elif col1 == col2:
            ciphertext += table[(row1+1)%5][col1]
            ciphertext += table[(row2+1)%5][col2]
        else:
            ciphertext += table[row1][col2]
            ciphertext += table[row2][col1]
    return ciphertext

def decrypt_playfair(ciphertext, key):
    # Dekripsi ciphertext menggunakan Playfair Cipher
    table = generate_table(key)
    plaintext = ''
    for i in range(0, len(ciphertext), 2):
        row1, col1 = get_position(table, ciphertext[i])
        row2, col2 = get_position(table, ciphertext[i+1])
        if row1 == row2:
            plaintext += table[row1][(col1-1)%5]
            plaintext += table[row2][(col2-1)%5]
        elif col1 == col2:
            plaintext += table[(row1-1)%5][col1]
            plaintext += table[(row2-1)%5][col2]
        else:
            plaintext += table[row1][col2]
            plaintext += table[row2][col1]
    plaintext = re.sub(r'X', '', plaintext)
    return plaintext

# vinegere
def encrypt_vigenere(plaintext, key):
    # Enkripsi plaintext menggunakan Vigenere Cipher
    plaintext = plaintext.upper()
    key = key.upper()
    ciphertext = ''
    for i in range(len(plaintext)):
        char = plaintext[i]
        key_char = key[i % len(key)]
        if char.isalpha():
            char = chr((ord(char) + ord(key_char) - 2 * ord('A')) %
                       26 + ord('A'))
        ciphertext += char
    return ciphertext

def decrypt_vigenere(ciphertext, key):
    # Dekripsi ciphertext menggunakan Vigenere Cipher
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = ''
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        key_char = key[i % len(key)]
        if char.isalpha():
            char = chr((ord(char) - ord(key_char) + 26) % 26 + ord('A'))
        plaintext += char
    return plaintext

def main():
    menu = st.sidebar.selectbox("Menu", ["Playfair", "vigenere"])
    if menu == "Playfair":
        st.title("Playfair")
        plaintext = st.text_input("Masukkan plaintext")
        key = st.text_input("Masukkan kunci")
        if st.button("Encrypt"):
            st.write("# Hasil enkripsi: ", encrypt_playfair(plaintext, key))
        if st.button("Decrypt"):
            st.write("# Hasil dekripsi: ", decrypt_playfair(plaintext, key))
    elif menu == "vigenere":
        st.title("Vigenere")
        plaintext = st.text_input("Masukkan plaintext")
        key = st.text_input("Masukkan kunci")
        if st.button("Encrypt"):
            st.write("# Hasil enkripsi: " + encrypt_vigenere(plaintext, key))
        if st.button("Decrypt"):
            st.write("# Hasil dekripsi: " + decrypt_vigenere(plaintext, key))

if __name__ == "__main__":
    main()