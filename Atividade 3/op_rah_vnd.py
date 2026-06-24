"""
=============================================================
  Orienteering Problem - RAH Chico Mendes
  Heurística VND (Variable Neighborhood Descent)
  Disciplina: Estrutura de Dados e Complexidade de Algoritmos
  Autor: José Lindenberg de Andrade
=============================================================
"""

import math
import time
import random
import copy

# ─────────────────────────────────────────────────────────────
# 1. DADOS DA INSTÂNCIA (Praia do Jacaré, Cabedelo/PB)
# ─────────────────────────────────────────────────────────────

NOMES = [
    "RAH (Origem)",
    "Vítima 1",  "Vítima 2",  "Vítima 3",  "Vítima 4",
    "Vítima 5",  "Vítima 6",  "Vítima 7",  "Vítima 8",
    "Vítima 9",  "Vítima 10", "Vítima 11", "Vítima 12",
    "Vítima 13", "Vítima 14", "Vítima 15", "Vítima 16",
    "Vítima 17", "Vítima 18", "Vítima 19", "Vítima 20",
    "RAH (Destino)",
]

LATITUDES = [
    -7.03920, -7.03547, -7.03245, -7.03158, -7.03802,
    -7.03857, -7.03235, -7.02767, -7.02837, -7.03434,
    -7.02897, -7.03906, -7.04056, -7.04158, -7.03497,
    -7.02965, -7.03049, -7.04170, -7.04329, -7.04412,
    -7.03260, -7.03920,
]

LONGITUDES = [
    -34.85536, -34.86326, -34.86246, -34.85551, -34.86276,
    -34.85755, -34.85950, -34.85886, -34.86257, -34.86036,
    -34.85716, -34.86034, -34.86374, -34.86111, -34.85815,
    -34.86107, -34.86386, -34.85811, -34.86296, -34.85743,
    -34.85717, -34.85536,
]

PREMIOS = [
    0,  # RAH origem
    1, 4, 3, 5, 2, 2, 3, 3, 4, 1,
    5, 3, 2, 1, 4, 2, 3, 5, 3, 4,
    0,  # RAH destino
]

TMAX      = 3000.0   # Wh
AUTONOMIA = 2000.0   # metros
CONSUMO   = TMAX / AUTONOMIA  # 1.5 Wh/m

N = len(PREMIOS)          # 22 nós (0 = origem, 21 = destino)
ORIGEM  = 0
DESTINO = N - 1

# ─────────────────────────────────────────────────────────────
# 2. MATRIZ DE DISTÂNCIAS E CUSTOS
# ─────────────────────────────────────────────────────────────

def calc_distancia(i, j):
    dlat = LATITUDES[i]  - LATITUDES[j]
    dlon = LONGITUDES[i] - LONGITUDES[j]
    return 111_000.0 * math.sqrt(dlat**2 + dlon**2)

DIST  = [[calc_distancia(i, j) for j in range(N)] for i in range(N)]
CUSTO = [[DIST[i][j] * CONSUMO for j in range(N)] for i in range(N)]

# ─────────────────────────────────────────────────────────────
# 3. FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────────────────────

def custo_rota(rota):
    """Custo energético total da rota."""
    return sum(CUSTO[rota[k]][rota[k+1]] for k in range(len(rota)-1))

def premio_rota(rota):
    """Prêmio total (sem contar origem e destino)."""
    return sum(PREMIOS[v] for v in rota[1:-1])

def viavel(rota):
    """Verifica se a rota respeita o orçamento Tmax."""
    return custo_rota(rota) <= TMAX

def nos_visitados(rota):
    """Conjunto de nós intermediários na rota."""
    return set(rota[1:-1])

def nos_disponiveis(rota):
    """Nós intermediários ainda não visitados."""
    todos = set(range(1, DESTINO))
    return todos - nos_visitados(rota)

