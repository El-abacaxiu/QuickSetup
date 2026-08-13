import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import subprocess
import threading
import sys
import os


# ============================================================
# QUICK SETUP 2.0
# Interface redesign inspired by the Quick Setup website
# ============================================================

APP_TITLE = "QuickSetup"
APP_VERSION = "2.0 UI"

# Cores inspiradas no site
BLUE = "#3B82F6"
BLUE_HOVER = "#2563EB"

DARK_BG = "#171717"
DARK_SIDEBAR = "#1C1C1C"
DARK_CARD = "#222222"
DARK_CARD_2 = "#262626"
DARK_BORDER = "#303030"
DARK_TEXT = "#F2F2F2"
DARK_MUTED = "#A3A3A3"

LIGHT_BG = "#F4F4F5"
LIGHT_SIDEBAR = "#EDEDED"
LIGHT_CARD = "#FFFFFF"
LIGHT_CARD_2 = "#F3F3F3"
LIGHT_BORDER = "#D8D8D8"
LIGHT_TEXT = "#18181B"
LIGHT_MUTED = "#666666"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

modo_atual = "dark"


# ============================================================
# CAMINHOS DE RECURSOS
# ============================================================

def resource_path(rel_path):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, rel_path)


# ============================================================
# PACOTES
# ============================================================

PACOTE_GAMER = {
    "Steam": "Valve.Steam",
    "Discord": "Discord.Discord",
    "MSI Afterburner": "MSI.Afterburner",
    "Epic Games Launcher": "EpicGames.EpicGamesLauncher",
    "OBS Studio": "OBSProject.OBSStudio",
    "DirectX Runtime": "Microsoft.DirectX",
    "Visual C++ Redistributables": "Microsoft.VCRedist.2015+.x64",
    "WinRAR": "RARLab.WinRAR",
}

PACOTE_HOME = {
    "Google Chrome": "Google.Chrome",
    "LibreOffice": "TheDocumentFoundation.LibreOffice",
    "Adobe Reader": "Adobe.Acrobat.Reader.64-bit",
    "VLC Media Player": "VideoLAN.VLC",
    "WinRAR": "RARLab.WinRAR",
    "Everything": "voidtools.Everything",
    "ShareX": "ShareX.ShareX",
}

PACKS = {
    "Gamer": {
        "icon": "🎮",
        "title": "Gamer Pack",
        "subtitle": "Tudo para deixar seu Windows pronto para jogar.",
        "apps": PACOTE_GAMER,
    },
    "Home": {
        "icon": "⌂",
        "title": "Home Pack",
        "subtitle": "Aplicativos essenciais para uso diário e produtividade.",
        "apps": PACOTE_HOME,
    },
}


# Cada pack possui suas próprias variáveis.
# Isso corrige o problema do WinRAR compartilhar a mesma checkbox
# entre Gamer e Home na versão antiga.
checkbox_vars = {
    "Gamer": {},
    "Home": {},
}

install_buttons = []
current_pack = "Gamer"
installing = False


# ============================================================
# TEMA / CORES
# ============================================================

def colors():
    if modo_atual == "dark":
        return {
            "bg": DARK_BG,
            "sidebar": DARK_SIDEBAR,
            "card": DARK_CARD,
            "card2": DARK_CARD_2,
            "border": DARK_BORDER,
            "text": DARK_TEXT,
            "muted": DARK_MUTED,
        }

    return {
        "bg": LIGHT_BG,
        "sidebar": LIGHT_SIDEBAR,
        "card": LIGHT_CARD,
        "card2": LIGHT_CARD_2,
        "border": LIGHT_BORDER,
        "text": LIGHT_TEXT,
        "muted": LIGHT_MUTED,
    }


# ============================================================
# JANELA
# ============================================================

app = ctk.CTk()

app.title("QuickSetup")
app.geometry("1050x680")
app.minsize(760, 520)

try:
    app.iconbitmap(resource_path("template.ico"))
except Exception:
    pass

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)


# ============================================================
# IMAGEM / LOGO
# ============================================================

logo_img = None

try:
    logo_img = ctk.CTkImage(
        light_image=Image.open(resource_path("template.jpg")),
        dark_image=Image.open(resource_path("template.jpg")),
        size=(30, 30),
    )
except Exception:
    logo_img = None


# ============================================================
# SIDEBAR
# ============================================================

sidebar = ctk.CTkFrame(
    app,
    width=205,
    corner_radius=0,
    fg_color=colors()["sidebar"],
)

