# Proyecto Realizado por:
# Angela Jimenez - 202210989
# Andrés Felipe Alfonso Gamba - 202210412

from collections import defaultdict

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
    # Inicializar DSUs
    dsu_fibra = DSU(n_nodos)
    dsu_coaxial = DSU(n_nodos)

    # mapF: líderF -> (dict líderC -> count)
    # mapC: líderC -> (dict líderF -> count)
    mapF = {i: {i: 1} for i in range(1, n_nodos+1)}
    mapC = {i: {i: 1} for i in range(1, n_nodos+1)}

    # contadores globales: cuántos líderes tienen más de un mapeo
    badF = 0
    badC = 0

    respuestas = []

    def merge_f_nodes(x, y):
        nonlocal badF, badC
        fa = dsu_fibra.buscar(x)
        fb = dsu_fibra.buscar(y)
        if fa == fb:
            return
        # ensure fa is the larger
        if dsu_fibra.tam[fa] < dsu_fibra.tam[fb]:
            fa, fb = fb, fa
        # perform union
        dsu_fibra.unir(fa, fb)

        MF_a = mapF.get(fa, {})
        MF_b = mapF.get(fb, {})

        # adjust badF for previous states
        if len(MF_a) > 1:
            badF -= 1
        if len(MF_b) > 1:
            badF -= 1

        # merge MF_b into MF_a
        for liderC, cnt in list(MF_b.items()):
            MC = mapC.get(liderC, {})
            antes = len(MC)
            # remove fb entry from MC
            val_fb = MC.pop(fb, 0)
            # add cnt to fa in MC
            MC[fa] = MC.get(fa, 0) + cnt
            despues = len(MC)
            if antes > 1 and despues <= 1:
                badC -= 1
            elif antes <= 1 and despues > 1:
                badC += 1
            mapC[liderC] = MC

            MF_a[liderC] = MF_a.get(liderC, 0) + cnt

        mapF[fa] = MF_a
        mapF[fb] = {}

        if len(MF_a) > 1:
            badF += 1

    def merge_c_nodes(x, y):
        nonlocal badF, badC
        ca = dsu_coaxial.buscar(x)
        cb = dsu_coaxial.buscar(y)
        if ca == cb:
            return
        if dsu_coaxial.tam[ca] < dsu_coaxial.tam[cb]:
            ca, cb = cb, ca
        dsu_coaxial.unir(ca, cb)

        MC_a = mapC.get(ca, {})
        MC_b = mapC.get(cb, {})

        if len(MC_a) > 1:
            badC -= 1
        if len(MC_b) > 1:
            badC -= 1

        for liderF, cnt in list(MC_b.items()):
            MF = mapF.get(liderF, {})
            antes = len(MF)

            # remove cb entry from MF (if any) and add to ca
            val_cb = MF.pop(cb, 0)
            MF[ca] = MF.get(ca, 0) + cnt

            # update mapC entries
            MCa = mapC.get(ca, {})
            MCa[liderF] = MCa.get(liderF, 0) + cnt
            MCb = mapC.get(cb, {})
            if liderF in MCb:
                if MCb[liderF] <= cnt:
                    del MCb[liderF]
                else:
                    MCb[liderF] = MCb[liderF] - cnt

            despues = len(MF)
            if antes > 1 and despues <= 1:
                badF -= 1
            elif antes <= 1 and despues > 1:
                badF += 1

            mapF[liderF] = MF
            mapC[ca] = MCa
            mapC[cb] = MCb

        mapC[ca] = mapC.get(ca, {})
        mapC[cb] = {}
        if len(mapC[ca]) > 1:
            badC += 1

    for (a,b,tipo) in aristas:
        if tipo == 1:
            merge_f_nodes(a, b)
        else:
            merge_c_nodes(a, b)

        respuestas.append(1 if (badF == 0 and badC == 0) else 0)
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
    out_lines = []
    for _ in range(t_casos):
        n_nodos = int(next(iterador)); m_aristas = int(next(iterador))
        aristas = []
        for _ in range(m_aristas):
            a = int(next(iterador)); b = int(next(iterador)); tipo = int(next(iterador))
            aristas.append((a,b,tipo))
        out_lines.append(' '.join(str(x) for x in process_case(n_nodos, aristas)))
    output = '\n'.join(out_lines)
    # Asegurar que la salida termine en newline para que el comprobador se imprima
    # en una línea separada y no quede pegado al último token.
    if not output.endswith('\n'):
        output += '\n'
    sys.stdout.write(output)
    elapsed = time.time() - start
    # Comentar acá abajo para quitar el tiempo en la entrega final
    # Imprimir la línea de tiempo sin newline inicial extra (sin espacio al inicio)
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
    # Para evitar una fila en blanco final en el archivo guardado, eliminamos
    # el salto de línea final antes de escribir en el archivo. Sin embargo,
    # dejamos la versión con newline para stdout (ya garantizada arriba)
    file_output = output.rstrip('\n')
    with open(salida_path, 'w', encoding='utf-8') as f:
        f.write(file_output)

    # Comentar acá abajo para quitar la prueba en la entrega final
    revisar = os.path.join(candidate_root, 'RevisarRTAs.py')
    esperado_path = os.path.join(esperadas_dir, f"{base}E.txt")
    if os.path.exists(revisar) and os.path.exists(esperado_path):
        try:
            p = subprocess.run([sys.executable, revisar, salida_path, esperado_path], capture_output=True, text=True)
            # Mostrar el resultado del comprobador en su propia línea.
            res = p.stdout.strip()
            if res:
                print(res)
        except Exception as e:
            print(f"Error al ejecutar el comprobador: {e}", file=sys.stderr)