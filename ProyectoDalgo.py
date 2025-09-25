"""
FESTIVAL DE LOS ROBOTS CREATIVOS - DIGIT DP CON ACARREO

Problema:
- Distribuir n unidades de energía en exactamente k celdas (números no negativos)
- Solo los dígitos 3, 6 y 9 aportan puntos de creatividad
- La puntuación depende del dígito y su posición según una tabla dada
- Objetivo: Maximizar la creatividad total

Solución: Digit DP con acarreo
- Procesa columna por columna (unidades → decenas → ...)
- En cada columna p: suma de k dígitos = d_p - cin + 10*cout
- Ganancia óptima por columna: P_p * floor(T/3) donde T es la suma
- Complejidad: O(columnas × k × acarreos) = O(6 × k × k) ≈ O(k²)

Autor: Tu nombre aquí  
Fecha: Septiembre 2025
"""

def resolver_festival_robots(n, k, valores_p):
    """
    Resuelve usando Digit DP con acarreo - enfoque eficiente para límites grandes
    
    Args:
        n: Total de energía a distribuir
        k: Número de celdas
        valores_p: Lista de valores [P0, P1, P2, P3, P4]
    
    Returns:
        La máxima creatividad posible
    """
    # Convertir n a dígitos (de derecha a izquierda: unidades, decenas, ...)
    digitos_n = []
    temp_n = n
    while temp_n > 0:
        digitos_n.append(temp_n % 10)
        temp_n //= 10
    
    # Si n = 0, caso especial
    if not digitos_n:
        digitos_n = [0]
    
    num_columnas = len(digitos_n)
    
    # DP[columna][acarreo] = máxima creatividad
    # Inicializar con -infinito (imposible)
    INF = float('inf')
    dp_prev = {}
    dp_curr = {}
    
    # Caso base: columna 0, acarreo 0
    dp_prev[0] = 0
    
    # Procesar cada columna
    for col in range(num_columnas):
        dp_curr = {}
        d_p = digitos_n[col]
        P_p = valores_p[col] if col < len(valores_p) else 0
        
        # Para cada acarreo de entrada alcanzable
        for cin in dp_prev:
            if dp_prev[cin] == -INF:
                continue
            
            # Probar todas las sumas T posibles en esta columna
            # T debe satisfacer: T ≡ d_p - cin (mod 10) y 0 ≤ T ≤ 9*k
            target_mod = (d_p - cin) % 10
            
            for T in range(target_mod, 9 * k + 1, 10):
                if T < 0:
                    continue
                
                # Calcular acarreo de salida
                cout = (T - d_p + cin) // 10
                
                # Ganancia óptima de esta columna: P_p * floor(T/3) 
                ganancia = P_p * (T // 3)
                
                # Actualizar DP
                nueva_creatividad = dp_prev[cin] + ganancia
                if cout not in dp_curr or dp_curr[cout] < nueva_creatividad:
                    dp_curr[cout] = nueva_creatividad
        
        dp_prev = dp_curr
    
    # La respuesta está en dp_curr[0] (acarreo final debe ser 0)
    return dp_curr.get(0, 0)



def resolver_desde_stdin():
    """
    Resuelve el problema leyendo desde entrada estándar (stdin)
    Formato estándar para jueces:
    t
    k n P0 P1 P2 P3 P4
    k n P0 P1 P2 P3 P4
    ...
    """
    try:
        # Leer número de casos de prueba
        t = int(input().strip())
        
        for _ in range(t):
            # Leer k n P0 P1 P2 P3 P4 (todo en una línea)
            datos = list(map(int, input().strip().split()))
            k = datos[0]  # número de celdas
            n = datos[1]  # energía total
            valores_p = datos[2:]  # valores P0 P1 P2 P3 P4
            
            # Resolver y imprimir resultado
            resultado = resolver_festival_robots(n, k, valores_p)
            print(resultado)
            
    except EOFError:
        pass
    except Exception as e:
        pass


def resolver_desde_archivo(nombre_archivo):
    """
    Resuelve el problema leyendo desde un archivo
    Formato: k n P0 P1 P2 P3 P4 (todo en una línea por caso)
    """
    try:
        with open(nombre_archivo, 'r') as f:
            lineas = [line.strip() for line in f.readlines() if line.strip()]
        
        # Leer número de casos de prueba
        t = int(lineas[0])
        
        for i in range(1, t + 1):
            # Leer k n P0 P1 P2 P3 P4 (todo en una línea)
            datos = list(map(int, lineas[i].split()))
            k = datos[0]  # número de celdas
            n = datos[1]  # energía total
            valores_p = datos[2:]  # valores P0 P1 P2 P3 P4
            
            # Resolver y imprimir resultado
            resultado = resolver_festival_robots(n, k, valores_p)
            print(resultado)
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # Sin argumentos: leer desde stdin (para jueces automáticos)
        resolver_desde_stdin()
    elif len(sys.argv) == 2:
        # Con archivo: leer desde archivo (para testing local)
        archivo_entrada = sys.argv[1]
        resolver_desde_archivo(archivo_entrada)
    else:
        print("Uso:")
        print("  python ProyectoDalgo.py                 # Leer desde entrada estándar")
        print("  python ProyectoDalgo.py <archivo>       # Leer desde archivo")
        print("Ejemplo: python ProyectoDalgo.py test_input.txt")
        sys.exit(1)
