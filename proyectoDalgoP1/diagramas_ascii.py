#!/usr/bin/env python3
"""
Generador de Diagramas ASCII para el Algoritmo de Festival de Robots Creativos
Autor: Andrés Felipe Alfonso Gamba - 202210412

Esta versión no requiere librerías externas y genera diagramas en texto ASCII
"""

def crear_diagrama_ascii_dp(n=134, k=2, P=[5,3,1]):
    """Genera diagrama ASCII de la matriz DP"""
    
    # Convertir n a dígitos
    if n == 0:
        digitos = [0]
    else:
        digitos = []
        temp_n = n
        while temp_n > 0:
            digitos.append(temp_n % 10)
            temp_n //= 10
    
    max_carry = (9 * k) // 10 + 2  # Simplificado para visualización ASCII
    num_cols = len(digitos)
    
    print(f"\n{'='*60}")
    print(f"MATRIZ DP PARA n={n}, k={k}, P={P}")
    print(f"{'='*60}")
    
    # Encabezado
    header = "Carry │"
    for i in range(num_cols):
        header += f"  d{i}={digitos[i]} │"
    header += " Final │"
    
    print(header)
    print("─" * len(header))
    
    # Filas de la matriz
    for carry in range(max_carry, -1, -1):  # De arriba hacia abajo
        row = f"  {carry}   │"
        for col in range(num_cols + 1):  # +1 para columna final
            if col == 0 and carry == 0:
                cell = "   0  "  # Estado inicial
            elif col == num_cols and carry == 0:
                cell = "  RES "  # Resultado final
            elif col == num_cols and carry != 0:
                cell = "  -1  "  # Estado final inválido
            else:
                cell = "   ?  "  # Estados a calcular
            row += cell + "│"
        print(row)
    
    print("─" * len(header))
    print("Leyenda: 0=inicial, ?=a calcular, RES=resultado, -1=inválido\n")

def crear_tabla_puntuacion_ascii(k=2):
    """Genera tabla de puntuación en ASCII"""
    
    max_T = 9 * k
    print(f"\n{'='*50}")
    print(f"TABLA DE PUNTUACIÓN PARA k={k}")
    print(f"{'='*50}")
    print("│  T  │ Score │ Tipo        │ Fórmula        │")
    print("├─────┼───────┼─────────────┼────────────────┤")
    
    for T in range(min(max_T + 1, 20)):  # Limitar para visualización
        # Calcular score usando la lógica del algoritmo
        q = T // 3
        r = T % 3
        s = (q + 2) // 3
        
        if r == 0 or s < k:
            score = q
            tipo = "Divisible/3" if r == 0 else "Sufic.robots"
            formula = "T/3"
        else:
            m = q % 3
            score = q - (1 if m == 1 else 2)
            tipo = "Penalización"
            formula = f"T/3 - {1 if m == 1 else 2}"
        
        print(f"│ {T:2d}  │  {score:2d}   │ {tipo:11s} │ {formula:14s} │")
    
    if max_T > 19:
        print("│ ... │  ...  │ ...         │ ...            │")
    print("└─────┴───────┴─────────────┴────────────────┘\n")

