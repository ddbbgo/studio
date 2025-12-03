import streamlit as st
import datetime
import pandas as pd

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="Studio Manager", layout="centered")

# --- PASSWORD DI PROTEZIONE ---
password_segreta = "studio2024"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if st.session_state.password_correct:
        return True
    st.markdown("### 🔒 Accesso Riservato Staff")
    pwd = st.text_input("Inserisci Password:", type="password")
    if st.button("Accedi"):
        if pwd == password_segreta:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Password errata")
    return False

if not check_password():
    st.stop()

# --- MEMORIA TEMPORANEA ---
if "pazienti" not in st.session_state:
    st.session_state.pazienti = []

# --- LISTINO PREZZI BASE ---
TRATTAMENTI = {
    "Vacuum Therapy (20 min)": 80.0,
    "Radiofrequenza Viso": 120.0,
    "Linfodrenaggio Manuale": 70.0,
    "Laser Epilazione (Gambe)": 150.0,
    "Pacchetto Dimagrimento Urto": 90.0,
    "Pulizia Viso Profonda": 60.0
}

# --- MENU DI NAVIGAZIONE (Più visibile dei TAB) ---
st.markdown("### 🏥 Studio Medico & Estetico")
menu = st.radio("Cosa vuoi fare?", ["📝 NUOVA VENDITA", "📂 VEDI ARCHIVIO"], horizontal=True)
st.divider()

# --- SEZIONE 1: VENDITA ---
if menu == "📝 NUOVA VENDITA":
    
    # 1. DATI PAZIENTE
    st.caption("1️⃣ ANAGRAFICA")
    col1, col2 = st.columns(2)
    with col1:
        nome_paziente = st.text_input("Nome Paziente")
    with col2:
        trattamento_oggi = st.text_input("Fatto oggi (da pagare)", placeholder="Es. Igiene Viso")

    st.markdown("---")
    
    # 2. CONFIGURAZIONE PROTOCOLLO
    st.caption("2️⃣ COSTRUZIONE PROTOCOLLO")
    
    trattamento_prop = st.selectbox("Trattamento Proposto:", list(TRATTAMENTI.keys()))
    prezzo_unitario = TRATTAMENTI[trattamento_prop]
    
    # QUI LA LOGICA CAMBIA: Ideale vs Reale
    col_sed1, col_sed2 = st.columns(2)
    with col_sed1:
        n_ideali = st.number_input("Sedute IDEALI (per risultato Top):", min_value=1, value=8)
    with col_sed2:
        n_proposte = st.number_input("Sedute PROPOSTE (nel pacchetto):", min_value=1, value=6)

    # Logica Efficacia
    efficacia = min(int((n_proposte / n_ideali) * 100), 100)
    
    if efficacia < 100:
        st.progress(efficacia)
        st.warning(f"⚠️ Stai proponendo {n_proposte} sedute su {n_ideali}. Risultato parziale.")
    else:
        st.progress(efficacia)
        st.success("✅ Protocollo Completo (100% Efficacia).")

    st.markdown("---")

    # 3. PREZZI E SCONTO (EURO)
    st.caption("3️⃣ PROPOSTA ECONOMICA")
    
    prezzo_listino = prezzo_unitario * n_proposte
    
    # Checkbox per attivare lo sconto
    attiva_sconto = st.checkbox("Applica Sconto (Importo Fisso)")
    
    if attiva_sconto:
        # SE C'È LO SCONTO: Mostra prezzo barrato e input sconto in euro
        sconto_euro = st.number_input("Sconto in Euro (€):", min_value=0.0, value=50.0, step=10.0)
        prezzo_finale = prezzo_listino - sconto_euro
        
        st.write(f"Prezzo di Listino: <strike style='color:red'>€ {prezzo_listino:.2f}</strike>", unsafe_allow_html=True)
        st.markdown(f"# € {prezzo_finale:.2f}")
        st.success(f"🎉 Risparmi € {sconto_euro:.2f}")
    
    else:
        # SE NON C'È LO SCONTO: Mostra solo il prezzo normale
        prezzo_finale = prezzo_listino
        st.markdown(f"# € {prezzo_listino:.2f}")

    # 4. SALVATAGGIO
    st.markdown("---")
    if st.button("💾 REGISTRA E COPIA PER RECEPTION", type="primary"):
        if nome_paziente:
            # Salvataggio in memoria
            nuova_scheda = {
                "Ora": datetime.datetime.now().strftime("%H:%M"),
                "Paziente": nome_paziente,
                "Fatto Oggi": trattamento_oggi,
                "Pacchetto": f"{n_proposte}x {trattamento_prop}",
                "Totale": f"€ {prezzo_finale:.2f}",
            }
            st.session_state.pazienti.append(nuova_scheda)
            st.toast("Salvato con successo!", icon="✅")
            
            # Generazione Messaggio WhatsApp
            testo_wa = f"""
            *CLIENTE IN USCITA*
            👤 {nome_paziente}
            🛠 Fatto oggi: {trattamento_oggi}
            📦 PACCHETTO: {n_proposte}x {trattamento_prop}
            💰 DA INCASSARE: € {prezzo_finale:.2f}
            """
            st.code(testo_wa, language="markdown")
            st.caption("Copia il testo qui sopra e invialo alla Reception")
        else:
            st.error("Inserisci il nome del paziente!")

