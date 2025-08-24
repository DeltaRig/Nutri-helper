import pandas as pd

def calcular_tmb(peso, altura, idade, sexo='M'):
    if sexo == 'M':
        # Fórmula de Harris-Benedict para homens
        return 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    else:
        # Fórmula de Harris-Benedict para mulheres
        return 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

def calcular_gasto_total(tmb, fator_atividade=1.55):
    return tmb * fator_atividade

def distribuicao_refeicoes(calorias_totais, macros):
    # Distribuição percentual
    distribuicao = {
        "café da manhã": 0.25,
        "almoço": 0.35,
        "lanche": 0.15,
        "jantar": 0.25
    }

    refeicoes = {}
    for nome, perc in distribuicao.items():
        refeicoes[nome] = {
            "kcal": calorias_totais * perc,
            "proteína (g)": macros["proteínas (g)"] * perc,
            "carboidrato (g)": macros["carboidratos (g)"] * perc,
            "gordura (g)": macros["gorduras (g)"] * perc
        }
    return refeicoes

def calcular_macros(calorias_totais, peso):
    # Proteínas: 2g/kg
    # Gorduras: 1g/kg
    proteinas = peso * 2  # g
    gorduras = peso * 1   # g

    calorias_prot = proteinas * 4
    calorias_gord = gorduras * 9
    calorias_restantes = calorias_totais - (calorias_prot + calorias_gord)
    carboidratos = calorias_restantes / 4

    return {
        "proteínas (g)": proteinas,
        "carboidratos (g)": carboidratos,
        "gorduras (g)": gorduras
    }

def converter_alimento(calorias_refeicao):
    # Carrega a tabela
    df = pd.read_csv("tabela_alimentos.csv")

    # Converter para dicionário
    alimentos = df.set_index("Alimento")[["Energia (kcal)", "Carboidrato (g)", "Proteína (g)", "Lipídeos (g)"]].to_dict(orient="index")

    print("\nTabela de alimentos (valores médios por 100g):")
    for k, v in alimentos.items():
        print(f"{k}: {v['Energia (kcal)']} kcal, {v['Carboidrato (g)']}g carb, {v['Proteína (g)']}g prot, {v['Lipídeos (g)']}g gord")

    total = {"kcal": 0, "carb": 0, "prot": 0, "gord": 0}
    decisoes = []

    while total["kcal"] < calorias_refeicao:
        alimento = input("Escolha um alimento (ou 'sair' para terminar): ").strip()
        if alimento.lower() == 'sair':
            break
        if alimento not in alimentos:
            print("Alimento não encontrado. Verifique nome exato na tabela.")
            continue

        gramas = float(input("Quantos gramas deseja adicionar? "))
        fator = gramas / 100
        macros = alimentos[alimento]

        kcal_add = macros["Energia (kcal)"] * fator
        carb_add = macros["Carboidrato (g)"] * fator
        prot_add = macros["Proteína (g)"] * fator
        gord_add = macros["Lipídeos (g)"] * fator

        total["kcal"] += kcal_add
        total["carb"] += carb_add
        total["prot"] += prot_add
        total["gord"] += gord_add

        decisoes.append([alimento, gramas, kcal_add, carb_add, prot_add, gord_add])

        print(f"Adicionado {gramas}g de {alimento} -> {kcal_add:.1f} kcal | {carb_add:.1f}g carb | {prot_add:.1f}g prot | {gord_add:.1f}g gord")
        print(f"Total até agora: {total['kcal']:.1f} kcal | {total['carb']:.1f}g carb | {total['prot']:.1f}g prot | {total['gord']:.1f}g gord")

    print(f"\nTotal da refeição: {total['kcal']:.1f} kcal (meta: {calorias_refeicao:.1f} kcal)")
    print(f"Macros da refeição: {total['carb']:.1f}g carb | {total['prot']:.1f}g prot | {total['gord']:.1f}g gord")

    # Salvar escolhas no arquivo
    df_resultado = pd.DataFrame(decisoes, columns=["Alimento", "Quantidade (g)", "Kcal", "Carboidratos (g)", "Proteínas (g)", "Gorduras (g)"])
    df_resultado.to_csv("refeicao_almoço.csv", index=False, encoding="utf-8-sig")
    print("\nArquivo 'refeicao_almoço.csv' salvo com sucesso!")

# -------------------------------
# Exemplo de uso
# -------------------------------
peso = 85 # kg
altura = 178  # cm
idade = 30
sexo = 'M'  # 'M' para masculino, 'F' para feminino

tmb = calcular_tmb(peso, altura, idade, sexo)
gasto_total = calcular_gasto_total(tmb)
calorias_meta = gasto_total - 600  # déficit

print(f"TMB: {tmb:.1f} kcal")
print(f"Gasto total estimado: {gasto_total:.1f} kcal")
print(f"Meta para emagrecimento: {calorias_meta:.1f} kcal")

macros = calcular_macros(calorias_meta, peso)
refeicoes = distribuicao_refeicoes(calorias_meta, macros)

print("\nSugestão de distribuição:")
for refeicao, valores in refeicoes.items():
    print(f"{refeicao.capitalize()}: {valores['kcal']:.1f} kcal | "
          f"{valores['proteína (g)']:.1f}g prot | "
          f"{valores['carboidrato (g)']:.1f}g carb | "
          f"{valores['gordura (g)']:.1f}g gord")

# Interativo no almoço
converter_alimento(refeicoes["almoço"]["kcal"])

'''
# Gera sugestões automáticas
print("\nSugestões de refeições:")
for nome, meta in refeicoes.items():
    sugestao, total = sugestao_refeicao(meta, alimentos)
    print(f"\n➡️ {nome.capitalize()} (meta {meta['kcal']:.0f} kcal):")
    for item in sugestao:
        print(f"  - {item[1]}g {item[0]} -> {item[2]:.0f} kcal | {item[3]:.1f}g carb | {item[4]:.1f}g prot | {item[5]:.1f}g gord")
    print(f"   Total: {total['kcal']:.0f} kcal | {total['carb']:.1f}g carb | {total['prot']:.1f}g prot | {total['gord']:.1f}g gord")
    salvar_refeicao_csv(nome, sugestao)
'''