sidebar.grid(row=0, column=0, sticky="nsew")
sidebar.grid_propagate(False)
sidebar.grid_rowconfigure(5, weight=1)


brand = ctk.CTkLabel(
    sidebar,
    text="  QuickSetup",
    image=logo_img,
    compound="left",
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color=colors()["text"],
)

brand.grid(row=0, column=0, padx=18, pady=(28, 35), sticky="w")


def sidebar_button(text, command):
    return ctk.CTkButton(
        sidebar,
        text=text,
        command=command,
        height=42,
        corner_radius=9,
        fg_color=BLUE,
        hover_color=BLUE_HOVER,
        text_color="white",
        font=ctk.CTkFont(size=14, weight="bold"),
    )


btn_gamer = sidebar_button("🎮  Gamer", lambda: trocar_pack("Gamer"))
btn_gamer.grid(row=1, column=0, padx=14, pady=5, sticky="ew")

btn_home = sidebar_button("⌂  Home", lambda: trocar_pack("Home"))
btn_home.grid(row=2, column=0, padx=14, pady=5, sticky="ew")


# Área inferior da sidebar
sidebar_bottom = ctk.CTkFrame(
    sidebar,
    fg_color="transparent",
)
sidebar_bottom.grid(row=6, column=0, padx=14, pady=(10, 18), sticky="ew")


theme_button = ctk.CTkButton(
    sidebar_bottom,
    text="☾  Tema",
    command=lambda: alternar_tema(),
    height=40,
    corner_radius=9,
    fg_color=colors()["card2"],
    hover_color=BLUE,
    text_color=colors()["text"],
    border_width=1,
    border_color=colors()["border"],
)

theme_button.pack(fill="x")


version_label = ctk.CTkLabel(
    sidebar_bottom,
    text=f"QuickSetup {APP_VERSION}",
    font=ctk.CTkFont(size=10),
    text_color=colors()["muted"],
)

version_label.pack(pady=(10, 0))


# ============================================================
# ÁREA PRINCIPAL
# ============================================================

main = ctk.CTkFrame(
    app,
    corner_radius=0,
    fg_color=colors()["bg"],
)

main.grid(row=0, column=1, sticky="nsew")
main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(1, weight=1)


# Cabeçalho
header = ctk.CTkFrame(
    main,
    fg_color="transparent",
)

header.grid(row=0, column=0, padx=30, pady=(28, 8), sticky="ew")
header.grid_columnconfigure(0, weight=1)


title_label = ctk.CTkLabel(
    header,
    text="",
    font=ctk.CTkFont(size=28, weight="bold"),
    text_color=colors()["text"],
)

title_label.grid(row=0, column=0, sticky="w")


subtitle_label = ctk.CTkLabel(
    header,
    text="",
    font=ctk.CTkFont(size=13),
    text_color=colors()["muted"],
)

subtitle_label.grid(row=1, column=0, pady=(4, 0), sticky="w")


# Indicador de selecionados
selected_label = ctk.CTkLabel(
    header,
    text="",
    font=ctk.CTkFont(size=12, weight="bold"),
    text_color=BLUE,
)

selected_label.grid(row=0, column=1, rowspan=2, padx=(15, 0), sticky="e")


# ============================================================
# ÁREA ROLÁVEL DOS APPS
# ============================================================

apps_area = ctk.CTkScrollableFrame(
    main,
    corner_radius=14,
    fg_color=colors()["card"],
    border_width=1,
    border_color=colors()["border"],
)

apps_area.grid(
    row=1,
    column=0,
    padx=30,
    pady=(8, 12),
    sticky="nsew",
)


# ============================================================
# BARRA INFERIOR
# ============================================================

bottom = ctk.CTkFrame(
    main,
    fg_color="transparent",
)

bottom.grid(row=2, column=0, padx=30, pady=(0, 24), sticky="ew")
bottom.grid_columnconfigure(0, weight=1)


progress_frame = ctk.CTkFrame(
    bottom,
    fg_color="transparent",
)

progress_frame.grid(row=0, column=0, sticky="ew")
progress_frame.grid_columnconfigure(0, weight=1)


progress_bar = ctk.CTkProgressBar(
    progress_frame,
    height=7,
    corner_radius=5,
    progress_color=BLUE,
    fg_color=colors()["border"],
)

progress_bar.grid(row=0, column=0, sticky="ew")
progress_bar.set(0)


status_label = ctk.CTkLabel(
    progress_frame,
    text="Pronto para começar 🚀",
    font=ctk.CTkFont(size=12),
    text_color=colors()["muted"],
)

