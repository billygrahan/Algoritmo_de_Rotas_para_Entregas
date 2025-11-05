import os
import time
import openrouteservice

CO_FILE = "RUSSAS_MAPA_N13.co"
GR_FILE = "RUSSAS_MAPA_N13.gr"
OUT_FILE = "RUSSAS_MAPA_N13_updated.gr"

SLEEP_SECONDS = 10.5  # ajuste para respeitar limites da API

def load_coordinates(co_path):
    coords = {}
    with open(co_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if parts[0] != 'v' or len(parts) < 4:
                continue
            vid = int(parts[1])
            lat = float(parts[2])
            lon = float(parts[3])
            coords[vid] = (lat, lon)
    return coords

def process_gr(gr_path, out_path, coords, client):
    memo = {}  # chave: (u,v) -> distância em metros (int)
    updated_lines = []
    total = 0
    updated = 0

    with open(gr_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()
        if not stripped or not stripped.startswith('a '):
            updated_lines.append(line)
            continue

        parts = stripped.split()
        # expect format: a u v weight [maybe more]
        if len(parts) < 4:
            updated_lines.append(line)
            continue

        try:
            u = int(parts[1])
            v = int(parts[2])
        except ValueError:
            updated_lines.append(line)
            continue

        total += 1
        key = (u, v)
        inv_key = (v, u)

        if key in memo:
            dist = memo[key]
        elif inv_key in memo:
            dist = memo[inv_key]
            memo[key] = dist  # keep symmetric
        else:
            # build coords for openrouteservice: (lon, lat)
            if u not in coords or v not in coords:
                print(f"Aviso: coordenada não encontrada para {u} ou {v}, mantendo peso original.")
                dist = int(float(parts[3])) if parts[3].replace('.', '', 1).isdigit() else 0
                memo[key] = memo[inv_key] = dist
            else:
                lat_u, lon_u = coords[u]
                lat_v, lon_v = coords[v]
                coords_pair = [(lon_u, lat_u), (lon_v, lat_v)]
                try:
                    resp = client.directions(coords_pair, profile='driving-car', format='json')
                    dist_m = resp['routes'][0]['summary']['distance']
                    dist = int(round(dist_m))
                    memo[key] = memo[inv_key] = dist
                    print(f"calc {u} -> {v} = {dist} m")
                    time.sleep(SLEEP_SECONDS)
                except Exception as e:
                    print(f"Erro API para {u}->{v}: {e}. Mantendo peso original.")
                    dist = int(float(parts[3])) if parts[3].replace('.', '', 1).isdigit() else 0
                    memo[key] = memo[inv_key] = dist

        # substitui o quarto token pela distância atualizada
        parts[3] = str(dist)
        new_line = " ".join(parts) + "\n"
        updated_lines.append(new_line)
        updated += 1

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f"Total arestas processadas: {total}. Linhas atualizadas: {updated}. Saída: {out_path}")

def main():
    api_key = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjA1Yzg4ZjM0MjY0ODQyNGViZTA3YWI0MmU1YmFlOTFkIiwiaCI6Im11cm11cjY0In0='

    script_dir = os.path.dirname(__file__)
    co_path = os.path.join(script_dir, CO_FILE)
    gr_path = os.path.join(script_dir, GR_FILE)
    out_path = os.path.join(script_dir, OUT_FILE)

    if not os.path.exists(co_path) or not os.path.exists(gr_path):
        print("Arquivos .co ou .gr não encontrados no diretório do script.")
        return

    coords = load_coordinates(co_path)
    client = openrouteservice.Client(key=api_key)
    process_gr(gr_path, out_path, coords, client)

if __name__ == "__main__":
    main()