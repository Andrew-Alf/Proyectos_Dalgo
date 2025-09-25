def score_col_optimizado(T, k, tabla_score):
    """Versión optimizada usando tabla precalculada"""
    return tabla_score.get(T, 0)

def resolver_festival_robots_optimizado(n, k, valores_p):
    # Precalcular tabla de score_col
    max_T = 9 * k
    tabla_score = {}
    for T in range(max_T + 1):
        q, r = divmod(T, 3)
        s = (q + 2) // 3
        if r == 0 or s < k:
            tabla_score[T] = q
        else:
            m = q % 3
            tabla_score[T] = q - (1 if m == 1 else 2)
    
    # Convertir n a dígitos
    digitos_n = []
    temp_n = n
    while temp_n > 0:
        digitos_n.append(temp_n % 10)
        temp_n //= 10
    
    if not digitos_n:
        digitos_n = [0]
    
    num_columnas = len(digitos_n)
    
    # Usar array en lugar de dict para mejor rendimiento
    max_carry = (9 * k) // 10 + 1
    dp_prev = [-1] * (max_carry + 1)
    dp_prev[0] = 0
    
    for col in range(num_columnas):
        dp_curr = [-1] * (max_carry + 1)
        d_p = digitos_n[col]
        P_p = valores_p[col] if col < len(valores_p) else 0
        
        for cin in range(max_carry + 1):
            if dp_prev[cin] == -1:
                continue
                
            target_mod = (d_p - cin) % 10
            
            for T in range(target_mod, max_T + 1, 10):
                cout = (T - d_p + cin) // 10
                if cout > max_carry:
                    continue
                    
                ganancia = P_p * tabla_score[T]
                nueva_creatividad = dp_prev[cin] + ganancia
                
                if dp_curr[cout] < nueva_creatividad:
                    dp_curr[cout] = nueva_creatividad
        
        dp_prev = dp_curr
    
    return dp_prev[0] if dp_prev[0] != -1 else 0