# Proyecto Realizado por:
# Angela Jimenez - 202210989
# Andrés Felipe Alfonso Gamba - 202210412

from collections import defaultdict
import sys


def solve_case(points):
    """
    points: lista de tuplas (x, y) con los focos.
    Retorna:
        horiz_segments: lista de (x1, y, x2, y)
        vert_segments:  lista de (x, y1, x, y2)
    """

    # Por seguridad, eliminar duplicados (el enunciado dice que los focos son distintos).
    points = list(dict.fromkeys(points))

    # Agrupar por filas y por columnas
    rows = defaultdict(list)  # y -> lista de x
    cols = defaultdict(list)  # x -> lista de y
    for x, y in points:
        rows[y].append(x)
        cols[x].append(y)

    # Ordenar filas (y) y columnas (x)
    row_keys = sorted(rows.keys())     # todas las y con al menos un foco
    col_keys = sorted(cols.keys())     # todos los x con al menos un foco
    row_index = {y: i for i, y in enumerate(row_keys)}  # y -> índice en 0..R-1

    horiz_segments = []
    vert_segments = []

    # 1) Horizontales: una por cada fila con focos
    for y in row_keys:
        xs = rows[y]
        x1 = min(xs)
        x2 = max(xs)
        horiz_segments.append((x1, y, x2, y))

    # 2) Verticales: runs por columna según el orden de filas
    for x in col_keys:
        ys = cols[x]
        # ordenar ys según el índice global de filas
        ys_sorted = sorted(ys, key=lambda yy: row_index[yy])

        start_y = ys_sorted[0]
        prev_idx = row_index[start_y]
        prev_y = start_y

        for y in ys_sorted[1:]:
            curr_idx = row_index[y]
            if curr_idx == prev_idx + 1:
                # sigue el run
                prev_idx = curr_idx
                prev_y = y
            else:
                # cerrar segmento anterior
                vert_segments.append((x, start_y, x, prev_y))
                # iniciar nuevo segmento
                start_y = y
                prev_idx = curr_idx
                prev_y = y

        # cerrar último segmento de la columna
        vert_segments.append((x, start_y, x, prev_y))

    return horiz_segments, vert_segments


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    it = iter(data)
    try:
        T = int(next(it))  # número de casos
    except StopIteration:
        return

    out_lines = []

    for _ in range(T):
        try:
            n = int(next(it))
        except StopIteration:
            break

        points = []
        for _ in range(n):
            try:
                x = int(next(it))
                y = int(next(it))
            except StopIteration:
                break
            points.append((x, y))

        hsegs, vsegs = solve_case(points)

        # Línea 1: horizontales
        line1 = [str(len(hsegs))]
        for x1, y1, x2, y2 in hsegs:
            line1.extend([str(x1), str(y1), str(x2), str(y2)])

        # Línea 2: verticales
        line2 = [str(len(vsegs))]
        for x1, y1, x2, y2 in vsegs:
            line2.extend([str(x1), str(y1), str(x2), str(y2)])

        out_lines.append(" ".join(line1))
        out_lines.append(" ".join(line2))

    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