# ─────────────────────────────────────────────────────────────
# 4. HEURÍSTICA DE CONSTRUÇÃO GULOSA
#    Razão prêmio / custo de inserção (origem → nó → destino)
# ─────────────────────────────────────────────────────────────

def construcao_gulosa(seed=None):
    """
    Constrói uma solução inicial inserindo iterativamente
    o nó com melhor razão prêmio/custo de inserção.
    """
    rng = random.Random(seed)
    rota = [ORIGEM, DESTINO]

    while True:
        melhor_no    = None
        melhor_ratio = -1.0
        melhor_pos   = None

        candidatos = list(nos_disponiveis(rota))
        rng.shuffle(candidatos)   # ordem aleatória para desempate

        for no in candidatos:
            for pos in range(1, len(rota)):
                ant = rota[pos - 1]
                prox = rota[pos]
                delta = CUSTO[ant][no] + CUSTO[no][prox] - CUSTO[ant][prox]
                if PREMIOS[no] == 0:
                    continue
                ratio = PREMIOS[no] / (delta + 1e-9)

                nova_rota = rota[:pos] + [no] + rota[pos:]
                if not viavel(nova_rota):
                    continue

                if ratio > melhor_ratio:
                    melhor_ratio = ratio
                    melhor_no    = no
                    melhor_pos   = pos

        if melhor_no is None:
            break

        rota.insert(melhor_pos, melhor_no)

    return rota

# ─────────────────────────────────────────────────────────────
# 5. ESTRUTURAS DE VIZINHANÇA
# ─────────────────────────────────────────────────────────────

def vizinhanca_insercao(rota):
    """
    N1 – Inserção: tenta inserir cada nó não visitado
    na melhor posição da rota. Retorna a melhor melhora encontrada.
    """
    melhor_rota   = rota
    melhor_premio = premio_rota(rota)

    for no in nos_disponiveis(rota):
        if PREMIOS[no] == 0:
            continue
        for pos in range(1, len(rota)):
            nova = rota[:pos] + [no] + rota[pos:]
            if viavel(nova):
                p = premio_rota(nova)
                if p > melhor_premio:
                    melhor_premio = p
                    melhor_rota   = nova

    return melhor_rota

def vizinhanca_remocao(rota):
    """
    N2 – Remoção: remove o nó intermediário de menor prêmio/custo.
    Isso libera orçamento para inserções futuras.
    Retorna rota sem o nó menos valioso (só aplica se há mais de 1 nó).
    """
    intermediarios = rota[1:-1]
    if not intermediarios:
        return rota

    # Remove o de menor razão prêmio/custo_contribuição
    pior_no  = min(intermediarios,
                   key=lambda v: PREMIOS[v] / (CUSTO[ORIGEM][v] + 1e-9))
    nova = [v for v in rota if v != pior_no]

    # Verifica que a rota não perdeu prêmio em excesso
    if premio_rota(nova) < premio_rota(rota):
        # Só aceita remoção se ela não piora diretamente:
        # a remoção abre espaço para que N1 insira nó melhor.
        # Retornamos a nova rota mesmo assim (VND decide).
        return nova
    return nova

def vizinhanca_swap(rota):
    """
    N3 – Troca: substitui um nó visitado por um não visitado,
    se o substituto tem prêmio maior e a rota continua viável.
    """
    melhor_rota   = rota
    melhor_premio = premio_rota(rota)

    visitados  = list(nos_visitados(rota))
    disponiveis = list(nos_disponiveis(rota))

    for v_out in visitados:
        idx = rota.index(v_out)
        for v_in in disponiveis:
            if PREMIOS[v_in] <= PREMIOS[v_out]:
                continue
            nova = rota[:idx] + [v_in] + rota[idx+1:]
            if viavel(nova):
                p = premio_rota(nova)
                if p > melhor_premio:
                    melhor_premio = p
                    melhor_rota   = nova

    return melhor_rota

# ─────────────────────────────────────────────────────────────
# 6. VND – Variable Neighborhood Descent
# ─────────────────────────────────────────────────────────────

