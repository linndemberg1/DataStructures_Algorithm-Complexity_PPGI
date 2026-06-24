# 🤖 Orienteering Problem — RAH Chico Mendes

> **Disciplina:** Estrutura de Dados e Complexidade de Algoritmos  
> **Programa:** Pós-Graduação em Informática — UFPB  
> **Autor:** José Lindenberg de Andrade  
> **Matrícula:** 20261001315  
> **Docente:** Prof. Dr. Gilberto Farias  

---

## 📋 Descrição do Problema

Este repositório implementa a **Atividade A2** do Projeto Final da disciplina, que consiste em resolver um Problema de Otimização Combinatória (POC) por meio de uma meta-heurística.

O problema modelado é o **Orienteering Problem (OP)** aplicado ao planejamento de rotas do **Robô Ambiental Híbrido Chico Mendes (RAH)**, desenvolvido no projeto R2AH da UFPB em parceria com a Petrobras.

### Cenário

Em um desastre ambiental na **Praia do Jacaré (Cabedelo/PB)**, 20 animais ficam feridos e dispersos. O RAH deve partir de sua base, resgatar o maior número possível de animais prioritários e retornar — respeitando sua limitação energética de **3.000 Wh** (autonomia de ~2 km).

### Formulação

| Parâmetro | Valor |
|---|---|
| Nós totais | 22 (20 vítimas + origem + destino) |
| Bateria (Tmax) | 3.000 Wh |
| Autonomia | 2.000 m |
| Consumo | 1,5 Wh/m |
| Prioridades (Si) | 1 a 5 (baixa → crítica) |

**Objetivo:** maximizar a soma das prioridades das vítimas atendidas, respeitando o orçamento energético.

---

## 🧠 Meta-heurística: VND

A solução implementa o **Variable Neighborhood Descent (VND)**, com as seguintes etapas:

### Representação da Solução

Lista ordenada de nós representando o caminho do RAH:

```
[0, 4, 11, 5, 17, 21]
 ↑                  ↑
origem            destino
```

### Heurística de Construção

**Greedy por razão prêmio/custo de inserção:** a cada iteração, insere o nó não visitado com melhor razão `prêmio / delta_custo` na posição ótima da rota, enquanto houver orçamento disponível.

### Estruturas de Vizinhança

| Vizinhança | Descrição |
|---|---|
| **N1 – Inserção** | Tenta inserir cada vítima não visitada em toda posição possível da rota |
| **N2 – Remoção** | Remove a vítima de pior razão prêmio/custo, liberando orçamento |
| **N3 – Troca (swap)** | Substitui uma vítima visitada por uma não visitada de prêmio maior |

### Algoritmo VND

```
rota ← construcao_gulosa()
k ← 0
enquanto k < 3:
    nova_rota ← melhor_da_vizinhanca(rota, Nk)
    se premio(nova_rota) > premio(rota):
        rota ← nova_rota
        k ← 0          // melhora → volta a N1
    senão:
        k ← k + 1      // sem melhora → próxima vizinhança
retorna rota
```

---

## 📊 Resultados Computacionais

Execução com **10 repetições** (sementes aleatórias distintas):

| Execução | Prêmio | Tempo (s) |
|:---:|:---:|:---:|
| 1  | 15 | 0,0007 |
| 2  | 15 | 0,0005 |
| 3  | 15 | 0,0005 |
| 4  | 15 | 0,0005 |
| 5  | 15 | 0,0005 |
| 6  | 15 | 0,0005 |
| 7  | 15 | 0,0046 |
| 8  | 15 | 0,0007 |
| 9  | 15 | 0,0005 |
| 10 | 15 | 0,0005 |
| **Melhor** | **15** | **0,0005** |
| **Média** | **15** | **0,0010** |

### Melhor Rota Encontrada

```
RAH (Origem) → Vítima 5 → Vítima 4 → Vítima 11 → Vítima 17 → RAH (Destino)
```

| Métrica | Valor |
|---|---|
| Prêmio total | **15** |
| Custo energético | 2.884 Wh / 3.000 Wh |
| Distância percorrida | ~1.923 m |
| Vítimas resgatadas | 4 |
| Urgências atendidas | 2 + 5 + 5 + 3 |

---

## 🚀 Como Executar

### Requisitos

- Python 3.7+
- Nenhuma biblioteca externa necessária (usa apenas `math`, `time`, `random`, `copy`)

### Execução local

```bash
python op_rah_vnd.py
```

### Google Colab

1. Acesse [colab.research.google.com](https://colab.research.google.com)
2. Crie um novo notebook
3. Cole o conteúdo de `op_rah_vnd.py` em uma célula
4. Execute com **Shift + Enter**

---

## 📁 Estrutura do Repositório

```
.
├── op_rah_vnd.py      # Implementação do VND em Python
├── OP_RAH.mod         # Modelo exato em OPL/CPLEX (A1)
├── OP_RAH.dat         # Dados da instância para o CPLEX
└── README.md          # Este arquivo
```

---

## 📍 Instância

A instância é original, desenvolvida com base em coordenadas geográficas reais da **Praia do Jacaré, Cabedelo/PB**, com graus de urgência atribuídos conforme critérios de triagem veterinária.

| Vítima | Latitude | Longitude | Urgência |
|---|---|---|---|
| RAH (base) | -7,03920 | -34,85536 | — |
| Vítima 1  | -7,03547 | -34,86326 | 1 |
| Vítima 2  | -7,03245 | -34,86246 | 4 |
| Vítima 3  | -7,03158 | -34,85551 | 3 |
| Vítima 4  | -7,03802 | -34,86276 | **5** |
| Vítima 5  | -7,03857 | -34,85755 | 2 |
| Vítima 6  | -7,03235 | -34,85950 | 2 |
| Vítima 7  | -7,02767 | -34,85886 | 3 |
| Vítima 8  | -7,02837 | -34,86257 | 3 |
| Vítima 9  | -7,03434 | -34,86036 | 4 |
| Vítima 10 | -7,02897 | -34,85716 | 1 |
| Vítima 11 | -7,03906 | -34,86034 | **5** |
| Vítima 12 | -7,04056 | -34,86374 | 3 |
| Vítima 13 | -7,04158 | -34,86111 | 2 |
| Vítima 14 | -7,03497 | -34,85815 | 1 |
| Vítima 15 | -7,02965 | -34,86107 | 4 |
| Vítima 16 | -7,03049 | -34,86386 | 2 |
| Vítima 17 | -7,04170 | -34,85811 | 3 |
| Vítima 18 | -7,04329 | -34,86296 | **5** |
| Vítima 19 | -7,04412 | -34,85743 | 3 |
| Vítima 20 | -7,03260 | -34,85717 | 4 |

---

## 📚 Referências

- TSILIGIRIDES, T. Heuristic methods applied to orienteering. *Journal of the Operational Research Society*, v. 35, n. 9, p. 797–809, 1984.
- FISCHETTI, M.; SALAZAR GONZÁLEZ, J. J.; TOTH, P. Solving the orienteering problem through branch-and-cut. *INFORMS Journal on Computing*, v. 10, n. 2, p. 133–148, 1998.
- VANSTEENWEGEN, P. et al. A guided local search metaheuristic for the team orienteering problem. *European Journal of Operational Research*, v. 196, n. 1, p. 118–127, 2009.
- R2AH PROJECT — Robô Ambiental Híbrido. UFPB, 2026. Disponível em: https://r2ah.ci.ufpb.br/
