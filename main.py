import tkinter as tk
from tkinter import messagebox, ttk


# Configuração inicial padrão; os valores são substituídos pelo usuário.
quantidade_alunos = 5
quantidade_avaliacoes = 3
nota_maxima = 10.0
media_minima = 6.0

alunos = []
notas = []
campos_nomes = []
campos_notas = []
colunas_resultado = []

janela = None
configuracao_frame = None
cadastro_frame = None
formulario_frame = None
resultados_frame = None
canvas_formulario = None
canvas_resultados = None
resumo_var = None
status_var = None
entrada_quantidade_alunos = None
entrada_quantidade_avaliacoes = None
entrada_nota_maxima = None
entrada_media_minima = None
tabela = None


def formatar_numero(valor):
    # replace() troca o separador decimal para o padrão usado no Brasil.
    return f"{valor:.2f}".replace(".", ",")


def ler_numero(texto):
    # strip() remove espaços nas extremidades antes da conversão numérica.
    texto_limpo = texto.strip()
    # replace() permite que o usuário use vírgula como separador decimal.
    return float(texto_limpo.replace(",", "."))


def mostrar_frame(frame):
    configuracao_frame.grid_remove()
    cadastro_frame.grid_remove()
    frame.grid()


def limpar_tabela():
    # get_children() obtém os identificadores das linhas existentes na tabela.
    for item in tabela.get_children():
        tabela.delete(item)


def existem_dados_preenchidos():
    # Repetição: verifica nomes e notas já digitados antes de permitir descarte.
    for campo in campos_nomes:
        if campo.get().strip() != "":
            return True
    for linha in campos_notas:
        for campo in linha:
            if campo.get().strip() != "":
                return True
    return False


def validar_valores_configuracao(texto_alunos, texto_avaliacoes, texto_nota_maxima, texto_media_minima):
    try:
        novos_alunos = int(texto_alunos.strip())
        novas_avaliacoes = int(texto_avaliacoes.strip())
        nova_nota_maxima = ler_numero(texto_nota_maxima)
        nova_media_minima = ler_numero(texto_media_minima)
    except ValueError:
        messagebox.showerror(
            "Configuração inválida",
            "Informe números válidos em todos os campos.",
        )
        return None

    # Seleção: quantidades precisam ser inteiras positivas.
    if novos_alunos <= 0 or novas_avaliacoes <= 0:
        messagebox.showerror(
            "Configuração inválida",
            "A quantidade de alunos e avaliações deve ser maior que zero.",
        )
        return None

    # Seleção: a escala e a média mínima devem formar um intervalo válido.
    if nova_nota_maxima <= 0 or nova_media_minima < 0 or nova_media_minima > nova_nota_maxima:
        messagebox.showerror(
            "Configuração inválida",
            "A nota máxima deve ser positiva e a média mínima deve estar entre zero e a nota máxima.",
        )
        return None

    return novos_alunos, novas_avaliacoes, nova_nota_maxima, nova_media_minima


def aplicar_configuracoes(novos_alunos, novas_avaliacoes, nova_nota_maxima, nova_media_minima):
    global quantidade_alunos, quantidade_avaliacoes, nota_maxima, media_minima

    quantidade_alunos = novos_alunos
    quantidade_avaliacoes = novas_avaliacoes
    nota_maxima = nova_nota_maxima
    media_minima = nova_media_minima

    # Repetição: reconstrói o formulário e a tabela com as novas dimensões.
    criar_formulario_dinamico()
    configurar_tabela_resultados()
    mostrar_frame(cadastro_frame)
    campos_nomes[0].focus()


