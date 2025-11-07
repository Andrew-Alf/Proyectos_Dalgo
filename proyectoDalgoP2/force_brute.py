# Proyecto Realizado por:
# Angela Jimenez - 202210989
# Andrés Felipe Alfonso Gamba - 202210412

from collections import deque, defaultdict

def comps_from_adj(n_nodos, ady):
    comp = [0]*(n_nodos+1)
    cid = 0
    for i in range(1, n_nodos+1):
        if comp[i]==0:
            cid += 1
            q = deque([i])
            comp[i]=cid
            while q:
                nodo = q.popleft()
                for vecino in ady[nodo]:
                    if comp[vecino]==0:
                        comp[vecino]=cid
                        q.append(vecino)
    return comp

def process_case(n_nodos, aristas):
    # aristas: lista de tuplas (a,b,tipo) con tipo==1 fibra, tipo==2 coaxial
    adj_fibra = [[] for _ in range(n_nodos+1)]
    adj_coaxial = [[] for _ in range(n_nodos+1)]
    respuestas = []
    for (a,b,tipo) in aristas:
        if tipo==1:
            adj_fibra[a].append(b)
            adj_fibra[b].append(a)
        else:
            adj_coaxial[a].append(b)
            adj_coaxial[b].append(a)

        comp_fibra = comps_from_adj(n_nodos, adj_fibra)
        comp_coaxial = comps_from_adj(n_nodos, adj_coaxial)

        # comprobar biyección entre particiones de forma robusta:
        # construir el conjunto de tuplas (repF, repC) para todos los nodos
        pares = set((comp_fibra[i], comp_coaxial[i]) for i in range(1, n_nodos+1))
        lideres_f = set(comp_fibra[1:])
        lideres_c = set(comp_coaxial[1:])
        # la condición biyectiva se cumple si el número de tuplas distintas es igual
        # al número de líderes de fibra y al número de líderes de coaxial
        ok = (len(pares) == len(lideres_f) == len(lideres_c))
        respuestas.append(1 if ok else 0)
    return respuestas

if __name__ == '__main__':
    import sys, time, os, subprocess
    # Si se pasa un argumento, lo usamos como archivo de entrada (para obtener el nombre base)
    input_path = sys.argv[1] if len(sys.argv) > 1 else None
    if input_path:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = f.read().strip().split()
        base = os.path.splitext(os.path.basename(input_path))[0]
    else:
        data = sys.stdin.read().strip().split()
        base = 'stdin'
    if not data:
        sys.exit(0)
    start = time.time()
    iterador = iter(data)
    t_casos = int(next(iterador))
    out_lines = []
    for _ in range(t_casos):
        n_nodos = int(next(iterador)); m_aristas = int(next(iterador))
        aristas = []
        for _ in range(m_aristas):
            a = int(next(iterador)); b = int(next(iterador)); tipo = int(next(iterador))
            aristas.append((a,b,tipo))
        out_lines.append(' '.join(str(x) for x in process_case(n_nodos, aristas)))
    output = '\n'.join(out_lines)
    # Ensure stdout output ends with newline so checker prints on its own line
    if not output.endswith('\n'):
        output += '\n'
    sys.stdout.write(output)
    elapsed = time.time() - start
    # Comentar acá abajo para quitar el tiempo en la entrega final
    print(f"# Time: {elapsed:.6f}s", file=sys.stderr)

    # Comentar acá abajo para quitar la prueba en la entrega final
    # Guardar la salida en Tests/Arrojadas/<base>A.txt (prefiere carpeta con mayúscula si existe)
    repo_dir = os.path.dirname(__file__)
    candidate_root = None
    for cand in ('Tests', 'tests'):
        path = os.path.join(repo_dir, cand)
        if os.path.isdir(path):
            candidate_root = path
            break
    if candidate_root is None:
        candidate_root = os.path.join(repo_dir, 'Tests')
    arrojadas_dir = os.path.join(candidate_root, 'Arrojadas')
    esperadas_dir = os.path.join(candidate_root, 'Esperadas')
    pruebas_dir = os.path.join(candidate_root, 'Pruebas')
    os.makedirs(arrojadas_dir, exist_ok=True)
    salida_path = os.path.join(arrojadas_dir, f"{base}A.txt")
    # Save file without trailing blank line
    file_output = output.rstrip('\n')
    with open(salida_path, 'w', encoding='utf-8') as f:
        f.write(file_output)

    # Comentar acá abajo para quitar la prueba en la entrega final
    revisar = os.path.join(candidate_root, 'RevisarRTAs.py')
    esperado_path = os.path.join(esperadas_dir, f"{base}E.txt")
    if os.path.exists(revisar) and os.path.exists(esperado_path):
        try:
            p = subprocess.run([sys.executable, revisar, salida_path, esperado_path], capture_output=True, text=True)
            res = p.stdout.strip()
            if res:
                print(res)
        except Exception as e:
            print(f"Error al ejecutar el comprobador: {e}", file=sys.stderr)
