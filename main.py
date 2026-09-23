import tkinter as tk
from tkinter import messagebox, ttk


QUANTIDADE_ALUNOS = 5
QUANTIDADE_AVALIACOES = 3
MEDIA_MINIMA = 6.0

alunos = ["" for _ in range(QUANTIDADE_ALUNOS)]
notas = [
    [0.0 for _ in range(QUANTIDADE_AVALIACOES)]
    for _ in range(QUANTIDADE_ALUNOS)
]
campos_nomes = []
campos_notas = []


def formatar_nota(valor):
    return f"{valor:.2f}".replace(".", ",")


def limpar_resultados():
    for item in tabela.get_children():
        tabela.delete(item)
    resumo_var.set("Preencha os dados e clique em Calcular Resultados.")
    status_var.set("Aguardando preenchimento dos cinco alunos.")


def limpar_formulario():
    global alunos, notas

    for campo in campos_nomes:
        campo.delete(0, tk.END)
    for linha in campos_notas:
        for campo in linha:
            campo.delete(0, tk.END)

    alunos = ["" for _ in range(QUANTIDADE_ALUNOS)]
    notas = [
        [0.0 for _ in range(QUANTIDADE_AVALIACOES)]
        for _ in range(QUANTIDADE_ALUNOS)
    ]
    limpar_resultados()
    status_var.set("Formulário limpo. Pronto para um novo preenchimento.")


def ler_dados():
    global alunos, notas

    novos_alunos = []
    novas_notas = []

    # REPETIÇÃO: percorre as cinco linhas do formulário para coletar os dados.
    for indice_aluno in range(QUANTIDADE_ALUNOS):
        nome = campos_nomes[indice_aluno].get().strip()
        if nome == "":
            messagebox.showwarning(
                "Dados incompletos",
                f"Informe o nome do aluno {indice_aluno + 1}.",
            )
            campos_nomes[indice_aluno].focus()
            return False

        notas_aluno = []
        # REPETIÇÃO aninhada: percorre as três avaliações do aluno atual.
        for indice_avaliacao in range(QUANTIDADE_AVALIACOES):
            texto_nota = campos_notas[indice_aluno][indice_avaliacao].get().strip()
            texto_nota = texto_nota.replace(",", ".")
            if texto_nota == "":
                messagebox.showwarning(
                    "Dados incompletos",
                    f"Informe a avaliação {indice_avaliacao + 1} de {nome}.",
                )
                campos_notas[indice_aluno][indice_avaliacao].focus()
                return False

            try:
                nota = float(texto_nota)
            except ValueError:
                messagebox.showerror(
                    "Nota inválida",
                    f"A avaliação {indice_avaliacao + 1} de {nome} deve ser numérica.",
                )
                campos_notas[indice_aluno][indice_avaliacao].focus()
                return False

            # SELEÇÃO: rejeita valores fora do intervalo permitido pela atividade.
            if nota < 0 or nota > 10:
                messagebox.showerror(
                    "Nota fora do intervalo",
                    f"A avaliação {indice_avaliacao + 1} de {nome} deve estar entre 0 e 10.",
                )
                campos_notas[indice_aluno][indice_avaliacao].focus()
                return False

            notas_aluno.append(nota)

        novos_alunos.append(nome)
        novas_notas.append(notas_aluno)

    alunos = novos_alunos
    notas = novas_notas
    return True


def calcular_resultados():
    if not ler_dados():
        return

    limpar_resultados()
    total_medias = 0.0
    quantidade_aprovados = 0
    quantidade_reprovados = 0
    maior_media = 0.0
    menor_media = 10.0
    nome_maior_media = ""
    nome_menor_media = ""

    # REPETIÇÃO: calcula e exibe o resultado de cada posição do vetor/matriz.
    for indice_aluno in range(QUANTIDADE_ALUNOS):
        soma = 0.0
        # Acumulação manual das três notas, substituindo sum().
        for indice_avaliacao in range(QUANTIDADE_AVALIACOES):
            soma = soma + notas[indice_aluno][indice_avaliacao]
        media = soma / QUANTIDADE_AVALIACOES
        total_medias = total_medias + media

        # SELEÇÃO: classifica o aluno conforme a média mínima de aprovação.
        if media >= MEDIA_MINIMA:
            situacao = "Aprovado"
            quantidade_aprovados = quantidade_aprovados + 1
        else:
            situacao = "Reprovado"
            quantidade_reprovados = quantidade_reprovados + 1

        # Seleção manual de maior e menor média, substituindo max() e min().
        if indice_aluno == 0 or media > maior_media:
            maior_media = media
            nome_maior_media = alunos[indice_aluno]
        if indice_aluno == 0 or media < menor_media:
            menor_media = media
            nome_menor_media = alunos[indice_aluno]

        tabela.insert(
            "",
            tk.END,
            values=(
                indice_aluno + 1,
                alunos[indice_aluno],
                formatar_nota(notas[indice_aluno][0]),
                formatar_nota(notas[indice_aluno][1]),
                formatar_nota(notas[indice_aluno][2]),
                formatar_nota(soma),
                formatar_nota(media),
                situacao,
            ),
        )

    media_turma = total_medias / QUANTIDADE_ALUNOS
    resumo_var.set(
        f"Média da turma: {formatar_nota(media_turma)} | "
        f"Aprovados: {quantidade_aprovados} | "
        f"Reprovados: {quantidade_reprovados} | "
        f"Maior média: {nome_maior_media} ({formatar_nota(maior_media)}) | "
        f"Menor média: {nome_menor_media} ({formatar_nota(menor_media)})"
    )
    status_var.set("Resultados calculados com sucesso.")