VIZINHANCAS = [
    ("N1 - Inserção", vizinhanca_insercao),
    ("N2 - Remoção",  vizinhanca_remocao),
    ("N3 - Troca",    vizinhanca_swap),
]

def vnd(rota_inicial):
    """
    VND clássico: percorre as vizinhanças em ordem.
    Se há melhora em Nk, volta a N1.
    Para quando nenhuma vizinhança melhora a solução.
    """
    rota_atual = copy.copy(rota_inicial)
    k = 0

    while k < len(VIZINHANCAS):
        nome_viz, viz_fn = VIZINHANCAS[k]
        nova_rota = viz_fn(rota_atual)

        if premio_rota(nova_rota) > premio_rota(rota_atual):
            rota_atual = nova_rota
            k = 0           # melhora → volta ao início
        else:
            k += 1          # sem melhora → próxima vizinhança

    return rota_atual

# ─────────────────────────────────────────────────────────────
# 7. EXECUÇÃO E RESULTADOS COMPUTACIONAIS
# ─────────────────────────────────────────────────────────────

def executar(n_repeticoes=10):
    print("=" * 60)
    print("  ORIENTEERING PROBLEM — RAH CHICO MENDES")
    print("  Heurística: VND (Variable Neighborhood Descent)")
    print("=" * 60)
    print(f"  Instância : Praia do Jacaré, Cabedelo/PB")
    print(f"  Nós       : {N} (20 vítimas + origem + destino)")
    print(f"  Tmax      : {TMAX} Wh  |  Autonomia: {AUTONOMIA} m")
    print("=" * 60)

    melhor_rota   = None
    melhor_premio = -1
    tempos        = []

    for rep in range(1, n_repeticoes + 1):
        t0 = time.perf_counter()

        rota_inicial = construcao_gulosa(seed=rep)
        rota_final   = vnd(rota_inicial)

        t1 = time.perf_counter()
        tempos.append(t1 - t0)

        p = premio_rota(rota_final)
        if p > melhor_premio:
            melhor_premio = p
            melhor_rota   = rota_final

    # ── Resultados ──────────────────────────────────────────
    print(f"\n{'Execução':<10} {'Prêmio':>8} {'Tempo (s)':>12}")
    print("-" * 34)

    # Reexecuta para mostrar individualmente
    premios_exec = []
    for rep in range(1, n_repeticoes + 1):
        rota_i = construcao_gulosa(seed=rep)
        rota_f = vnd(rota_i)
        premios_exec.append(premio_rota(rota_f))
        print(f"  {rep:<8} {premios_exec[-1]:>8} {tempos[rep-1]:>12.4f}")

    print("-" * 34)
    print(f"  {'Melhor':<8} {max(premios_exec):>8} {min(tempos):>12.4f}")
    print(f"  {'Média t':<8} {'':>8} {sum(tempos)/len(tempos):>12.4f}")

    # ── Melhor rota detalhada ───────────────────────────────
    print("\n" + "=" * 60)
    print("  MELHOR ROTA ENCONTRADA")
    print("=" * 60)
    print(f"  Prêmio total   : {melhor_premio}")
    print(f"  Custo energét. : {custo_rota(melhor_rota):.2f} Wh  "
          f"(limite: {TMAX} Wh)")
    print(f"  Distância total: {custo_rota(melhor_rota)/CONSUMO:.1f} m")
    print(f"  Nós visitados  : {len(melhor_rota) - 2} vítimas\n")

    print("  Sequência:")
    for idx, no in enumerate(melhor_rota):
        seta = " →" if idx < len(melhor_rota) - 1 else ""
        urgencia = f" [urgência={PREMIOS[no]}]" if 0 < no < DESTINO else ""
        print(f"    [{idx:02d}] {NOMES[no]:<20}{urgencia}{seta}")

    print("\n" + "=" * 60)
    return melhor_rota, melhor_premio

# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    executar(n_repeticoes=10)
