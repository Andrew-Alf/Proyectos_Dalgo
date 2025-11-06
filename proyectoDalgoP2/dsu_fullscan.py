#!/usr/bin/env python3
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

        ok = True
        mapeo = {}
        mapeados = set()
        for i in range(1,n_nodos+1):
            x = comp_fibra[i]; y = comp_coaxial[i]
            if x in mapeo:
                if mapeo[x] != y:
                    ok = False; break
            else:
                mapeo[x] = y
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
    out=[]
    for _ in range(t_casos):
        n_nodos=int(next(iterador)); m_aristas=int(next(iterador))
        aristas=[]
        for _ in range(m_aristas):
            a=int(next(iterador)); b=int(next(iterador)); tipo=int(next(iterador))
            aristas.append((a,b,tipo))
        out.append(' '.join(str(x) for x in process_case(n_nodos, aristas)))
    sys.stdout.write('\n'.join(out))
    elapsed = time.time() - start
    # Comentar acá abajo para quitar el tiempo en la entrega final
    print(f"# Time: {elapsed:.6f}s", file=sys.stderr)
