# Proyecto Realizado por:
# Angela Jimenez - 202210989
# Andrés Felipe Alfonso Gamba - 202210412

def dsu_init(n):
    padre = list(range(n+1))
    tam = [1] * (n+1)
    return padre, tam

def dsu_find(padre, a):
    p = padre
    while p[a] != a:
        p[a] = p[p[a]]
        a = p[a]
    return a

def dsu_union(padre, tam, a, b):
    a = dsu_find(padre, a); b = dsu_find(padre, b)
    if a == b:
        return a
    if tam[a] < tam[b]:
        a, b = b, a
    padre[b] = a
    tam[a] += tam[b]
    return a

def process_case(n_nodos, aristas):
    dsu_fibra_padre, dsu_fibra_tam = dsu_init(n_nodos)
    dsu_coaxial_padre, dsu_coaxial_tam = dsu_init(n_nodos)

    mapF = {i: {i: 1} for i in range(1, n_nodos+1)}
    mapC = {i: {i: 1} for i in range(1, n_nodos+1)}

    badF = 0
    badC = 0

    respuestas = []

    def merge_f_nodes(x, y):
        nonlocal badF, badC
        fa = dsu_find(dsu_fibra_padre, x)
        fb = dsu_find(dsu_fibra_padre, y)
        if fa == fb:
            return
        if dsu_fibra_tam[fa] < dsu_fibra_tam[fb]:
            fa, fb = fb, fa
        dsu_union(dsu_fibra_padre, dsu_fibra_tam, fa, fb)

        MF_a = mapF.get(fa, {})
        MF_b = mapF.get(fb, {})

        if len(MF_a) > 1:
            badF -= 1
        if len(MF_b) > 1:
            badF -= 1

        for liderC, cnt in list(MF_b.items()):
            MC = mapC.get(liderC, {})
            antes = len(MC)
            MC.pop(fb, 0)
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
        ca = dsu_find(dsu_coaxial_padre, x)
        cb = dsu_find(dsu_coaxial_padre, y)
        if ca == cb:
            return
        if dsu_coaxial_tam[ca] < dsu_coaxial_tam[cb]:
            ca, cb = cb, ca
        dsu_union(dsu_coaxial_padre, dsu_coaxial_tam, ca, cb)

        MC_a = mapC.get(ca, {})
        MC_b = mapC.get(cb, {})

        if len(MC_a) > 1:
            badC -= 1
        if len(MC_b) > 1:
            badC -= 1

        for liderF, cnt in list(MC_b.items()):
            MF = mapF.get(liderF, {})
            antes = len(MF)

            MF.pop(cb, 0)
            MF[ca] = MF.get(ca, 0) + cnt

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
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else None
    if input_path:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = f.read().strip().split()
    else:
        data = sys.stdin.read().strip().split()
    if not data:
        sys.exit(0)

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
    if not output.endswith('\n'):
        output += '\n'
    sys.stdout.write(output)