import streamlit as st
from datetime import date
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="Scouting Rapports", layout="centered")

# Ajout dans la sidebar pour choisir la version
version = st.sidebar.radio("Choisir la version", options=["PC", "Mobile"])

st.title("📝 Rapport de Scouting Football")

# --- Infos joueur & observation ---
with st.expander("Infos joueur & observation", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        age = st.number_input("Âge", min_value=5, max_value=60, step=1)
        categorie = st.selectbox("Catégorie", ["U12", "U13", "U14", "U15", "U16", "U17", "U18", "U19", "Senior"])
        club = st.text_input("Club")
    with col2:
        date_obs = st.date_input("Date de l'observation", value=date.today())
        observateur = st.text_input("Nom de l'observateur")
        nb_fois = st.number_input("Nombre de fois observé", min_value=1, max_value=50, step=1)
        adversaire = st.text_input("Adversaire")
        lieu = st.selectbox("Lieu", ["Domicile", "Extérieur"])
        competition = st.text_input("Compétition")

# --- Poste observé ---
poste = st.selectbox(
    "Poste observé",
    options=["Gardien", "Défenseur", "Milieu", "Attaquant"],
    index=1,
)

criteres_par_poste = {
    "Gardien": {
        "Offensif": ["Lancements longs", "Relances", "Jeu au pied"],
        "Défensif": ["Arrêts", "Sorties aériennes", "Anticipation", "Communication", "Positionnement"]
    },
    "Défenseur": {
        "Offensif": ["Montées", "Passes clés", "Centres", "Jeu au pied"],
        "Défensif": ["Tacles", "Interceptions", "Marquage", "Duels aériens", "Positionnement"]
    },
    "Milieu": {
        "Offensif": ["Passes décisives", "Progressions balle au pied", "Création d'espaces", "Tirs"],
        "Défensif": ["Pressing", "Récupérations", "Marquage", "Repli défensif"]
    },
    "Attaquant": {
        "Offensif": ["Finition", "Dribbles", "Appels", "Jeu dos au but"],
        "Défensif": ["Pressing haut", "Repli", "Conservation balle"]
    }
}

criteres_off = criteres_par_poste[poste]["Offensif"]
criteres_def = criteres_par_poste[poste]["Défensif"]

# --- Notes et commentaires ---
st.header(f"📝 Critères Offensifs et Défensifs pour {poste}")

# Ajuster l'affichage en fonction de la version choisie
if version == "PC":
    cols_off = st.columns(2)
    container_off = cols_off[0]
    container_def = cols_off[1]
else:  # version Mobile : on empile verticalement
    container_off = st.container()
    container_def = st.container()

notes_off = {}
comms_off = {}
notes_def = {}
comms_def = {}

with container_off:
    st.subheader("Offensif")
    for i, crit in enumerate(criteres_off):
        crit_mod = st.text_input(f"Critère Offensif #{i+1}", value=crit, key=f"off_crit_{i}")
        notes_off[crit_mod] = st.slider(f"Note - {crit_mod}", 0, 10, 5, key=f"off_note_{i}")
        comms_off[crit_mod] = st.text_area(f"Commentaire - {crit_mod}", height=80, key=f"off_comm_{i}")

with container_def:
    st.subheader("Défensif")
    for i, crit in enumerate(criteres_def):
        crit_mod = st.text_input(f"Critère Défensif #{i+1}", value=crit, key=f"def_crit_{i}")
        notes_def[crit_mod] = st.slider(f"Note - {crit_mod}", 0, 10, 5, key=f"def_note_{i}")
        comms_def[crit_mod] = st.text_area(f"Commentaire - {crit_mod}", height=80, key=f"def_comm_{i}")

# Commentaire général
commentaire_general = st.text_area("Commentaire général", height=100)

def create_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Titre principal
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 60, 90)
    pdf.cell(0, 15, "Rapport de Scouting Football", ln=True, align="C")
    pdf.ln(4)

    # Infos générales encadrées
    pdf.set_fill_color(230, 240, 250)
    pdf.set_draw_color(30, 60, 90)
    pdf.set_line_width(0.7)
    pdf.rect(10, pdf.get_y(), 190, 60, style="DF")
    pdf.set_xy(15, pdf.get_y() + 3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 60, 90)
    pdf.cell(0, 8, "Informations générales", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    infos = [
        f"Nom complet : {prenom} {nom}",
        f"Âge : {age} ans",
        f"Catégorie : {categorie}",
        f"Club : {club}",
        f"Date observation : {date_obs.strftime('%d/%m/%Y')}",
        f"Observateur : {observateur}",
        f"Nombre fois observé : {nb_fois}",
        f"Adversaire : {adversaire}",
        f"Lieu : {lieu}",
        f"Compétition : {competition}",
        f"Poste observé : {poste}"
    ]
    for i, info in enumerate(infos):
        pdf.set_xy(15, pdf.get_y() + 7)
        pdf.cell(0, 7, info, ln=True)

    pdf.ln(8)

    # Tableau Offensif & Défensif
    pdf.set_fill_color(200, 220, 240)
    pdf.set_text_color(10, 40, 80)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(95, 10, "Critères Offensifs", border=1, align="C", fill=True)
    pdf.cell(95, 10, "Critères Défensifs", border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)

    max_len = max(len(notes_off), len(notes_def))
    for i in range(max_len):
        # Offensif
        if i < len(notes_off):
            crit_off = list(notes_off.keys())[i]
            note_off = notes_off[crit_off]
            comm_off = comms_off.get(crit_off, "").replace('\n', ' ')
            comm_off = (comm_off[:45] + "...") if len(comm_off) > 45 else comm_off
            pdf.cell(40, 8, crit_off, border=1)
            pdf.cell(15, 8, str(note_off), border=1, align="C")
            pdf.cell(40, 8, comm_off, border=1)
        else:
            pdf.cell(95, 8, "", border=1)

        # Défensif
        if i < len(notes_def):
            crit_def = list(notes_def.keys())[i]
            note_def = notes_def[crit_def]
            comm_def = comms_def.get(crit_def, "").replace('\n', ' ')
            comm_def = (comm_def[:45] + "...") if len(comm_def) > 45 else comm_def
            pdf.cell(40, 8, crit_def, border=1)
            pdf.cell(15, 8, str(note_def), border=1, align="C")
            pdf.cell(40, 8, comm_def, border=1)
        else:
            pdf.cell(95, 8, "", border=1)
        pdf.ln()

    pdf.ln(5)

    # Note moyenne & commentaire général dans cadre
    all_notes = list(notes_off.values()) + list(notes_def.values())
    moyenne = round(sum(all_notes) / len(all_notes), 2) if all_notes else 0

    pdf.set_fill_color(230, 240, 250)
    pdf.set_draw_color(30, 60, 90)
    pdf.set_line_width(0.7)
    y_start = pdf.get_y()
    pdf.rect(10, y_start, 190, 30, style="DF")

    pdf.set_xy(15, y_start + 5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 60, 90)
    pdf.cell(0, 8, f"Note moyenne : {moyenne} / 10", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    cg = commentaire_general.strip()
    pdf.set_xy(15, y_start + 15)
    if cg:
        pdf.multi_cell(0, 7, f"Commentaire général : {cg}")
    else:
        pdf.cell(0, 8, "Commentaire général : -", ln=True)

    return pdf

if st.button("📄 Générer le rapport PDF"):
    pdf = create_pdf()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        st.success("Rapport généré avec succès !")
        with open(tmp_file.name, "rb") as f:
            st.download_button("⬇️ Télécharger le rapport PDF", data=f, file_name="rapport_scouting.pdf", mime="application/pdf")
