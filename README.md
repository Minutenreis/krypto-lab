# krypto-lab
Krypto-Lab by Justus Dreßler

## Programme

Für jedes Programm soll erst zum jeweiligen Folder navigiert werden (`cd 1_additive-chiffre` bspw.).
Alle Programme wurden mit `python 3.10.12` geschrieben.
Jedes Programm printed seine Argumente sollte man es ohne aufrufen (hier sollten sie dennoch aufgelistet sein, aber falls ich eines vergesse).
`python3 encrypt-add.py` gibt bspw. `Usage: python3 encrypt-add.py path-to-plaintext key path-to-output` aus.

Argumente sind wie folgt angegeben: \
`python3 program.py` => Aufruf des Programs \
`argument` => Argument das angegeben werden muss \
`[argument]` => Optionales Argument (meist für meine Unit Tests)

Die Korrektheit der Programme wird mit Unittests sichergestellt (selbstgeschrieben, nicht konform zu einem Framework).
Alle Programme haben mindestens einen Unittest in den Files mit der Endung `.test.py`.
(Ausnahme: operation_mode.py da dies nur Vorarbeit für AES_Keygen war).
Wenn man alle Unittests ausführen will, muss man `python3 run-tests.py` im Grundverzeichniss ausführen. 

### Additive Chiffre (/1_additive-chiffre)

Verschlüsselung:

`python3 encrypt-add.py path-to-plaintext key path-to-output`

Entschlüsselung:

`python3 decrypt-add.py path-to-crypttext key path-to-output`

Automatische Entschlüsselung deutscher Texte:

`python3 auto-decode-add.py path-to-crypttext [path-to-output]`

### Viginere (/2_viginere-chiffre)

Verschlüsselung:

`python3 python3 encrypt-add.py path-to-plaintext key path-to-output`

Automatische Entschlüsselung deutscher Texte:

`python3 auto-decode-viginere.py path-to-crypttext path-to-output`

### AES 128 bit (/4_AES)

Verschlüsseln / Entschlüsseln:

`python3 AES.py path-to-plaintext path-to-key path-to-output encrypt/decrypt`

### AES mit Modi und beliebig langem Input (/5_AES_Keygen)

Verschlüsseln:

`python3 AES_Encryption.py mode input_file key_file output_file [initVec_file]`

Entschlüsseln:

`python3 AES_Encryption.py mode input_file key_file output_file [initVec_file]`

### Lineare Kryptoanalyse (/6_linear_cryptoanalysis)

Substitutions-Permutations-Netz:

`python3 SPN.py input_file key_file output_file`

Viele Klartexte generieren für Teilschlüsselsuche:

`python3 generateExampleTexts.py plaintext_file number_of_texts`

Linearisierungsangriff (Teilschlüsselsuche):

`python3 LinApprox.py plaintexts.txt ciphertexts.txt [output_file]`

### Güte von Approximationen bestimmen (/7_Quality_approximation)

`python3 SPN.py sBox_file approximation_file [output_file]`

### RSA (/8_RSA)

`python3 RSA.py input_file key_file output_file`

### RSA Schlüsselgenerierung (/9_RSA_Keygen)

`python3 RSA_keygen.py length output_private_key output_public_key output_primes`

### Diffie-Hellman-Schlüsselaustausch (/10_Diffie_Hellman)

`python3 diffie_hellman.py keylength [output_file]`

Note: output_file ist nur für meine Unittests gedacht und folgt nicht der Formattierung des Outputs in der Aufgabe