# --- SEZIONE 2: ARCHIVIO ---
elif menu == "📂 VEDI ARCHIVIO":
    st.markdown("#### 📂 Pazienti inseriti oggi")
    
    if len(st.session_state.pazienti) > 0:
        df = pd.DataFrame(st.session_state.pazienti)
        st.dataframe(df, use_container_width=True)
        st.info("Ricorda: se chiudi la pagina web, questa lista si azzera.")
    else:
        st.warning("Nessun paziente ancora registrato.")
TRATTAMENTI = {
    "Vacuum Therapy (20 min)": 80.0,
    "Radiofrequenza Viso": 120.0,
    "Linfodrenaggio Manuale": 70.0,
    "Laser Epilazione (Gambe)": 150.0,
    "Pacchetto Dimagrimento Urto": 90.0
}

def main():
    # Intestazione carina per cellulare
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966334.png", width=50) # Icona generica
    st.markdown("### 💎 Protocol Builder")
    st.caption("Configuratore Offerta per Paziente")
    
    st.divider()
    
    # 1. INPUT DATI
    st.write("📋 **Configurazione**")
    trattamento = st.selectbox("Trattamento:", list(TRATTAMENTI.keys()))
    prezzo_unitario = TRATTAMENTI[trattamento]
    
    n_sedute = st.number_input("Numero Sedute:", min_value=1, value=6, step=1)

    # Logica Barra Efficacia
    ciclo_ideale = 6
    efficacia = min(int((n_sedute / ciclo_ideale) * 100), 100)
    
    if efficacia < 80:
        st.progress(efficacia)
        st.warning("⚠️ Risultato parziale (Ciclo incompleto)")
    else:
        st.progress(efficacia)
        st.success("✅ Risultato ottimale garantito")

    st.divider()

    # 2. PREZZO E SCONTO
    prezzo_totale_listino = prezzo_unitario * n_sedute
    
    st.write("💰 **Proposta Economica**")
    st.caption(f"Listino: {n_sedute} sedute x €{prezzo_unitario}")
    
    # Prezzo Barrato Visivo
    st.markdown(f"### <strike style='color:red'>€ {prezzo_totale_listino:.2f}</strike>", unsafe_allow_html=True)
    
    # Checkbox per attivare la modalità "Chiusura Vendita"
    applica_sconto = st.checkbox("Applica Sconto 'Solo Oggi'")
    
    if applica_sconto:
        perc_sconto = st.slider("Sconto (%)", 5, 30, 15)
        
        risparmio = prezzo_totale_listino * (perc_sconto / 100)
        prezzo_finale = prezzo_totale_listino - risparmio
        
        st.markdown("---")
        st.metric(label="PREZZO BLOCCATO", value=f"€ {prezzo_finale:.2f}", delta=f"Risparmi € {risparmio:.2f}")
        
        st.warning(f"🔥 Offerta valida solo oggi: {datetime.date.today().strftime('%d/%m')}")
        
        if st.button("CONFIRMA E BLOCCA PREZZO", use_container_width=True):
            st.balloons()
            st.success("✅ Offerta salvata! Procedere in reception.")
            st.caption("Fai uno screenshot di questa schermata per la reception.")

if __name__ == "__main__":
    main()
