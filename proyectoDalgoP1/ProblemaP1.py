#Proyecto Realizado por:
#Angela Jimenez Gonzalez - 202210989
#Andrés Felipe Alfonso Gamba - 202210412

import time

def max_carry_real(k):
    """Calcula el acarreo máximo real posible"""
    return (9 * k) // 10

def crear_tabla_score(k, max_T):
    """Precalcula score_col para todos los T posibles"""
    tabla = [0] * (max_T + 1)  # Usar array para O(1) acceso
    for T in range(max_T + 1):
        q, r = divmod(T, 3)
        s = (q + 2) // 3
        if r == 0 or s < k:
            tabla[T] = q
        else:
            m = q % 3
            tabla[T] = q - (1 if m == 1 else 2)
    return tabla


def resolver_festival_robots(n, k, valores_p):
    # Precalcular tabla de score_col para O(1) lookup
    max_T = 9 * k
    tabla_score = crear_tabla_score(k, max_T)
    
    # Calcular límite preciso de acarreo con margen de seguridad
    max_carry = max_carry_real(k) + 5
    
    # Convertir n a dígitos (de derecha a izquierda: unidades, decenas, ...)
    digitos_n = []
    temp_n = n
    while temp_n > 0:
        digitos_n.append(temp_n % 10)
        temp_n //= 10
    
    # Si n = 0, caso especial
    if not digitos_n:
        digitos_n = [0]
    
    num_digitos = len(digitos_n)
    
    # Extender valores_p con ceros si es necesario
    if len(valores_p) < num_digitos:
        valores_p = valores_p + [0] * (num_digitos - len(valores_p))
    
    # DP usando arrays: -1 indica estado inalcanzable
    dp_prev = [-1] * (max_carry + 1)
    dp_prev[0] = 0  # Caso base: columna 0, acarreo 0
    
    # Procesar cada columna
    for col in range(num_digitos):
        dp_curr = [-1] * (max_carry + 1)
        d_p = digitos_n[col]
        P_p = valores_p[col]
        
        # Para cada acarreo de entrada alcanzable
        for cin in range(max_carry + 1):
            if dp_prev[cin] == -1:  # Estado inalcanzable
                continue
            
            # NUEVA IMPLEMENTACIÓN: Iterar sobre cout en lugar de T
            # Calcular rango de cout válidos usando techo entero
            lo = (cin - d_p + 9) // 10
            if lo < 0:
                lo = 0
            hi = min(max_carry, (9 * k + cin - d_p) // 10)
            
            for cout in range(lo, hi + 1):
                # Calcular T correspondiente (garantizado en rango [0, 9*k])
                T = d_p - cin + 10 * cout
                
                # Calcular ganancia usando tabla precalculada
                ganancia = P_p * tabla_score[T]
                
                # Actualizar DP
                nueva_creatividad = dp_prev[cin] + ganancia
                if dp_curr[cout] == -1 or dp_curr[cout] < nueva_creatividad:
                    dp_curr[cout] = nueva_creatividad
        
        dp_prev = dp_curr
    
    # La respuesta está en dp_curr[0] (acarreo final debe ser 0)
    return dp_prev[0] if dp_prev[0] != -1 else 0


if __name__ == "__main__":
    import sys
    
    tiempo_inicio = time.time()
    
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
    
    tiempo_total = time.time() - tiempo_inicio
    print(f"Tiempo: {tiempo_total:.6f}s", file=sys.stderr)
