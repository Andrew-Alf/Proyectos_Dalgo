def score_col(T, k):
    q, r = divmod(T, 3)          # q = puntos teóricos, r = sobrante (0..2)
    s = (q + 2) // 3             # mín # de dígitos premiados (cada uno da ≤3)
    if r == 0 or s < k:
        return q                 # hay al menos un dígito "no premiado" que absorbe el sobrante
    # r > 0 y s == k: todos los k dígitos ya son 3/6/9, no hay dónde poner el sobrante
    m = q % 3
    return q - (1 if m == 1 else 2)  # degradar un 3→4/5 (-1) o un 6→7/8 (-2)


def resolver_festival_robots(n, k, valores_p):

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
    dp_prev = {0: 0}  # Caso base: columna 0, acarreo 0
    dp_curr = {}
    
    # Procesar cada columna
    for col in range(num_columnas):
        dp_curr = {}
        d_p = digitos_n[col]
        P_p = valores_p[col] if col < len(valores_p) else 0
        
        # Para cada acarreo de entrada alcanzable
        for cin in dp_prev:
            # Probar todas las sumas T posibles en esta columna
            # T debe satisfacer: T ≡ d_p - cin (mod 10) y 0 ≤ T ≤ 9*k
            target_mod = (d_p - cin) % 10
            
            for T in range(target_mod, 9 * k + 1, 10):
                # Calcular acarreo de salida
                cout = (T - d_p + cin) // 10
                
                # Ganancia óptima de esta columna usando score_col
                ganancia = P_p * score_col(T, k)
                
                # Actualizar DP
                nueva_creatividad = dp_prev[cin] + ganancia
                if cout not in dp_curr or dp_curr[cout] < nueva_creatividad:
                    dp_curr[cout] = nueva_creatividad
        
        dp_prev = dp_curr
    
    # La respuesta está en dp_curr[0] (acarreo final debe ser 0)
    return dp_curr.get(0, 0)


if __name__ == "__main__":
    import sys
    
    input = sys.stdin.read
    data = input().strip().split('\n')
    
    num_casos = int(data[0].strip())
    index = 1
    
    for i in range(num_casos):
        # Leer k n P0 P1 P2 P3 P4 (todo en una línea)
        datos = list(map(int, data[index].strip().split()))
        k = datos[0]  # número de celdas
        n = datos[1]  # energía total
        valores_p = datos[2:]  # valores P0 P1 P2 P3 P4
        index += 1
        
        resultado = resolver_festival_robots(n, k, valores_p)
        print(resultado)
