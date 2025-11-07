"""
RevisarRTAs.py
Uso: python RevisarRTAs.py <archivo_generado_A> <archivo_esperado_E>
Compara estrictamente ambos archivos (byte a byte) y escribe en stdout "SÍ" si son iguales o "NO" si difieren.
"""
import sys
import os

def main():
    if len(sys.argv) < 3:
        print("NO")
        return
    producido = sys.argv[1]
    esperado = sys.argv[2]
    try:
        with open(producido, 'rb') as f1, open(esperado, 'rb') as f2:
            b1 = f1.read()
            b2 = f2.read()
            if b1 == b2:
                print("SÍ")
            else:
                print("NO")
    except FileNotFoundError:
        print("NO")

if __name__ == '__main__':
    main()