def crear_diagrama_flujo_ascii():
    """Genera diagrama de flujo en ASCII"""
    
    print(f"\n{'='*60}")
    print("DIAGRAMA DE FLUJO DEL ALGORITMO")
    print(f"{'='*60}")
    
    flujo = """
    ┌─────────────────┐
    │     INICIO      │
    │ Input: n, k, P  │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │ Crear tabla de  │
    │   puntuación    │
    │   O(k) tiempo   │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │ Convertir n a   │
    │ dígitos [d₀,d₁] │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │ Inicializar DP  │
    │    dp[0] = 0    │
    └─────────┬───────┘
              │
              ▼
    ┌─────────────────┐
    │ Para cada       │◄─────────┐
    │ columna i       │          │
    └─────────┬───────┘          │
              │                  │
              ▼                  │
    ┌─────────────────┐          │
    │ Para cada       │◄─────┐   │
    │ acarreo cin     │      │   │
    └─────────┬───────┘      │   │
              │              │   │
              ▼              │   │
    ┌─────────────────┐      │   │
    │ Calcular rango  │      │   │
    │ [lo, hi] cout   │      │   │
    └─────────┬───────┘      │   │
              │              │   │
              ▼              │   │
    ┌─────────────────┐      │   │
    │ Para cout en    │      │   │
    │ [lo,hi]:        │      │   │
    │ • T=dᵢ-cin+10×cout    │   │
    │ • score=tabla[T]│      │   │
    │ • actualizar DP │      │   │
    └─────────┬───────┘      │   │
              │              │   │
              └──────────────┘   │
              │                  │
              └──────────────────┘
              │
              ▼
    ┌─────────────────┐
    │   RESULTADO:    │
    │     dp[0]       │
    └─────────────────┘
    """
    
    print(flujo)

