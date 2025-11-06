#!/usr/bin/env python3
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

        # comprobar biyección entre particiones: comp_fibra[i]==comp_fibra[j] iff comp_coaxial[i]==comp_coaxial[j]
        ok = True
        mapeo = {}
        mapeados = set()
        for i in range(1, n_nodos+1):
            x = comp_fibra[i]
            y = comp_coaxial[i]
            if x in mapeo:
                if mapeo[x] != y:
                    ok = False
                    break
            else:
                mapeo[x] = y
                if y in mapeados:
                    # posible conflicto detectado arriba
                    pass
                mapeados.add(y)
        respuestas.append(1 if ok else 0)
    return respuestas

if __name__ == '__main__':
    import sys, time
    data = sys.stdin.read().strip().split()
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
    sys.stdout.write('\n'.join(out_lines))
    elapsed = time.time() - start
    # Comentar acá abajo para quitar el tiempo en la entrega final
    print(f"# Time: {elapsed:.6f}s", file=sys.stderr)
