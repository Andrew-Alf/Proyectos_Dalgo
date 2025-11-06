#!/usr/bin/env python3
"""
Generador de Diagramas Visuales para el Algoritmo de Festival de Robots Creativos
Autor: Andrés Felipe Alfonso Gamba - 202210412
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

def crear_diagrama_dp_matriz(n=134, k=2, P=[5,3,1]):
    """Crea un diagrama de la matriz DP mostrando las transiciones de estado"""
    
    # Convertir n a dígitos
    if n == 0:
        digitos = [0]
    else:
        digitos = []
        temp_n = n
        while temp_n > 0:
            digitos.append(temp_n % 10)
            temp_n //= 10
    
    max_carry = (9 * k) // 10 + 5
    num_cols = len(digitos)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Dibujar matriz DP
    for col in range(num_cols + 1):  # +1 para estado inicial
        for carry in range(max_carry + 1):
            # Color basado en si el estado es alcanzable
            if col == 0 and carry == 0:
                color = 'lightgreen'  # Estado inicial
                text = '0'
            elif col == num_cols and carry == 0:
                color = 'lightblue'   # Estado final válido
                text = '?'
            elif col == num_cols and carry != 0:
                color = 'lightcoral'  # Estado final inválido
                text = '-1'
            else:
                color = 'lightyellow' # Estados intermedios
                text = '?'
            
            rect = Rectangle((col, carry), 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)
            ax.text(col + 0.5, carry + 0.5, text, ha='center', va='center', fontweight='bold')
    
    # Etiquetas
    ax.set_xlim(0, num_cols + 1)
    ax.set_ylim(0, max_carry + 1)
    ax.set_xlabel('Columnas (Dígitos de n)', fontsize=12)
    ax.set_ylabel('Acarreo', fontsize=12)
    ax.set_title(f'Matriz DP para n={n}, k={k}, P={P}', fontsize=14, fontweight='bold')
    
    # Agregar etiquetas de columnas
    for i in range(num_cols):
        ax.text(i + 1, max_carry + 0.5, f'd_{i}={digitos[i]}', ha='center', va='center')
    
    ax.text(0.5, max_carry + 0.5, 'Inicial', ha='center', va='center')
    ax.text(num_cols + 0.5, max_carry + 0.5, 'Final', ha='center', va='center')
    
    # Leyenda
    legend_elements = [
        mpatches.Patch(color='lightgreen', label='Estado Inicial'),
        mpatches.Patch(color='lightyellow', label='Estados Intermedios'),
        mpatches.Patch(color='lightblue', label='Estado Final Válido'),
        mpatches.Patch(color='lightcoral', label='Estados Finales Inválidos')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def crear_diagrama_tabla_puntuacion(k=2):
    """Crea un diagrama mostrando la función de puntuación"""
    
    max_T = 9 * k
    T_values = list(range(max_T + 1))
    scores = []
    
    # Calcular scores usando la misma lógica del código Java
    for T in T_values:
        q = T // 3
        r = T % 3
        s = (q + 2) // 3
        
        if r == 0 or s < k:
            score = q
        else:
            m = q % 3
            score = q - (1 if m == 1 else 2)
        scores.append(score)
    
    # Crear gráfico
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Gráfico de barras
    bars = ax1.bar(T_values, scores, color='skyblue', edgecolor='navy', alpha=0.7)
    ax1.set_xlabel('T (Suma total en columna)', fontsize=12)
    ax1.set_ylabel('Score(T)', fontsize=12)
    ax1.set_title(f'Función de Puntuación para k={k}', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Resaltar valores especiales
    for i, (T, score) in enumerate(zip(T_values, scores)):
        if T % 3 == 0:
            bars[i].set_color('lightgreen')
        elif score < T // 3:
            bars[i].set_color('lightcoral')
    
    # Tabla de valores
    ax2.axis('tight')
    ax2.axis('off')
    
    # Crear tabla en chunks para que sea legible
    chunk_size = 10
    table_data = []
    for i in range(0, len(T_values), chunk_size):
        chunk_T = T_values[i:i+chunk_size]
        chunk_scores = scores[i:i+chunk_size]
        table_data.append([f'T={t}' for t in chunk_T])
        table_data.append([f'{s}' for s in chunk_scores])
        table_data.append(['---'] * len(chunk_T))  # Separador
    
    if table_data:
        table = ax2.table(cellText=table_data, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)
    
    plt.tight_layout()
    return fig

def crear_diagrama_complejidad():
    """Crea un diagrama de análisis de complejidad"""
    
    k_values = np.array([1, 2, 3, 4, 5])
    n_values = np.array([10, 100, 1000, 10000, 100000])
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Gráfico 1: Complejidad vs k (n fijo)
    n_fixed = 1000
    complexity_k = k_values**2 * np.log10(n_fixed)
    ax1.plot(k_values, complexity_k, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('k (número de celdas)', fontsize=12)
    ax1.set_ylabel('Operaciones (k² × log n)', fontsize=12)
    ax1.set_title(f'Complejidad vs k (n={n_fixed})', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2: Complejidad vs n (k fijo)
    k_fixed = 3
    complexity_n = k_fixed**2 * np.log10(n_values)
    ax2.plot(n_values, complexity_n, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('n (energía total)', fontsize=12)
    ax2.set_ylabel('Operaciones (k² × log n)', fontsize=12)
    ax2.set_title(f'Complejidad vs n (k={k_fixed})', fontsize=14, fontweight='bold')
    ax2.set_xscale('log')
    ax2.grid(True, alpha=0.3)
    
    # Gráfico 3: Heatmap de complejidad
    K, N = np.meshgrid(k_values, n_values)
    complexity_2d = K**2 * np.log10(N)
    
    im = ax3.imshow(complexity_2d, cmap='YlOrRd', aspect='auto')
    ax3.set_xticks(range(len(k_values)))
    ax3.set_xticklabels(k_values)
    ax3.set_yticks(range(len(n_values)))
    ax3.set_yticklabels(n_values)
    ax3.set_xlabel('k (número de celdas)', fontsize=12)
    ax3.set_ylabel('n (energía total)', fontsize=12)
    ax3.set_title('Mapa de Calor: Complejidad', fontsize=14, fontweight='bold')
    plt.colorbar(im, ax=ax3)
    
    # Gráfico 4: Comparación Python vs Java
    test_cases = ['10 casos', '25 casos', '50 casos', '75 casos', '100 casos']
    python_times = [66.1, 331.0, 1653.8, 3720.0, 6624.0]  # Extrapolado
    java_times = [0.5, 2.7, 13.6, 30.6, 54.4]  # Extrapolado
    
    x = np.arange(len(test_cases))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, python_times, width, label='Python', color='lightcoral', alpha=0.8)
    bars2 = ax4.bar(x + width/2, java_times, width, label='Java', color='lightgreen', alpha=0.8)
    
    ax4.set_xlabel('Número de casos de prueba', fontsize=12)
    ax4.set_ylabel('Tiempo (segundos)', fontsize=12)
    ax4.set_title('Comparación de Rendimiento: Python vs Java', fontsize=14, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(test_cases)
    ax4.legend()
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3)
    
    # Agregar etiquetas de tiempo en las barras
    for bar in bars1:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}s', ha='center', va='bottom', fontsize=8)
    
    for bar in bars2:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}s', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    return fig

def crear_diagrama_flujo_algoritmo():
    """Crea un diagrama de flujo del algoritmo"""
    
    fig, ax = plt.subplots(figsize=(14, 18))
    
    # Definir posiciones de los elementos del flujo
    boxes = [
        {"text": "INICIO\nInput: n, k, P[]", "pos": (0.5, 0.95), "color": "lightgreen"},
        {"text": "Calcular maxCarry\n= (9×k)÷10 + 5", "pos": (0.5, 0.88), "color": "lightblue"},
        {"text": "Crear tabla de\npuntuación\nO(k) precálculo", "pos": (0.5, 0.81), "color": "lightblue"},
        {"text": "Convertir n a dígitos\n[d₀, d₁, ..., dₘ]", "pos": (0.5, 0.74), "color": "lightblue"},
        {"text": "Extender P[] con ceros\nsi es necesario", "pos": (0.5, 0.67), "color": "lightblue"},
        {"text": "Inicializar DP\ndp[0] = 0\nresto = -1", "pos": (0.5, 0.60), "color": "yellow"},
        {"text": "col = 0", "pos": (0.5, 0.53), "color": "orange"},
        {"text": "col < numDigitos?", "pos": (0.5, 0.46), "color": "pink"},
        {"text": "cin = 0", "pos": (0.2, 0.39), "color": "orange"},
        {"text": "cin ≤ maxCarry?", "pos": (0.2, 0.32), "color": "pink"},
        {"text": "dp[cin] == -1?", "pos": (0.2, 0.25), "color": "pink"},
        {"text": "Calcular rango\n[lo, hi] para cout", "pos": (0.2, 0.18), "color": "lightcyan"},
        {"text": "Para cada cout ∈ [lo,hi]:\n• T = dᵢ - cin + 10×cout\n• score = tabla[T]\n• ganancia = Pᵢ × score\n• actualizar dp[cout]", "pos": (0.2, 0.11), "color": "lightcyan"},
        {"text": "cin++", "pos": (0.2, 0.04), "color": "orange"},
        {"text": "col++", "pos": (0.8, 0.39), "color": "orange"},
        {"text": "RESULTADO\ndp[0]", "pos": (0.8, 0.25), "color": "lightgreen"},
    ]
    
    # Dibujar cajas
    for box in boxes:
        bbox = FancyBboxPatch((box["pos"][0]-0.08, box["pos"][1]-0.025), 0.16, 0.05,
                             boxstyle="round,pad=0.01", facecolor=box["color"],
                             edgecolor="black", linewidth=1)
        ax.add_patch(bbox)
        ax.text(box["pos"][0], box["pos"][1], box["text"], ha='center', va='center',
                fontsize=9, fontweight='bold')
    
    # Dibujar flechas (conexiones)
    arrows = [
        # Flujo principal hacia abajo
        ((0.5, 0.925), (0.5, 0.905)),
        ((0.5, 0.855), (0.5, 0.835)),
        ((0.5, 0.785), (0.5, 0.765)),
        ((0.5, 0.715), (0.5, 0.695)),
        ((0.5, 0.645), (0.5, 0.625)),
        ((0.5, 0.575), (0.5, 0.555)),
        ((0.5, 0.505), (0.5, 0.485)),
        
        # Rama SI del primer if
        ((0.45, 0.46), (0.25, 0.415)),
        ((0.2, 0.365), (0.2, 0.345)),
        ((0.2, 0.295), (0.2, 0.275)),
        ((0.2, 0.225), (0.2, 0.205)),
        ((0.2, 0.155), (0.2, 0.135)),
        ((0.2, 0.085), (0.2, 0.065)),
        
        # Vuelta del loop cin
        ((0.12, 0.04), (0.05, 0.04)),
        ((0.05, 0.04), (0.05, 0.32)),
        ((0.05, 0.32), (0.12, 0.32)),
        
        # Rama NO del primer if hacia col++
        ((0.55, 0.46), (0.75, 0.415)),
        ((0.8, 0.365), (0.8, 0.275)),
        
        # Vuelta del loop col
        ((0.8, 0.415), (0.9, 0.415)),
        ((0.9, 0.415), (0.9, 0.53)),
        ((0.9, 0.53), (0.58, 0.53)),
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='darkblue'))
    
    # Etiquetas de decisión
    ax.text(0.35, 0.48, 'SÍ', ha='center', va='center', fontsize=10, 
            fontweight='bold', color='green')
    ax.text(0.65, 0.48, 'NO', ha='center', va='center', fontsize=10, 
            fontweight='bold', color='red')
    ax.text(0.1, 0.34, 'SÍ', ha='center', va='center', fontsize=10, 
            fontweight='bold', color='green')
    ax.text(0.1, 0.27, 'NO', ha='center', va='center', fontsize=10, 
            fontweight='bold', color='red')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Diagrama de Flujo del Algoritmo DP\nFestival de Robots Creativos',
                fontsize=16, fontweight='bold', pad=20)
    
    return fig

def generar_todos_los_diagramas():
    """Genera todos los diagramas y los guarda como archivos PNG"""
    
    print("Generando diagramas visuales...")
    
    # Configurar estilo
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Generar cada diagrama
    diagramas = [
        ("matriz_dp", crear_diagrama_dp_matriz),
        ("tabla_puntuacion", crear_diagrama_tabla_puntuacion),
        ("complejidad", crear_diagrama_complejidad),
        ("flujo_algoritmo", crear_diagrama_flujo_algoritmo)
    ]
    
    for nombre, funcion in diagramas:
        try:
            print(f"Creando diagrama: {nombre}")
            fig = funcion()
            fig.savefig(f'diagrama_{nombre}.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
            print(f"✓ Guardado: diagrama_{nombre}.png")
        except Exception as e:
            print(f"✗ Error creando {nombre}: {e}")
    
    print("\n¡Diagramas generados exitosamente!")
    print("Archivos creados:")
    print("- diagrama_matriz_dp.png")
    print("- diagrama_tabla_puntuacion.png") 
    print("- diagrama_complejidad.png")
    print("- diagrama_flujo_algoritmo.png")

if __name__ == "__main__":
    generar_todos_los_diagramas()