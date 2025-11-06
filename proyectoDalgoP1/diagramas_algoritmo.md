# Diagramas Explicativos del Algoritmo - Festival de Robots Creativos

## 1. Diagrama de Flujo General del Algoritmo

```
┌─────────────────┐
│  INICIO         │
│ Input: n, k, P  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Crear tabla de  │
│ puntuación      │
│ (precalculada)  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Convertir n a   │
│ dígitos         │
│ [d₀, d₁, ...,dₘ]│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Inicializar DP  │
│ dp[0] = 0       │
│ (acarreo 0)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Para cada       │
│ columna i       │
│ (0 → m-1)       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Para cada       │
│ acarreo cin     │
│ posible         │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Calcular rango  │
│ válido de cout  │
│ [lo, hi]        │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Para cada cout  │
│ en [lo, hi]:    │
│ T = dᵢ-cin+10*cout │
│ score = tabla[T]│
│ actualizar DP   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Siguiente       │
│ columna         │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ RESULTADO:      │
│ dp[0] final     │
│ (sin acarreo)   │
└─────────────────┘
```

## 2. Ejemplo Visual con n=134, k=2, P=[5,3,1]

### Representación de la suma:
```
    P₂ P₁ P₀     1  3  4  ← dígitos de n
  +  1  3  5  ← valores P extendidos
  ──────────
    ?  ?  ?
```

### Proceso columna por columna:

```
COLUMNA 0 (dígito más bajo):
d₀ = 4, P₀ = 5

cin=0: T = 4-0+10*0 = 4  → score = 1 → ganancia = 5*1 = 5
       cout = 0

Estado DP después:
dp[0] = 5

COLUMNA 1:
d₁ = 3, P₁ = 3

cin=0: T = 3-0+10*0 = 3  → score = 1 → ganancia = 3*1 = 3
       cout = 0
       dp[0] = 5 + 3 = 8

COLUMNA 2:
d₂ = 1, P₂ = 1

cin=0: T = 1-0+10*0 = 1  → score = 0 → ganancia = 1*0 = 0
       cout = 0
       dp[0] = 8 + 0 = 8

RESULTADO FINAL: 8
```

## 3. Diagrama de Estados DP

```
                COLUMNAS (dígitos de n)
                    0    1    2    ...
    A    ┌─────┬─────┬─────┬─────┬─────┐
    C  0 │  0  │  ?  │  ?  │  ?  │  0  │ ← Estado final válido
    A    ├─────┼─────┼─────┼─────┼─────┤
    R  1 │ -1  │  ?  │  ?  │  ?  │ -1  │
    R    ├─────┼─────┼─────┼─────┼─────┤
    E  2 │ -1  │  ?  │  ?  │  ?  │ -1  │
    O    ├─────┼─────┼─────┼─────┼─────┤
    S  3 │ -1  │  ?  │  ?  │  ?  │ -1  │
       ...└─────┴─────┴─────┴─────┴─────┘

Leyenda:
- 0: Estado inicial (columna 0, acarreo 0)
- ?: Estados calculados durante el proceso
- -1: Estados inalcanzables
- Flecha →: Dirección del procesamiento
```

## 4. Fórmulas Clave Visualizadas

### Cálculo de T (suma total en una columna):
```
T = dᵢ + cin + suma_robots = dᵢ - cin + 10*cout
    │    │        │               │
    │    │        └─ Valor que aportan los robots
    │    └─ Acarreo de entrada
    └─ Dígito objetivo de n
```

### Función de puntuación:
```
T → score(T):

Si T divisible por 3 y suficientes robots:
    score = T/3

Si no:
    score = (T/3) - penalización

Tabla precalculada para O(1) lookup
```

### Rango válido de cout:
```
lo = ⌈(cin - dᵢ + 9)/10⌉  ← Mínimo acarreo de salida
hi = ⌊(9k + cin - dᵢ)/10⌋  ← Máximo acarreo de salida

Garantiza: 0 ≤ suma_robots ≤ 9k
```

## 5. Diagrama de Complejidad

```
COMPLEJIDAD TEMPORAL:
┌─────────────────┐
│ Precálculo      │ O(k)
│ tabla scores    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ DP Principal:   │ O(log n × k² )
│ • log n cols    │
│ • k² transic.   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ TOTAL:          │ O(k² × log n)
│ ESPACIO:        │ O(k)
└─────────────────┘
```

## 6. Ejemplo de Tabla de Puntuación (k=2)

```
T  │ score(T) │ Explicación
───┼──────────┼─────────────────────────
0  │    0     │ T/3 = 0
1  │    0     │ No divisible por 3
2  │    0     │ No divisible por 3  
3  │    1     │ T/3 = 1
4  │    1     │ Penalización aplicada
5  │    1     │ Penalización aplicada
6  │    2     │ T/3 = 2
7  │    2     │ Penalización aplicada
8  │    2     │ Penalización aplicada
9  │    3     │ T/3 = 3
...│   ...    │ ...
18 │    6     │ T/3 = 6 (máximo para k=2)
```

## 7. Ventajas del Enfoque por Programación Dinámica

```
┌─────────────────┐    ┌─────────────────┐
│   ENFOQUE       │    │   ENFOQUE DP    │
│   INGENUO       │ VS │   OPTIMIZADO    │
├─────────────────┤    ├─────────────────┤
│ • Fuerza bruta  │    │ • Estados DP    │
│ • 10^(k×logn)   │    │ • O(k²×log n)   │
│ • Impracticable │    │ • Factible      │
│ • >27 minutos   │    │ • 13 segundos   │
└─────────────────┘    └─────────────────┘
```

Este conjunto de diagramas te ayudará a explicar tu algoritmo de manera visual y comprensible para tu presentación académica.