def abrir_configuracoes():
    janela_configuracoes = tk.Toplevel(janela)
    janela_configuracoes.title("Configurações da Turma")
    janela_configuracoes.resizable(False, False)
    janela_configuracoes.transient(janela)
    janela_configuracoes.grab_set()

    quadro = ttk.Frame(janela_configuracoes, padding=16)
    quadro.grid(row=0, column=0, sticky="nsew")
    quadro.columnconfigure(1, weight=1)
    ttk.Label(
        quadro,
        text="Personalize os parâmetros da turma",
        style="Titulo.TLabel",
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

    configuracoes = [
        ("Quantidade de alunos:", str(quantidade_alunos)),
        ("Quantidade de avaliações:", str(quantidade_avaliacoes)),
        ("Nota máxima:", formatar_numero(nota_maxima)),
        ("Média mínima para aprovação:", formatar_numero(media_minima)),
    ]
    entradas = []
    # Repetição: cria os campos preenchidos com os valores atuais.
    for indice, (rotulo, valor) in enumerate(configuracoes):
        ttk.Label(quadro, text=rotulo).grid(
            row=indice + 1, column=0, padx=(0, 12), pady=6, sticky="w"
        )
        entrada = ttk.Entry(quadro, width=18)
        entrada.insert(0, valor)
        entrada.grid(row=indice + 1, column=1, pady=6, sticky="ew")
        entradas.append(entrada)

    def salvar_configuracoes():
        valores = validar_valores_configuracao(
            entradas[0].get(),
            entradas[1].get(),
            entradas[2].get(),
            entradas[3].get(),
        )
        if valores is None:
            return

        # Seleção: só pede confirmação quando há algo que possa ser perdido.
        if existem_dados_preenchidos():
            confirmar = messagebox.askyesno(
                "Confirmar alteração",
                "Alterar as configurações poderá apagar os dados cadastrados. Deseja continuar?",
                parent=janela_configuracoes,
            )
            if not confirmar:
                return

        aplicar_configuracoes(*valores)
        janela_configuracoes.destroy()

    def restaurar_padrao():
        entradas[0].delete(0, tk.END)
        entradas[0].insert(0, "5")
        entradas[1].delete(0, tk.END)
        entradas[1].insert(0, "3")
        entradas[2].delete(0, tk.END)
        entradas[2].insert(0, "10")
        entradas[3].delete(0, tk.END)
        entradas[3].insert(0, "6")

    botoes = ttk.Frame(quadro)
    botoes.grid(row=5, column=0, columnspan=2, sticky="e", pady=(14, 0))
    ttk.Button(
        botoes,
        text="Salvar Configurações",
        command=salvar_configuracoes,
    ).grid(row=0, column=0, padx=(0, 8))
    ttk.Button(
        botoes,
        text="Restaurar Padrão",
        command=restaurar_padrao,
    ).grid(row=0, column=1, padx=(0, 8))
    ttk.Button(
        botoes,
        text="Cancelar",
        command=janela_configuracoes.destroy,
    ).grid(row=0, column=2)
    entradas[0].focus()


def validar_configuracao():
    global quantidade_alunos, quantidade_avaliacoes, nota_maxima, media_minima

    try:
        quantidade_alunos = int(entrada_quantidade_alunos.get().strip())
        quantidade_avaliacoes = int(entrada_quantidade_avaliacoes.get().strip())
        nota_maxima = ler_numero(entrada_nota_maxima.get())
        media_minima = ler_numero(entrada_media_minima.get())
    except ValueError:
        messagebox.showerror(
            "Configuração inválida",
            "Informe números válidos em todos os campos.",
        )
        return False

    # Seleção: quantidades precisam ser inteiras positivas.
    if quantidade_alunos <= 0 or quantidade_avaliacoes <= 0:
        messagebox.showerror(
            "Configuração inválida",
            "A quantidade de alunos e avaliações deve ser maior que zero.",
        )
        return False

    # Seleção: a escala e a média mínima não podem ser negativas.
    if nota_maxima <= 0 or media_minima < 0 or media_minima > nota_maxima:
        messagebox.showerror(
            "Configuração inválida",
            "A nota máxima deve ser positiva e a média mínima deve estar entre zero e a nota máxima.",
        )
        return False

    return True


def criar_formulario_dinamico():
    global alunos, notas, campos_nomes, campos_notas

    alunos = ["" for _ in range(quantidade_alunos)]
    notas = [
        [0.0 for _ in range(quantidade_avaliacoes)]
        for _ in range(quantidade_alunos)
    ]
    campos_nomes = []
    campos_notas = []

    # destroy() remove os widgets antigos antes de reconstruir a tabela.
    for widget in formulario_frame.winfo_children():
        widget.destroy()

    cabecalhos = ["Aluno", "Nome"]
    # Repetição: cria um cabeçalho para cada avaliação configurada.
    for indice_avaliacao in range(quantidade_avaliacoes):
        cabecalhos.append(f"Avaliação {indice_avaliacao + 1}")

    for coluna, texto in enumerate(cabecalhos):
        ttk.Label(formulario_frame, text=texto).grid(
            row=0, column=coluna, padx=6, pady=(0, 6), sticky="w"
        )

    # Repetição: cria uma linha para cada aluno e suas avaliações.
    for indice_aluno in range(quantidade_alunos):
        ttk.Label(formulario_frame, text=str(indice_aluno + 1)).grid(
            row=indice_aluno + 1, column=0, padx=6, pady=5
        )
        campo_nome = ttk.Entry(formulario_frame, width=28)
        campo_nome.grid(
            row=indice_aluno + 1,
            column=1,
            padx=6,
            pady=5,
            sticky="ew",
        )
        campos_nomes.append(campo_nome)

        linha_campos = []
        # Repetição aninhada: cria uma entrada para cada nota da linha.
        for indice_avaliacao in range(quantidade_avaliacoes):
            campo_nota = ttk.Entry(formulario_frame, width=14)
            campo_nota.grid(
                row=indice_aluno + 1,
                column=indice_avaliacao + 2,
                padx=6,
                pady=5,
            )
            linha_campos.append(campo_nota)
        campos_notas.append(linha_campos)

    formulario_frame.columnconfigure(1, weight=1)
    status_var.set(
        f"Cadastro criado para {quantidade_alunos} alunos e "
        f"{quantidade_avaliacoes} avaliações."
    )


def iniciar_cadastro():
    if validar_configuracao():
        criar_formulario_dinamico()
        configurar_tabela_resultados()
        mostrar_frame(cadastro_frame)
        campos_nomes[0].focus()


def ler_dados():
    global alunos, notas

    novos_alunos = []
    novas_notas = []

    # Repetição: percorre todas as linhas do formulário.
    for indice_aluno in range(quantidade_alunos):
        # strip() remove espaços extras do nome digitado.
        nome = campos_nomes[indice_aluno].get().strip()
        if nome == "":
            messagebox.showwarning(
                "Dados incompletos",
                f"Informe o nome do aluno {indice_aluno + 1}.",
            )
            campos_nomes[indice_aluno].focus()
            return False

        notas_aluno = []
        # Repetição aninhada: percorre as avaliações do aluno atual.
        for indice_avaliacao in range(quantidade_avaliacoes):
            texto_nota = campos_notas[indice_aluno][indice_avaliacao].get()
            if texto_nota.strip() == "":
                messagebox.showwarning(
                    "Dados incompletos",
                    f"Informe a avaliação {indice_avaliacao + 1} de {nome}.",
                )
                campos_notas[indice_aluno][indice_avaliacao].focus()
                return False

            try:
                nota = ler_numero(texto_nota)
            except ValueError:
                messagebox.showerror(
                    "Nota inválida",
                    f"A avaliação {indice_avaliacao + 1} de {nome} deve ser numérica.",
                )
                campos_notas[indice_aluno][indice_avaliacao].focus()
                return False

            # Seleção: impede notas menores que zero ou maiores que a escala.
            if nota < 0 or nota > nota_maxima:
                messagebox.showerror(
                    "Nota fora do intervalo",
                    f"A avaliação {indice_avaliacao + 1} de {nome} deve estar entre 0 e {formatar_numero(nota_maxima)}.",
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

    limpar_tabela()
    total_medias = 0.0
    quantidade_aprovados = 0
    quantidade_reprovados = 0
    maior_media = 0.0
    menor_media = 0.0
    nome_maior_media = ""
    nome_menor_media = ""

    # Repetição: calcula e exibe o resultado de cada aluno.
    for indice_aluno in range(quantidade_alunos):
        soma = 0.0
        # Acumulação manual das notas, substituindo sum().
        for indice_avaliacao in range(quantidade_avaliacoes):
            soma = soma + notas[indice_aluno][indice_avaliacao]
        media = soma / quantidade_avaliacoes
        total_medias = total_medias + media

        # Seleção: classifica conforme a média mínima configurada.
        if media >= media_minima:
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

        valores = [indice_aluno + 1, alunos[indice_aluno]]
        # Repetição: monta as colunas de notas conforme a configuração.
        for nota in notas[indice_aluno]:
            valores.append(formatar_numero(nota))
        valores.append(formatar_numero(soma))
        valores.append(formatar_numero(media))
        valores.append(situacao)
        tabela.insert("", tk.END, values=valores)

    media_turma = total_medias / quantidade_alunos
    resumo_var.set(
        f"Média da turma: {formatar_numero(media_turma)} | "
        f"Aprovados: {quantidade_aprovados} | "
        f"Reprovados: {quantidade_reprovados} | "
        f"Maior média: {nome_maior_media} ({formatar_numero(maior_media)}) | "
        f"Menor média: {nome_menor_media} ({formatar_numero(menor_media)})"
    )
    status_var.set("Resultados calculados com sucesso.")


def configurar_tabela_resultados():
    global tabela, colunas_resultado

    for widget in resultados_frame.winfo_children():
        widget.destroy()

    colunas_resultado = ["posicao", "aluno"]
    for indice_avaliacao in range(quantidade_avaliacoes):
        colunas_resultado.append(f"av{indice_avaliacao + 1}")
    colunas_resultado.extend(["soma", "media", "situacao"])

    tabela = ttk.Treeview(
        resultados_frame,
        columns=colunas_resultado,
        show="headings",
    )
    titulos = {
        "posicao": "#",
        "aluno": "Aluno",
        "soma": "Soma",
        "media": "Média",
        "situacao": "Situação",
    }
    larguras = {"posicao": 45, "aluno": 190, "soma": 90, "media": 90, "situacao": 105}
    for indice_avaliacao in range(quantidade_avaliacoes):
        chave = f"av{indice_avaliacao + 1}"
        titulos[chave] = f"Avaliação {indice_avaliacao + 1}"
        larguras[chave] = 100

    # Repetição: configura título e largura de cada coluna dinâmica.
    for coluna in colunas_resultado:
        tabela.heading(coluna, text=titulos[coluna])
        tabela.column(coluna, width=larguras[coluna], anchor="center")
    tabela.grid(row=0, column=0, sticky="nsew")
    resultados_frame.columnconfigure(0, weight=1)
    resultados_frame.rowconfigure(0, weight=1)


def limpar_formulario():
    for campo in campos_nomes:
        campo.delete(0, tk.END)
    for linha in campos_notas:
        for campo in linha:
            campo.delete(0, tk.END)
    limpar_tabela()
    resumo_var.set("Preencha os dados e clique em Calcular Resultados.")
    status_var.set("Formulário limpo. Pronto para um novo preenchimento.")


def nova_turma():
    limpar_formulario()
    mostrar_frame(configuracao_frame)
    entrada_quantidade_alunos.focus()
    status_var.set("Configure a nova turma.")


def criar_interface():
    global janela, configuracao_frame, cadastro_frame, formulario_frame
    global resultados_frame, canvas_formulario, canvas_resultados
    global resumo_var, status_var, entrada_quantidade_alunos
    global entrada_quantidade_avaliacoes, entrada_nota_maxima, entrada_media_minima

    janela = tk.Tk()
    janela.title("Controle de Notas da Turma")
    janela.minsize(980, 620)
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    estilo = ttk.Style()
    estilo.configure("Titulo.TLabel", font=("Segoe UI", 16, "bold"))
    estilo.configure("Resumo.TLabel", font=("Segoe UI", 10, "bold"))
    estilo.configure("Treeview", rowheight=28)

    principal = ttk.Frame(janela, padding=16)
    principal.grid(row=0, column=0, sticky="nsew")
    principal.columnconfigure(0, weight=1)
    principal.rowconfigure(1, weight=1)

    barra_superior = ttk.Frame(principal)
    barra_superior.grid(row=0, column=0, sticky="ew", pady=(0, 10))
    barra_superior.columnconfigure(0, weight=1)
    ttk.Label(
        barra_superior,
        text="Controle de Notas da Turma",
        style="Titulo.TLabel",
    ).grid(row=0, column=0, sticky="w")
    ttk.Button(
        barra_superior,
        text="⚙ Configurações",
        command=abrir_configuracoes,
    ).grid(row=0, column=1, sticky="e")

    configuracao_frame = ttk.Frame(principal)
    configuracao_frame.grid(row=1, column=0, sticky="nsew")
    configuracao_frame.columnconfigure(0, weight=1)

    ttk.Label(
        configuracao_frame,
        text="Configuração da turma",
        style="Titulo.TLabel",
    ).grid(row=0, column=0, sticky="w", pady=(0, 6))
    ttk.Label(
        configuracao_frame,
        text="Defina a quantidade de alunos, avaliações e a escala de notas.",
    ).grid(row=1, column=0, sticky="w", pady=(0, 18))

    quadro_configuracao = ttk.LabelFrame(
        configuracao_frame,
        text="Parâmetros",
        padding=16,
    )
    quadro_configuracao.grid(row=2, column=0, sticky="w")
    campos_configuracao = [
        ("Quantidade de alunos:", "5"),
        ("Quantidade de avaliações:", "3"),
        ("Nota máxima:", "10"),
        ("Média mínima para aprovação:", "6"),
    ]
    entradas = []
    # Repetição: cria os quatro campos da configuração inicial.
    for indice, (rotulo, valor) in enumerate(campos_configuracao):
        ttk.Label(quadro_configuracao, text=rotulo).grid(
            row=indice, column=0, padx=8, pady=8, sticky="w"
        )
        entrada = ttk.Entry(quadro_configuracao, width=18)
        entrada.insert(0, valor)
        entrada.grid(row=indice, column=1, padx=8, pady=8, sticky="w")
        entradas.append(entrada)

    entrada_quantidade_alunos = entradas[0]
    entrada_quantidade_avaliacoes = entradas[1]
    entrada_nota_maxima = entradas[2]
    entrada_media_minima = entradas[3]
    ttk.Button(
        configuracao_frame,
        text="Iniciar Cadastro",
        command=iniciar_cadastro,
    ).grid(row=3, column=0, sticky="w", pady=16)

    cadastro_frame = ttk.Frame(principal)
    cadastro_frame.grid(row=1, column=0, sticky="nsew")
    cadastro_frame.columnconfigure(0, weight=1)
    cadastro_frame.rowconfigure(1, weight=1)
    cadastro_frame.rowconfigure(3, weight=1)

    ttk.Label(
        cadastro_frame,
        text="Cadastro e resultados",
        style="Titulo.TLabel",
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))

    area_formulario = ttk.LabelFrame(cadastro_frame, text="Dados dos alunos", padding=10)
    area_formulario.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
    area_formulario.columnconfigure(0, weight=1)
    area_formulario.rowconfigure(0, weight=1)
    canvas_formulario = tk.Canvas(area_formulario, highlightthickness=0)
    barra_formulario_vertical = ttk.Scrollbar(
        area_formulario, orient="vertical", command=canvas_formulario.yview
    )
    barra_formulario_horizontal = ttk.Scrollbar(
        area_formulario, orient="horizontal", command=canvas_formulario.xview
    )
    canvas_formulario.configure(
        yscrollcommand=barra_formulario_vertical.set,
        xscrollcommand=barra_formulario_horizontal.set,
    )
    canvas_formulario.grid(row=0, column=0, sticky="nsew")
    barra_formulario_vertical.grid(row=0, column=1, sticky="ns")
    barra_formulario_horizontal.grid(row=1, column=0, sticky="ew")
    formulario_frame = ttk.Frame(canvas_formulario)
    canvas_formulario.create_window((0, 0), window=formulario_frame, anchor="nw")
    formulario_frame.bind(
        "<Configure>",
        lambda evento: canvas_formulario.configure(scrollregion=canvas_formulario.bbox("all")),
    )

    botoes = ttk.Frame(cadastro_frame)
    botoes.grid(row=2, column=0, sticky="e", pady=(0, 10))
    ttk.Button(botoes, text="Calcular Resultados", command=calcular_resultados).grid(
        row=0, column=0, padx=(0, 8)
    )
    ttk.Button(botoes, text="Limpar", command=limpar_formulario).grid(
        row=0, column=1, padx=(0, 8)
    )
    ttk.Button(botoes, text="Nova Turma", command=nova_turma).grid(row=0, column=2)

    area_resultados = ttk.LabelFrame(cadastro_frame, text="Resultados", padding=10)
    area_resultados.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
    area_resultados.columnconfigure(0, weight=1)
    area_resultados.rowconfigure(0, weight=1)
    canvas_resultados = tk.Canvas(area_resultados, highlightthickness=0)
    barra_resultados_horizontal = ttk.Scrollbar(
        area_resultados, orient="horizontal", command=canvas_resultados.xview
    )
    canvas_resultados.configure(xscrollcommand=barra_resultados_horizontal.set)
    canvas_resultados.grid(row=0, column=0, sticky="nsew")
    barra_resultados_horizontal.grid(row=1, column=0, sticky="ew")
    resultados_frame = ttk.Frame(canvas_resultados)
    canvas_resultados.create_window((0, 0), window=resultados_frame, anchor="nw")
    resultados_frame.bind(
        "<Configure>",
        lambda evento: canvas_resultados.configure(scrollregion=canvas_resultados.bbox("all")),
    )

    resumo_var = tk.StringVar(value="Preencha os dados e clique em Calcular Resultados.")
    ttk.Label(
        cadastro_frame,
        textvariable=resumo_var,
        style="Resumo.TLabel",
        wraplength=950,
    ).grid(row=4, column=0, sticky="w", pady=(0, 4))
    status_var = tk.StringVar(value="Configure a turma para iniciar.")
    ttk.Label(cadastro_frame, textvariable=status_var).grid(
        row=5, column=0, sticky="w"
    )

    configurar_tabela_resultados()
    mostrar_frame(configuracao_frame)
    janela.mainloop()


if __name__ == "__main__":
    criar_interface()
