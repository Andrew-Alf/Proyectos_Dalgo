# Optimización 1: Loop T más eficiente
def resolver_optimizado_v1(n, k, valores_p):
    # Convertir n a dígitos
    digitos_n = []
    temp_n = n
    while temp_n > 0:
        digitos_n.append(temp_n % 10)
        temp_n //= 10
    
    if not digitos_n:
        digitos_n = [0]
    
    num_columnas = len(digitos_n)
    dp_prev = {0: 0}
    
    for col in range(num_columnas):
        dp_curr = {}
        d_p = digitos_n[col]
        P_p = valores_p[col] if col < len(valores_p) else 0
        
        for cin in dp_prev:
            target_mod = (d_p - cin) % 10
            
            # Precalcular todos los T válidos de una vez
            max_T = 9 * k
            T_values = list(range(target_mod, max_T + 1, 10))
            
            for T in T_values:
                cout = (T - d_p + cin) // 10
                ganancia = P_p * score_col(T, k)
                nueva_creatividad = dp_prev[cin] + ganancia
                
                if cout not in dp_curr or dp_curr[cout] < nueva_creatividad:
                    dp_curr[cout] = nueva_creatividad
        
        dp_prev = dp_curr
    
    return dp_curr.get(0, 0)