def simular_ejecucion_ejemplo(n=23, k=2, P=[4,2]):
    """Simula paso a paso la ejecución del algoritmo"""
    
    print(f"\n{'='*70}")
    print(f"SIMULACIÓN PASO A PASO: n={n}, k={k}, P={P}")
    print(f"{'='*70}")
    
    # Convertir n a dígitos
    if n == 0:
        digitos = [0]
    else:
        digitos = []
        temp_n = n
        while temp_n > 0:
            digitos.append(temp_n % 10)
            temp_n //= 10
    
    print(f"1. PREPARACIÓN:")
    print(f"   n = {n} → dígitos = {digitos} (little-endian)")
    print(f"   k = {k} → max_carry = {(9*k)//10}")
    print(f"   P = {P}")
    
    # Crear tabla de puntuación (simplificada)
    max_T = 9 * k
    tabla_score = {}
    for T in range(max_T + 1):
        q = T // 3
        r = T % 3
        s = (q + 2) // 3
        
        if r == 0 or s < k:
            tabla_score[T] = q
        else:
            m = q % 3
            tabla_score[T] = q - (1 if m == 1 else 2)
    
    print(f"\n2. TABLA DE PUNTUACIÓN (primeros valores):")
    for i in range(min(10, max_T + 1)):
        print(f"   T={i} → score={tabla_score[i]}")
    
    # Simulación DP
    max_carry = (9 * k) // 10 + 1
    dp = [-1] * (max_carry + 1)
    dp[0] = 0  # Estado inicial
    
    print(f"\n3. PROCESO DP:")
    print(f"   Estado inicial: dp = {dp}")
    
    for col in range(len(digitos)):
        print(f"\n   COLUMNA {col} (d_{col} = {digitos[col]}, P_{col} = {P[col] if col < len(P) else 0}):")
        
        dp_nuevo = [-1] * (max_carry + 1)
        
        for cin in range(max_carry + 1):
            if dp[cin] == -1:
                continue
                
            # Calcular rango válido de cout
            d_p = digitos[col]
            lo = max(0, (cin - d_p + 9) // 10)
            hi = min(max_carry, (9 * k + cin - d_p) // 10)
            
            print(f"     cin={cin} (valor={dp[cin]}): rango cout=[{lo},{hi}]")
            
            for cout in range(lo, hi + 1):
                T = d_p - cin + 10 * cout
                if T in tabla_score:
                    score = tabla_score[T]
                    P_val = P[col] if col < len(P) else 0
                    ganancia = P_val * score
                    nuevo_valor = dp[cin] + ganancia
                    
                    if dp_nuevo[cout] == -1 or dp_nuevo[cout] < nuevo_valor:
                        dp_nuevo[cout] = nuevo_valor
                        print(f"       cout={cout}: T={T}, score={score}, ganancia={ganancia}, total={nuevo_valor}")
        
        dp = dp_nuevo
        print(f"   Estado después: dp = {dp}")
    
    resultado = dp[0] if dp[0] != -1 else 0
    print(f"\n4. RESULTADO FINAL: {resultado}")
    print(f"   (valor en dp[0] = sin acarreo final)")

def generar_comparacion_rendimiento():
    """Genera tabla de comparación de rendimiento"""
    
    print(f"\n{'='*80}")
    print("ANÁLISIS DE RENDIMIENTO: PYTHON vs JAVA")
    print(f"{'='*80}")
    
    print("┌────────────────┬─────────────────┬─────────────────┬──────────────┐")
    print("│ Casos de Prueba│  Python (seg)   │   Java (seg)    │ Factor Mejora│")
    print("├────────────────┼─────────────────┼─────────────────┼──────────────┤")
    print("│       10       │      66.1       │       0.5       │     132x     │")
    print("│       25       │     331.0       │       2.7       │     123x     │")
    print("│       50       │    1653.8       │      13.6       │     121x     │")
    print("│       75       │    3720.0*      │      30.6*      │     122x     │")
    print("│      100       │    6624.0*      │      54.4*      │     122x     │")
    print("└────────────────┴─────────────────┴─────────────────┴──────────────┘")
    print("* Valores extrapolados")
    
    print(f"\nCOMPLEJIDAD TEÓRICA:")
    print(f"  Temporal: O(k² × log n)")
    print(f"  Espacial: O(k)")
    
    print(f"\nOPTIMIZACIONES IMPLEMENTADAS:")
    print(f"  ✓ Tabla de puntuación precalculada")
    print(f"  ✓ Arrays en lugar de diccionarios")
    print(f"  ✓ Cálculo optimizado de rangos")
    print(f"  ✓ Eliminación de estados inalcanzables")
    print(f"  ✓ Traducción a Java para mejor rendimiento")

def menu_principal():
    """Menú principal para generar diferentes diagramas"""
    
    while True:
        print(f"\n{'='*60}")
        print("GENERADOR DE DIAGRAMAS - FESTIVAL DE ROBOTS CREATIVOS")
        print(f"{'='*60}")
        print("1. Diagrama de matriz DP")
        print("2. Tabla de puntuación")
        print("3. Diagrama de flujo")
        print("4. Simulación paso a paso")
        print("5. Comparación de rendimiento")
        print("6. Generar todos los diagramas")
        print("0. Salir")
        
        try:
            opcion = input("\nSeleccione una opción (0-6): ").strip()
            
            if opcion == "0":
                print("¡Hasta pronto!")
                break
            elif opcion == "1":
                n = int(input("Ingrese n (default 134): ") or "134")
                k = int(input("Ingrese k (default 2): ") or "2")
                crear_diagrama_ascii_dp(n, k)
            elif opcion == "2":
                k = int(input("Ingrese k (default 2): ") or "2")
                crear_tabla_puntuacion_ascii(k)
            elif opcion == "3":
                crear_diagrama_flujo_ascii()
            elif opcion == "4":
                n = int(input("Ingrese n (default 23): ") or "23")
                k = int(input("Ingrese k (default 2): ") or "2")
                P_str = input("Ingrese P como lista [4,2] (default): ") or "[4,2]"
                P = eval(P_str)  # Cuidado: solo para demo
                simular_ejecucion_ejemplo(n, k, P)
            elif opcion == "5":
                generar_comparacion_rendimiento()
            elif opcion == "6":
                crear_diagrama_ascii_dp()
                crear_tabla_puntuacion_ascii()
                crear_diagrama_flujo_ascii()
                simular_ejecucion_ejemplo()
                generar_comparacion_rendimiento()
            else:
                print("Opción inválida. Intente de nuevo.")
                
        except KeyboardInterrupt:
            print("\n¡Hasta pronto!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Intente de nuevo.")

if __name__ == "__main__":
    print("Generador de Diagramas ASCII para Festival de Robots Creativos")
    print("Autor: Andrés Felipe Alfonso Gamba - 202210412")
    menu_principal()