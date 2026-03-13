import random
import time

CLASSES = {
    "Guerreiro": {"hp": 120, "ataque": (15, 30), "defesa": 10, "habilidade": "Golpe Brutal"},
    "Mago":      {"hp": 70,  "ataque": (25, 45), "defesa": 4,  "habilidade": "Bola de Fogo"},
    "Arqueiro":  {"hp": 90,  "ataque": (18, 35), "defesa": 7,  "habilidade": "Flecha Certeira"},
    "Paladino":  {"hp": 110, "ataque": (12, 25), "defesa": 14, "habilidade": "Escudo Sagrado"},
}

def criar_personagem(nome, classe):
    stats = CLASSES[classe]
    return {
        "nome": nome,
        "classe": classe,
        "hp": stats["hp"],
        "hp_max": stats["hp"],
        "ataque": stats["ataque"],
        "defesa": stats["defesa"],
        "habilidade": stats["habilidade"],
        "vitorias": 0,
    }

def calcular_dano(atacante, defensor, habilidade=False):
    min_atk, max_atk = atacante["ataque"]
    dano_bruto = random.randint(min_atk, max_atk)
    if habilidade:
        dano_bruto = int(dano_bruto * 1.6)
    dano_final = max(1, dano_bruto - defensor["defesa"] + random.randint(-3, 3))
    return dano_final

def barra_hp(hp, hp_max, tamanho=20):
    proporcao = hp / hp_max
    preenchido = int(proporcao * tamanho)
    barra = "█" * preenchido + "░" * (tamanho - preenchido)
    cor = "🟢" if proporcao > 0.5 else "🟡" if proporcao > 0.25 else "🔴"
    return f"{cor} [{barra}] {hp}/{hp_max}"

def imprimir_status(p1, p2):
    print(f"\n  {p1['nome']} ({p1['classe']})")
    print(f"  HP: {barra_hp(p1['hp'], p1['hp_max'])}")
    print(f"  {p2['nome']} ({p2['classe']})")
    print(f"  HP: {barra_hp(p2['hp'], p2['hp_max'])}")
    print("  " + "─" * 40)

def batalha(p1, p2):
    print(f"\n{'='*45}")
    print(f"  ⚔️  BATALHA: {p1['nome']} vs {p2['nome']}")
    print(f"{'='*45}")
    imprimir_status(p1, p2)

    turno = 1
    while p1["hp"] > 0 and p2["hp"] > 0:
        print(f"\n  [ Turno {turno} ]")

        for atacante, defensor in [(p1, p2), (p2, p1)]:
            if defensor["hp"] <= 0:
                break
            usa_hab = random.random() < 0.2
            dano = calcular_dano(atacante, defensor, habilidade=usa_hab)
            defensor["hp"] = max(0, defensor["hp"] - dano)

            acao = f"✨ {atacante['habilidade']}!" if usa_hab else "espada"
            print(f"  {atacante['nome']} ataca com {acao} → {dano} de dano")

        imprimir_status(p1, p2)
        turno += 1

        if turno > 50:
            print("\n  ⏳ Batalha encerrada por tempo!")
            break

    vencedor = p1 if p1["hp"] > 0 else p2
    perdedor = p2 if vencedor == p1 else p1
    vencedor["vitorias"] += 1
    print(f"\n  🏆 {vencedor['nome']} VENCEU em {turno-1} turnos!")
    return vencedor

def torneio(personagens):
    print(f"\n{'#'*45}")
    print(f"  🏟️  TORNEIO COM {len(personagens)} PERSONAGENS")
    print(f"{'#'*45}")

    competidores = personagens[:]
    random.shuffle(competidores)

    rodada = 1
    while len(competidores) > 1:
        print(f"\n\n  ━━ RODADA {rodada} ━━")
        proximos = []
        random.shuffle(competidores)

        for i in range(0, len(competidores) - 1, 2):
            p1 = dict(competidores[i])
            p2 = dict(competidores[i + 1])
            p1["hp"] = p1["hp_max"]
            p2["hp"] = p2["hp_max"]
            vencedor_nome = batalha(p1, p2)["nome"]
            for p in personagens:
                if p["nome"] == vencedor_nome:
                    proximos.append(p)
                    break

        if len(competidores) % 2 == 1:
            bye = competidores[-1]
            print(f"\n  🎯 {bye['nome']} avança automaticamente (bye)")
            proximos.append(bye)

        competidores = proximos
        rodada += 1

    campeao = competidores[0]
    print(f"\n\n{'★'*45}")
    print(f"  🥇 CAMPEÃO DO TORNEIO: {campeao['nome']} ({campeao['classe']})")
    print(f"  Vitórias: {campeao['vitorias']}")
    print(f"{'★'*45}\n")

if __name__ == "__main__":
    random.seed(42)

    personagens = [
        criar_personagem("Aragorn",  "Guerreiro"),
        criar_personagem("Gandalf",  "Mago"),
        criar_personagem("Legolas",  "Arqueiro"),
        criar_personagem("Arthas",   "Paladino"),
    ]

    torneio(personagens)
