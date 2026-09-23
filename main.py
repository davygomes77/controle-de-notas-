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
painel_principal = None
pagina_painel = None
pagina_resultados = None
pagina_relatorio = None
area_formulario = None
area_resultados = None
botoes_cadastro = None
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
rotulo_pagina = None
cartoes_valores = []
relatorio_var = None
botoes_navegacao = []

COR_AZUL = "#064B73"
COR_AZUL_ESCURO = "#04344F"
COR_AZUL_CLARO = "#E8F2F7"
COR_FUNDO = "#F4F7F9"
COR_BORDA = "#D7E1E7"
COR_VERDE = "#197A5A"
COR_VERMELHO = "#B84A4A"
COR_TEXTO = "#173042"


def formatar_numero(valor):
    # replace() troca o separador decimal para o padrão usado no Brasil.
    return f"{valor:.2f}".replace(".", ",")


def ler_numero(texto):
    # strip() remove espaços nas extremidades antes da conversão numérica.
    texto_limpo = texto.strip()
    # replace() permite que o usuário use vírgula como separador decimal.
    return float(texto_limpo.replace(",", "."))


def mostrar_frame(frame):
    for pagina in [configuracao_frame, pagina_painel, cadastro_frame, pagina_resultados, pagina_relatorio]:
        if pagina is not None:
            pagina.grid_remove()
    frame.grid(row=0, column=0, sticky="nsew")


def atualizar_cartoes():
    total_aprovados = 0
    total_reprovados = 0
    total_medias = 0.0
    quantidade_processada = 0

    # Repetição: percorre as linhas calculadas para alimentar o painel.
    # len() informa quantos registros existem e substitui a contagem manual.
    for indice_aluno in range(len(alunos)):
        # len() verifica se há uma linha de notas antes do cálculo.
        if indice_aluno < len(notas) and len(notas[indice_aluno]) > 0:
            soma = 0.0
            for nota in notas[indice_aluno]:
                soma = soma + nota
            media = soma / quantidade_avaliacoes
            total_medias = total_medias + media
            quantidade_processada = quantidade_processada + 1
            # Seleção: conta a situação individual da turma.
            if media >= media_minima:
                total_aprovados = total_aprovados + 1
            else:
                total_reprovados = total_reprovados + 1

    media_geral = 0.0
    if quantidade_processada > 0:
        media_geral = total_medias / quantidade_processada

    valores = [
        str(quantidade_processada),
        str(quantidade_avaliacoes),
        formatar_numero(media_geral),
        str(total_aprovados),
        str(total_reprovados),
    ]
    for indice in range(len(cartoes_valores)):
        cartoes_valores[indice].configure(text=valores[indice])

    relatorio_var.set(
        f"Alunos configurados: {quantidade_alunos}\n"
        f"Avaliações por aluno: {quantidade_avaliacoes}\n"
        f"Nota máxima: {formatar_numero(nota_maxima)}\n"
        f"Média mínima para aprovação: {formatar_numero(media_minima)}\n\n"
        f"Média geral: {formatar_numero(media_geral)}\n"
        f"Aprovados: {total_aprovados}\n"
        f"Reprovados: {total_reprovados}"
    )


def mostrar_pagina(nome_pagina):
    paginas = {
        "painel": pagina_painel,
        "cadastro": cadastro_frame,
        "resultados": pagina_resultados,
        "relatorio": pagina_relatorio,
    }
    mostrar_frame(paginas[nome_pagina])
    # Repetição: atualiza o estado visual da opção ativa do menu.
    for botao, nome_botao in botoes_navegacao:
        if nome_botao == nome_pagina:
            botao.configure(background=COR_AZUL)
        else:
            botao.configure(background=COR_AZUL_ESCURO)

    if nome_pagina == "painel":
        atualizar_cartoes()
        rotulo_pagina.configure(text="Painel Inicial")
    elif nome_pagina == "cadastro":
        rotulo_pagina.configure(text="Cadastro de Alunos")
    elif nome_pagina == "resultados":
        atualizar_cartoes()
        rotulo_pagina.configure(text="Resultados")
    elif nome_pagina == "relatorio":
        atualizar_cartoes()
        rotulo_pagina.configure(text="Relatório da Turma")


def abrir_resultados():
    mostrar_pagina("resultados")