status_label.grid(row=1, column=0, pady=(6, 0), sticky="w")


action_frame = ctk.CTkFrame(
    bottom,
    fg_color="transparent",
)

action_frame.grid(row=0, column=1, padx=(18, 0), sticky="e")


select_all_button = ctk.CTkButton(
    action_frame,
    text="Selecionar tudo",
    command=lambda: marcar_todos(current_pack),
    height=42,
    corner_radius=9,
    fg_color=colors()["card2"],
    hover_color=BLUE,
    text_color=colors()["text"],
    border_width=1,
    border_color=colors()["border"],
)

select_all_button.grid(row=0, column=0, padx=(0, 8))


install_button = ctk.CTkButton(
    action_frame,
    text="Instalar Pack",
    command=lambda: instalar_selecionados(current_pack),
    height=42,
    corner_radius=9,
    fg_color=BLUE,
    hover_color=BLUE_HOVER,
    text_color="white",
    font=ctk.CTkFont(size=13, weight="bold"),
)

install_button.grid(row=0, column=1)

install_buttons.append(install_button)


# ============================================================
# FUNÇÕES DE UI
# ============================================================

def atualizar_cores():
    c = colors()

    app.configure(fg_color=c["bg"])
    sidebar.configure(fg_color=c["sidebar"])
    main.configure(fg_color=c["bg"])

    brand.configure(text_color=c["text"])
    title_label.configure(text_color=c["text"])
    subtitle_label.configure(text_color=c["muted"])
    selected_label.configure(text_color=BLUE)
    status_label.configure(text_color=c["muted"])
    version_label.configure(text_color=c["muted"])

    theme_button.configure(
        fg_color=c["card2"],
        hover_color=BLUE,
        text_color=c["text"],
        border_color=c["border"],
    )

    select_all_button.configure(
        fg_color=c["card2"],
        hover_color=BLUE,
        text_color=c["text"],
        border_color=c["border"],
    )

    progress_bar.configure(fg_color=c["border"])

    apps_area.configure(
        fg_color=c["card"],
        border_color=c["border"],
    )


def alternar_tema():
    global modo_atual

    modo_atual = "light" if modo_atual == "dark" else "dark"

    ctk.set_appearance_mode(modo_atual)
    atualizar_cores()
    trocar_pack(current_pack)


def trocar_pack(nome_pack):
    global current_pack

    if installing:
        return

    current_pack = nome_pack

    pack = PACKS[nome_pack]
    c = colors()

    title_label.configure(
        text=f"{pack['icon']}  {pack['title']}"
    )

    subtitle_label.configure(
        text=pack["subtitle"]
    )

    install_button.configure(
        text=f"Instalar {pack['icon']} {nome_pack}"
    )

    # Estado visual dos botões da sidebar
    if nome_pack == "Gamer":
        btn_gamer.configure(fg_color=BLUE, hover_color=BLUE_HOVER)
        btn_home.configure(
            fg_color=c["card2"],
            hover_color=BLUE,
            text_color=c["text"],
        )
    else:
        btn_home.configure(fg_color=BLUE, hover_color=BLUE_HOVER)
        btn_gamer.configure(
            fg_color=c["card2"],
            hover_color=BLUE,
            text_color=c["text"],
        )

    montar_cards(nome_pack)


def montar_cards(nome_pack):
    c = colors()
    pack = PACKS[nome_pack]

    # Limpa cards antigos
    for widget in apps_area.winfo_children():
        widget.destroy()

    vars_pack = checkbox_vars[nome_pack]

    # Responsividade simples:
    # >= 900 px: 2 colunas
    # < 900 px: 1 coluna
    try:
        largura = apps_area.winfo_width()
    except Exception:
        largura = 900

    colunas = 2 if largura >= 900 else 1

    for coluna in range(colunas):
        apps_area.grid_columnconfigure(coluna, weight=1)

    for index, nome_app in enumerate(pack["apps"]):
        if nome_app not in vars_pack:
            vars_pack[nome_app] = ctk.BooleanVar(value=True)

        var = vars_pack[nome_app]

        card = ctk.CTkFrame(
            apps_area,
            corner_radius=12,
            fg_color=c["card2"],
            border_width=1,
            border_color=c["border"],
        )

        linha = index // colunas
        coluna = index % colunas

        card.grid(
            row=linha,
            column=coluna,
            padx=7,
            pady=7,
            sticky="nsew",
        )

        card.grid_columnconfigure(0, weight=1)

        check = ctk.CTkCheckBox(
            card,
            text=nome_app,
            variable=var,
            command=atualizar_selecionados,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=c["text"],
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            border_color=c["muted"],
            corner_radius=6,
        )

        check.grid(
            row=0,
            column=0,
            padx=15,
            pady=(14, 4),
            sticky="w",
        )

        id_label = ctk.CTkLabel(
            card,
            text=f"winget • {pack['apps'][nome_app]}",
            font=ctk.CTkFont(size=10),
            text_color=c["muted"],
        )

        id_label.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 14),
            sticky="w",
        )

    atualizar_selecionados()