def criar_interface():
    global tabela, resumo_var, status_var

    janela = tk.Tk()
    janela.title("Controle de Notas da Turma")
    janela.minsize(980, 600)

    estilo = ttk.Style()
    estilo.configure("Titulo.TLabel", font=("Segoe UI", 16, "bold"))
    estilo.configure("Resumo.TLabel", font=("Segoe UI", 10, "bold"))
    estilo.configure("Treeview", rowheight=28)

    principal = ttk.Frame(janela, padding=16)
    principal.grid(row=0, column=0, sticky="nsew")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    principal.columnconfigure(0, weight=1)
    principal.rowconfigure(2, weight=1)

    ttk.Label(
        principal,
        text="Controle de Notas da Turma",
        style="Titulo.TLabel",
    ).grid(row=0, column=0, sticky="w", pady=(0, 4))
    ttk.Label(
        principal,
        text="Informe os cinco alunos e suas três avaliações (notas de 0 a 10).",
    ).grid(row=1, column=0, sticky="w", pady=(0, 12))

    formulario = ttk.LabelFrame(principal, text="Dados dos alunos", padding=10)
    formulario.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
    formulario.columnconfigure(1, weight=1)

    cabecalhos = ["Aluno", "Nome", "Avaliação 1", "Avaliação 2", "Avaliação 3"]
    for coluna, texto in enumerate(cabecalhos):
        ttk.Label(formulario, text=texto).grid(
            row=0, column=coluna, padx=6, pady=(0, 6), sticky="w"
        )

    # REPETIÇÃO: cria os campos da interface para cada posição do vetor e matriz.
    for indice_aluno in range(QUANTIDADE_ALUNOS):
        ttk.Label(formulario, text=str(indice_aluno + 1)).grid(
            row=indice_aluno + 1, column=0, padx=6, pady=5
        )
        campo_nome = ttk.Entry(formulario, width=32)
        campo_nome.grid(row=indice_aluno + 1, column=1, padx=6, pady=5, sticky="ew")
        campos_nomes.append(campo_nome)

        linha_campos = []
        for indice_avaliacao in range(QUANTIDADE_AVALIACOES):
            campo_nota = ttk.Entry(formulario, width=14)
            campo_nota.grid(
                row=indice_aluno + 1,
                column=indice_avaliacao + 2,
                padx=6,
                pady=5,
            )
            linha_campos.append(campo_nota)
        campos_notas.append(linha_campos)

    botoes = ttk.Frame(principal)
    botoes.grid(row=3, column=0, sticky="e", pady=(0, 12))
    ttk.Button(
        botoes,
        text="Calcular Resultados",
        command=calcular_resultados,
    ).grid(row=0, column=0, padx=(0, 8))
    ttk.Button(botoes, text="Limpar", command=limpar_formulario).grid(row=0, column=1)

    painel_resultados = ttk.LabelFrame(principal, text="Resultados", padding=10)
    painel_resultados.grid(row=4, column=0, sticky="nsew")
    painel_resultados.columnconfigure(0, weight=1)

    colunas = ("posicao", "aluno", "av1", "av2", "av3", "soma", "media", "situacao")
    tabela = ttk.Treeview(painel_resultados, columns=colunas, show="headings", height=6)
    titulos = {
        "posicao": "#",
        "aluno": "Aluno",
        "av1": "Avaliação 1",
        "av2": "Avaliação 2",
        "av3": "Avaliação 3",
        "soma": "Soma",
        "media": "Média",
        "situacao": "Situação",
    }
    larguras = {
        "posicao": 40,
        "aluno": 220,
        "av1": 100,
        "av2": 100,
        "av3": 100,
        "soma": 90,
        "media": 90,
        "situacao": 110,
    }
    for coluna in colunas:
        tabela.heading(coluna, text=titulos[coluna])
        tabela.column(coluna, width=larguras[coluna], anchor="center")
    tabela.grid(row=0, column=0, sticky="nsew")

    resumo_var = tk.StringVar(value="Preencha os dados e clique em Calcular Resultados.")
    ttk.Label(
        painel_resultados,
        textvariable=resumo_var,
        style="Resumo.TLabel",
        wraplength=950,
    ).grid(row=1, column=0, sticky="w", pady=(10, 0))

    status_var = tk.StringVar(value="Aguardando preenchimento dos cinco alunos.")
    ttk.Label(principal, textvariable=status_var).grid(
        row=5, column=0, sticky="w", pady=(10, 0)
    )

    janela.bind("<Return>", lambda evento: calcular_resultados())
    janela.mainloop()


if __name__ == "__main__":
    criar_interface()