def configurar_tags_tabela():
    tabela.tag_configure("aprovado", background="#EAF6F0", foreground="#155B43")
    tabela.tag_configure("reprovado", background="#FCEEEE", foreground="#7E3030")


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
        etiqueta_situacao = "aprovado"
        if situacao == "Reprovado":
            etiqueta_situacao = "reprovado"
        tabela.insert("", tk.END, values=valores, tags=(etiqueta_situacao,))

    media_turma = total_medias / quantidade_alunos
    resumo_var.set(
        f"Média da turma: {formatar_numero(media_turma)} | "
        f"Aprovados: {quantidade_aprovados} | "
        f"Reprovados: {quantidade_reprovados} | "
        f"Maior média: {nome_maior_media} ({formatar_numero(maior_media)}) | "
        f"Menor média: {nome_menor_media} ({formatar_numero(menor_media)})"
    )
    status_var.set("Resultados calculados com sucesso.")
    atualizar_cartoes()


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
    configurar_tags_tabela()
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
    global painel_principal, pagina_painel, pagina_resultados, pagina_relatorio
    global area_formulario, area_resultados, botoes_cadastro, rotulo_pagina
    global cartoes_valores, relatorio_var, botoes_navegacao

    janela = tk.Tk()
    janela.title("UEMG | Sistema de Controle de Notas")
    janela.minsize(1050, 680)
    janela.configure(background=COR_FUNDO)
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(1, weight=1)

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Titulo.TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=("Segoe UI", 18, "bold"))
    estilo.configure("Subtitulo.TLabel", background=COR_FUNDO, foreground="#5C7180", font=("Segoe UI", 10))
    estilo.configure("Resumo.TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=("Segoe UI", 10, "bold"))
    estilo.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
    estilo.configure("CardTitulo.TLabel", background="white", foreground="#607886", font=("Segoe UI", 9, "bold"))
    estilo.configure("CardValor.TLabel", background="white", foreground=COR_TEXTO, font=("Segoe UI", 22, "bold"))
    estilo.configure("Secao.TLabelframe", background="white", foreground=COR_AZUL, bordercolor=COR_BORDA)
    estilo.configure("Secao.TLabelframe.Label", background="white", foreground=COR_AZUL, font=("Segoe UI", 10, "bold"))
    estilo.configure("Treeview", background="white", fieldbackground="white", foreground=COR_TEXTO, rowheight=32, font=("Segoe UI", 9))
    estilo.configure("Treeview.Heading", background=COR_AZUL, foreground="white", font=("Segoe UI", 9, "bold"))
    estilo.map("Treeview.Heading", background=[("active", COR_AZUL_ESCURO)])
    estilo.configure("Acao.TButton", background=COR_AZUL, foreground="white", padding=(14, 8), font=("Segoe UI", 9, "bold"))
    estilo.map("Acao.TButton", background=[("active", COR_AZUL_ESCURO)])
    estilo.configure("Secundario.TButton", background="#E7EEF2", foreground=COR_TEXTO, padding=(14, 8))

    cabecalho = tk.Frame(janela, background=COR_AZUL, height=82)
    cabecalho.grid(row=0, column=0, sticky="ew")
    cabecalho.grid_propagate(False)
    cabecalho.columnconfigure(1, weight=1)
    tk.Label(cabecalho, text="UEMG", background=COR_AZUL, foreground="white", font=("Segoe UI", 22, "bold")).grid(row=0, column=0, rowspan=2, padx=(24, 18), pady=12)
    tk.Label(cabecalho, text="Universidade do Estado de Minas Gerais", background=COR_AZUL, foreground="white", font=("Segoe UI", 11, "bold")).grid(row=0, column=1, sticky="sw", pady=(14, 0))
    tk.Label(cabecalho, text="Sistema de Controle de Notas", background=COR_AZUL, foreground="#DCEBF2", font=("Segoe UI", 10)).grid(row=1, column=1, sticky="nw", pady=(2, 14))
    tk.Button(cabecalho, text="⚙  Configurações", command=abrir_configuracoes, background=COR_AZUL_ESCURO, foreground="white", activebackground="#0A5C87", activeforeground="white", relief="flat", padx=14, pady=8, font=("Segoe UI", 9, "bold")).grid(row=0, column=2, rowspan=2, padx=24)

    corpo = ttk.Frame(janela)
    corpo.grid(row=1, column=0, sticky="nsew")
    corpo.columnconfigure(1, weight=1)
    corpo.rowconfigure(0, weight=1)
    menu = tk.Frame(corpo, background=COR_AZUL_ESCURO, width=218)
    menu.grid(row=0, column=0, sticky="nsew")
    menu.grid_propagate(False)
    tk.Label(menu, text="NAVEGAÇÃO", background=COR_AZUL_ESCURO, foreground="#AFC9D5", font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=20, pady=(24, 12))
    opcoes_menu = [("⌂  Painel Inicial", "painel"), ("✎  Cadastro de Alunos", "cadastro"), ("▤  Resultados", "resultados"), ("▥  Relatório da Turma", "relatorio")]
    botoes_navegacao = []
    for texto, nome in opcoes_menu:
        botao_menu = tk.Button(menu, text=texto, command=lambda pagina=nome: mostrar_pagina(pagina), anchor="w", background=COR_AZUL_ESCURO, foreground="white", activebackground=COR_AZUL, activeforeground="white", relief="flat", bd=0, padx=20, pady=12, font=("Segoe UI", 10))
        botao_menu.pack(fill="x")
        botoes_navegacao.append((botao_menu, nome))
    tk.Frame(menu, background="#315D74", height=1).pack(fill="x", padx=20, pady=24)
    tk.Label(menu, text="UEMG • Gestão acadêmica", background=COR_AZUL_ESCURO, foreground="#AFC9D5", font=("Segoe UI", 8)).pack(anchor="w", padx=20)

    painel_principal = ttk.Frame(corpo, padding=24)
    painel_principal.grid(row=0, column=1, sticky="nsew")
    painel_principal.columnconfigure(0, weight=1)
    painel_principal.rowconfigure(0, weight=1)

    topo_pagina = ttk.Frame(painel_principal)
    topo_pagina.grid(row=0, column=0, sticky="ew", pady=(0, 16))
    topo_pagina.columnconfigure(0, weight=1)
    rotulo_pagina = ttk.Label(topo_pagina, text="Painel Inicial", style="Titulo.TLabel")
    rotulo_pagina.grid(row=0, column=0, sticky="w")
    ttk.Label(topo_pagina, text="Acompanhe o desempenho acadêmico da turma em um só lugar.", style="Subtitulo.TLabel").grid(row=1, column=0, sticky="w", pady=(4, 0))

    conteudo = ttk.Frame(painel_principal)
    conteudo.grid(row=1, column=0, sticky="nsew")
    conteudo.columnconfigure(0, weight=1)
    conteudo.rowconfigure(0, weight=1)

    pagina_painel = ttk.Frame(conteudo)
    pagina_painel.grid(row=0, column=0, sticky="nsew")
    pagina_painel.columnconfigure(0, weight=1)
    ttk.Label(pagina_painel, text="Visão geral da turma", style="Subtitulo.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 12))
    grade_cartoes = ttk.Frame(pagina_painel)
    grade_cartoes.grid(row=1, column=0, sticky="ew")
    for coluna in range(5):
        grade_cartoes.columnconfigure(coluna, weight=1)
    dados_cartoes = [("TOTAL DE ALUNOS", COR_AZUL), ("AVALIAÇÕES", "#437E98"), ("MÉDIA GERAL", "#7A638F"), ("APROVADOS", COR_VERDE), ("REPROVADOS", COR_VERMELHO)]
    cartoes_valores = []
    # Repetição: cria cartões consistentes para as métricas do painel.
    for indice, (titulo, cor) in enumerate(dados_cartoes):
        cartao = ttk.Frame(grade_cartoes, style="Card.TFrame", padding=14)
        cartao.grid(row=0, column=indice, sticky="nsew", padx=(0 if indice == 0 else 5, 5 if indice < 4 else 0))
        tk.Frame(cartao, background=cor, height=4).pack(fill="x", pady=(0, 12))
        ttk.Label(cartao, text=titulo, style="CardTitulo.TLabel").pack(anchor="w")
        valor = ttk.Label(cartao, text="0", style="CardValor.TLabel")
        valor.pack(anchor="w", pady=(6, 0))
        cartoes_valores.append(valor)
    ttk.Label(pagina_painel, text="Use o menu lateral para cadastrar alunos, calcular resultados ou consultar o relatório geral.", style="Subtitulo.TLabel").grid(row=2, column=0, sticky="w", pady=(26, 0))

    configuracao_frame = ttk.Frame(conteudo)
    configuracao_frame.grid(row=0, column=0, sticky="nsew")
    quadro_configuracao = ttk.LabelFrame(configuracao_frame, text="Configuração inicial", padding=16, style="Secao.TLabelframe")
    quadro_configuracao.grid(row=0, column=0, sticky="nw")
    campos_configuracao = [("Quantidade de alunos:", "5"), ("Quantidade de avaliações:", "3"), ("Nota máxima:", "10"), ("Média mínima para aprovação:", "6")]
    entradas = []
    # Repetição: cria os campos iniciais com organização institucional.
    for indice, (rotulo, valor) in enumerate(campos_configuracao):
        ttk.Label(quadro_configuracao, text=rotulo).grid(row=indice, column=0, padx=8, pady=8, sticky="w")
        entrada = ttk.Entry(quadro_configuracao, width=18)
        entrada.insert(0, valor)
        entrada.grid(row=indice, column=1, padx=8, pady=8, sticky="w")
        entradas.append(entrada)
    entrada_quantidade_alunos, entrada_quantidade_avaliacoes, entrada_nota_maxima, entrada_media_minima = entradas
    ttk.Button(configuracao_frame, text="Iniciar Cadastro", style="Acao.TButton", command=iniciar_cadastro).grid(row=1, column=0, sticky="w", pady=16)

    cadastro_frame = ttk.Frame(conteudo)
    cadastro_frame.grid(row=0, column=0, sticky="nsew")
    cadastro_frame.columnconfigure(0, weight=1)
    cadastro_frame.rowconfigure(0, weight=1)
    area_formulario = ttk.LabelFrame(cadastro_frame, text="Dados dos alunos e avaliações", padding=10, style="Secao.TLabelframe")
    area_formulario.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
    area_formulario.columnconfigure(0, weight=1)
    area_formulario.rowconfigure(0, weight=1)
    canvas_formulario = tk.Canvas(area_formulario, background="white", highlightthickness=0)
    barra_formulario_vertical = ttk.Scrollbar(area_formulario, orient="vertical", command=canvas_formulario.yview)
    barra_formulario_vertical.grid(row=0, column=1, sticky="ns")
    barra_formulario_horizontal = ttk.Scrollbar(area_formulario, orient="horizontal", command=canvas_formulario.xview)
    barra_formulario_horizontal.grid(row=1, column=0, sticky="ew")
    canvas_formulario.grid(row=0, column=0, sticky="nsew")
    canvas_formulario.configure(yscrollcommand=barra_formulario_vertical.set, xscrollcommand=barra_formulario_horizontal.set)
    formulario_frame = ttk.Frame(canvas_formulario)
    canvas_formulario.create_window((0, 0), window=formulario_frame, anchor="nw")
    formulario_frame.bind("<Configure>", lambda evento: canvas_formulario.configure(scrollregion=canvas_formulario.bbox("all")))
    botoes_cadastro = ttk.Frame(cadastro_frame)
    botoes_cadastro.grid(row=1, column=0, sticky="e")
    ttk.Button(botoes_cadastro, text="Calcular Resultados", style="Acao.TButton", command=calcular_resultados).grid(row=0, column=0, padx=(0, 8))
    ttk.Button(botoes_cadastro, text="Limpar", style="Secundario.TButton", command=limpar_formulario).grid(row=0, column=1, padx=(0, 8))
    ttk.Button(botoes_cadastro, text="Nova Turma", style="Secundario.TButton", command=nova_turma).grid(row=0, column=2)

    pagina_resultados = ttk.Frame(conteudo)
    pagina_resultados.grid(row=0, column=0, sticky="nsew")
    pagina_resultados.columnconfigure(0, weight=1)
    pagina_resultados.rowconfigure(0, weight=1)
    resultados_frame = ttk.Frame(pagina_resultados)
    resultados_frame.grid(row=0, column=0, sticky="nsew")
    pagina_resultados.rowconfigure(1, weight=0)
    resumo_var = tk.StringVar(value="Preencha o cadastro e clique em Calcular Resultados.")
    ttk.Label(pagina_resultados, textvariable=resumo_var, style="Resumo.TLabel", wraplength=950).grid(row=1, column=0, sticky="w", pady=(14, 0))

    pagina_relatorio = ttk.Frame(conteudo)
    pagina_relatorio.grid(row=0, column=0, sticky="nsew")
    pagina_relatorio.columnconfigure(0, weight=1)
    ttk.Label(pagina_relatorio, text="Resumo executivo", style="Subtitulo.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 12))
    relatorio_var = tk.StringVar(value="Configure a turma para iniciar.")
    ttk.Label(pagina_relatorio, textvariable=relatorio_var, justify="left", style="Resumo.TLabel").grid(row=1, column=0, sticky="nw")

    status_var = tk.StringVar(value="Configure a turma ou acesse o painel inicial.")
    ttk.Label(painel_principal, textvariable=status_var, style="Subtitulo.TLabel").grid(row=2, column=0, sticky="w", pady=(12, 0))

    configurar_tabela_resultados()
    mostrar_pagina("painel")
    janela.mainloop()


if __name__ == "__main__":
    criar_interface()