def atualizar_selecionados():
    pack_vars = checkbox_vars[current_pack]
    total = len(PACKS[current_pack]["apps"])
    selecionados = sum(var.get() for var in pack_vars.values())

    selected_label.configure(
        text=f"{selecionados}/{total} selecionados"
    )


def marcar_todos(nome_pack):
    if installing:
        return

    vars_pack = checkbox_vars[nome_pack]

    for nome in PACKS[nome_pack]["apps"]:
        if nome not in vars_pack:
            vars_pack[nome] = ctk.BooleanVar(value=True)
        else:
            vars_pack[nome].set(True)

    atualizar_selecionados()


# ============================================================
# INSTALAÇÃO
# ============================================================

def instalar_selecionados(nome_pack):
    global installing

    if installing:
        return

    pacote = PACKS[nome_pack]["apps"]
    vars_pack = checkbox_vars[nome_pack]

    selecionados = {
        nome: id_pacote
        for nome, id_pacote in pacote.items()
        if vars_pack[nome].get()
    }

    if not selecionados:
        messagebox.showwarning(
            "Nada selecionado",
            "Marque pelo menos 1 aplicativo 😅",
            parent=app,
        )
        return

    installing = True
    set_install_controls("disabled")
    progress_bar.set(0)
    status_label.configure(text="Preparando instalação...")

    threading.Thread(
        target=instalar_pacote,
        args=(selecionados, nome_pack),
        daemon=True,
    ).start()


def instalar_pacote(pacote, nome_pack):
    total = len(pacote)

    for i, (nome, id_pacote) in enumerate(pacote.items(), start=1):
        # Toda alteração da interface volta para a thread principal
        app.after(
            0,
            lambda i=i, nome=nome, total=total:
                atualizar_progresso(i, nome, total)
        )

        try:
            resultado = subprocess.run(
                [
                    "winget",
                    "install",
                    "--id",
                    id_pacote,
                    "-e",
                    "--silent",
                    "--accept-source-agreements",
                    "--accept-package-agreements",
                ],
                capture_output=True,
                text=True,
                shell=False,
            )

            if resultado.returncode != 0:
                app.after(
                    0,
                    lambda nome=nome:
                        status_label.configure(
                            text=f"⚠️ Não foi possível instalar {nome}"
                        ),
                )

        except Exception as erro:
            app.after(
                0,
                lambda nome=nome, erro=erro:
                    status_label.configure(
                        text=f"Erro em {nome}: {erro}"
                    ),
            )

        app.after(
            0,
            lambda i=i, total=total:
                progress_bar.set(i / total)
        )

    app.after(0, finalizar_instalacao, nome_pack)


def atualizar_progresso(i, nome, total):
    status_label.configure(
        text=f"[{i}/{total}] Instalando {nome}..."
    )


def finalizar_instalacao(nome_pack):
    global installing

    installing = False
    set_install_controls("normal")

    status_label.configure(
        text="Tudo pronto 🚀"
    )

    messagebox.showinfo(
        "Finalizado",
        f"{PACKS[nome_pack]['title']} concluído!",
        parent=app,
    )


def set_install_controls(state):
    install_button.configure(state=state)
    select_all_button.configure(state=state)
    btn_gamer.configure(state=state)
    btn_home.configure(state=state)
    theme_button.configure(state=state)


# ============================================================
# REDIMENSIONAMENTO
# ============================================================

_last_layout = None


def on_resize(event):
    global _last_layout

    if event.widget != app:
        return

    largura = event.width

    # Muda para 1 coluna em janelas menores.
    novo_layout = "2col" if largura >= 980 else "1col"

    if novo_layout != _last_layout and not installing:
        _last_layout = novo_layout
        montar_cards(current_pack)


app.bind("<Configure>", on_resize)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

atualizar_cores()
trocar_pack("Gamer")

app.mainloop()