# Proyecto Realizado por:
# Angela Jimenez - 202210989
# Andrés Felipe Alfonso Gamba - 202210412

class DSU:
    def __init__(self,n):
        self.padre=list(range(n+1))
        self.tam=[1]*(n+1)
    def buscar(self,a):
        p=self.padre
        while p[a]!=a:
            p[a]=p[p[a]]
            a=p[a]
        return a
    def unir(self,a,b):
        a=self.buscar(a); b=self.buscar(b)
        if a==b: return a
        if self.tam[a]<self.tam[b]: a,b=b,a
        self.padre[b]=a
        self.tam[a]+=self.tam[b]
        return a

def process_case(n_nodos, aristas):
    dsu_fibra = DSU(n_nodos)
    dsu_coaxial = DSU(n_nodos)
    respuestas = []
    for (a,b,tipo) in aristas:
        if tipo==1:
            dsu_fibra.unir(a,b)
        else:
            dsu_coaxial.unir(a,b)

        # escanear todos los nodos
        comp_fibra = [0]*(n_nodos+1)
        comp_coaxial = [0]*(n_nodos+1)
        for i in range(1,n_nodos+1):
            comp_fibra[i]=dsu_fibra.buscar(i)
            comp_coaxial[i]=dsu_coaxial.buscar(i)

        # Verificación biyectiva robusta: contar tuplas (repF,repC)
        pares = set((comp_fibra[i], comp_coaxial[i]) for i in range(1, n_nodos+1))
        lideres_f = set(comp_fibra[1:])
        lideres_c = set(comp_coaxial[1:])
        ok = (len(pares) == len(lideres_f) == len(lideres_c))
        respuestas.append(1 if ok else 0)
    return respuestas

if __name__ == '__main__':
    import sys, time, os, subprocess
    # soporte para pasar archivo de entrada opcional como argumento
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
    out=[]
    for _ in range(t_casos):
        n_nodos=int(next(iterador)); m_aristas=int(next(iterador))
        aristas=[]
        for _ in range(m_aristas):
            a=int(next(iterador)); b=int(next(iterador)); tipo=int(next(iterador))
            aristas.append((a,b,tipo))
        out.append(' '.join(str(x) for x in process_case(n_nodos, aristas)))
    output = '\n'.join(out)
    # Ensure stdout output ends with a single newline so the checker prints on its own line
    if not output.endswith('\n'):
        output += '\n'
    sys.stdout.write(output)
    elapsed = time.time() - start
    # Comentar acá abajo para quitar el tiempo en la entrega final
    # Print time without an extra leading newline
    print(f"# Time: {elapsed:.6f}s", file=sys.stderr)

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
    # Save file without a trailing blank line
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
