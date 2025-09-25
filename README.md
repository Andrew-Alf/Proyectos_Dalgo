# Festival de los Robots Creativos - Documentación

## Descripción del Problema

En la ciudad futurista de Tecnotown, se celebra anualmente el Festival de los Robots Creativos. El desafío consiste en que cada robot debe distribuir una cantidad total de energía `n` en exactamente `k` celdas, de modo que la suma de las energías asignadas a cada celda sea igual al total de energía `n`.

## Reglas de Creatividad

- Solo se consideran creativos los dígitos **3, 6 y 9**
- La puntuación depende del dígito y su posición según la tabla:

| Dígito | Posición 1 (P₀) | Posición 10 (P₁) | Posición 100 (P₂) | Posición 1000 (P₃) | Posición 10000 (P₄) |
|--------|-----------------|------------------|-------------------|---------------------|---------------------|
| 3      | P₀              | P₁               | P₂                | P₃                  | P₄                  |
| 6      | 2P₀             | 2P₁              | 2P₂               | 2P₃                 | 2P₄                 |
| 9      | 3P₀             | 3P₁              | 3P₂               | 3P₃                 | 3P₄                 |

## Formato de Entrada y Salida

### Entrada
```
<número_de_casos>
<k1> <n1>
<P0> <P1> <P2> <P3> <P4>
<k2> <n2>
<P0> <P1> <P2> <P3> <P4>
...
```

Donde:
- `k`: número de celdas (1 ≤ k ≤ 10²)
- `n`: energía total a distribuir (1 ≤ n ≤ 10⁵)
- `P0, P1, P2, P3, P4`: valores de creatividad para cada posición (1 ≤ Pi ≤ 10⁵)

### Salida
Una línea por caso con la **máxima creatividad posible**.

## Ejemplo

### Entrada
```
3
2 15
1 2 3 4 5
2 57
1 2 3 4 5
3 600
3 1 2 4 3
```

### Salida
```
5
5
26
```

### Explicación del primer caso:
- **Energía total:** 15
- **Celdas:** 2
- **Valores P:** [1, 2, 3, 4, 5]
- **Asignaciones óptimas:** (6, 9) o (9, 6)
- **Cálculo para (6, 9):**
  - 6 → dígito 6 en posición 0: 2 × P₀ = 2 × 1 = 2
  - 9 → dígito 9 en posición 0: 3 × P₀ = 3 × 1 = 3
  - **Total:** 2 + 3 = 5

## Solución Implementada

### Algoritmo Principal: Programación Dinámica
- **Estado:** `dp[i][j]` = máxima creatividad usando `i` energía en `j` celdas
- **Complejidad temporal:** O(n² × k)
- **Complejidad espacial:** O(n × k)

### Funciones Auxiliares
1. **calcular_creatividad(numero, valores_p)**: Calcula la creatividad de un número
2. **obtener_todas_las_asignaciones_optimas()**: Encuentra todas las asignaciones óptimas
3. **resolver_desde_archivo()**: Lee casos desde archivo
4. **resolver_desde_stdin()**: Lee desde entrada estándar

## Modos de Uso

```bash
# Casos de prueba predeterminados
python ProyectoDalgo.py

# Leer desde archivo
python ProyectoDalgo.py archivo.txt

# Leer desde entrada estándar (jueces en línea)
python ProyectoDalgo.py --stdin

# Modo interactivo
python ProyectoDalgo.py --interactive
```

## Ejemplos de Cálculo

### Número 613 con P = [1, 2, 3, 4, 5]
- Dígito 6 en posición 2 (centenas): 2 × P₂ = 2 × 3 = 6
- Dígito 1 en posición 1 (decenas): 0 (no creativo)
- Dígito 3 en posición 0 (unidades): 1 × P₀ = 1 × 1 = 1
- **Total:** 6 + 1 = 7

### Asignación (33, 66) con P = [1, 2, 3, 4, 5]
- 33: 3×P₀ + 3×P₁ = 1×1 + 1×2 = 3
- 66: 2×P₀ + 2×P₁ = 2×1 + 2×2 = 6
- **Total:** 3 + 6 = 9

## Complejidad

- **Tiempo:** O(n² × k) por caso de prueba
- **Espacio:** O(n × k) para la tabla de programación dinámica
- **Casos límite manejados:** n ≤ 10⁵, k ≤ 10²

## Autor
Tu nombre aquí - Septiembre 2025