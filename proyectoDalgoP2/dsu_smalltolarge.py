#!/usr/bin/env python3
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
    # Inicializar DSUs y conjuntos de vecinos
    dsu_fibra = DSU(n_nodos)
    dsu_coaxial = DSU(n_nodos)

    vecinos_fibra = {i: set([i]) for i in range(1, n_nodos+1)}  # líder fibra -> conjuntos de líderes coaxial
    vecinos_coaxial = {i: set([i]) for i in range(1, n_nodos+1)}  # líder coaxial -> conjuntos de líderes fibra

    def agregar_par_nodo(i):
        f = dsu_fibra.buscar(i); c = dsu_coaxial.buscar(i)
        vecinos_fibra.setdefault(f, set()).add(c)
        vecinos_coaxial.setdefault(c, set()).add(f)

    def unir_fibra(a,b):
        a = dsu_fibra.buscar(a); b = dsu_fibra.buscar(b)
        if a==b: return a
        # asegurar que a sea el mayor
        if dsu_fibra.tam[a] < dsu_fibra.tam[b]: a,b = b,a
        # fusionar b dentro de a
        dsu_fibra.padre[b]=a
        dsu_fibra.tam[a]+=dsu_fibra.tam[b]
        Sb = vecinos_fibra.get(b, set())
        Sa = vecinos_fibra.get(a, set())
        # small-to-large: fusionar conjunto pequeño en grande
        if len(Sb) > len(Sa):
            Sa, Sb = Sb, Sa
            vecinos_fibra[a] = Sa
        for c in Sb:
            # actualizar mapeo inverso
            s = vecinos_coaxial.get(c)
            if s:
                if b in s:
                    s.remove(b)
                s.add(a)
            Sa.add(c)
        vecinos_fibra[b] = set()
        return a

    def unir_coaxial(a,b):
        a = dsu_coaxial.buscar(a); b = dsu_coaxial.buscar(b)
        if a==b: return a
        if dsu_coaxial.tam[a] < dsu_coaxial.tam[b]: a,b = b,a
        dsu_coaxial.padre[b]=a
        dsu_coaxial.tam[a]+=dsu_coaxial.tam[b]
        Sb = vecinos_coaxial.get(b, set())
        Sa = vecinos_coaxial.get(a, set())
        if len(Sb) > len(Sa):
            Sa, Sb = Sb, Sa
            vecinos_coaxial[a] = Sa
        for f in Sb:
            s = vecinos_fibra.get(f)
            if s:
                if b in s:
                    s.remove(b)
                s.add(a)
            Sa.add(f)
        vecinos_coaxial[b] = set()
        return a

    respuestas = []
    for (a,b,tipo) in aristas:
        # asegurar que existan los mapeos de nodos
        agregar_par_nodo(a); agregar_par_nodo(b)
        if tipo==1:
            unir_fibra(a,b)
        else:
            unir_coaxial(a,b)

        # Después de la operación, comprobar si el mapeo es biyectivo:
        ok = True
        # iterar líderes de fibra
        vistos_coaxial = set()
        for i in range(1, n_nodos+1):
            if dsu_fibra.buscar(i) != i: continue
            s = vecinos_fibra.get(i, set())
            if len(s) != 1:
                ok = False; break
            c = next(iter(s))
            vistos_coaxial.add(c)
        if ok:
            # cada líder coaxial debe mapear exactamente a un líder de fibra
            for i in range(1, n_nodos+1):
                if dsu_coaxial.buscar(i) != i: continue
                s = vecinos_coaxial.get(i, set())
                if len(s) != 1:
                    ok = False; break
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