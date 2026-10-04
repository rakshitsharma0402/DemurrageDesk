import pandas as pd
import streamlit as st

from demurrage import charge
from rag import ask, extract_rule, providers, retrieve

st.title("Port Terms Assistant")
st.caption("Answers come only from your documents, with sources. Check the source before acting on any charge.")

choice = st.sidebar.selectbox("Shipping line / terminal", ["All"] + providers())
provider = None if choice == "All" else choice

question = st.text_input("Ask about free time, rates, documents, procedures...")
if st.button("Ask") and question:
    with st.spinner("Searching your documents..."):
        chunks = retrieve(question, provider)
        ans, cites, bad = ask(question, chunks)
    st.session_state["result"] = {"q": question, "chunks": chunks, "ans": ans, "cites": cites, "bad": bad}

res = st.session_state.get("result")
if res:
    if res["ans"].found:
        st.write(res["ans"].answer)
    else:
        st.info(res["ans"].answer or "Not found in your documents.")
    for c in res["cites"]:
        with st.expander(f"{c.source}, page {c.page}"):
            st.markdown(f"> {c.quote}")
    if res["bad"]:
        with st.expander(f"Debug: {len(res['bad'])} quote(s) the model gave that were not found word-for-word in the sources"):
            for c in res["bad"]:
                st.code(c.quote, language=None)

    st.divider()
    st.subheader("Charge calculator")
    st.caption("The model reads the rule from the sources; plain code does the maths. Check the numbers against the source.")

    def do_extract():
        r = extract_rule(res["q"], res["chunks"])
        df = pd.DataFrame([t.model_dump() for t in r.tiers] or [{"from_day": 1, "to_day": None, "rate": 0.0}])
        df["to_day"] = df["to_day"].astype("Int64")
        st.session_state.update(free_days=r.free_days, tiers=df, rule_notes=r.notes)

    st.button("Read rule from these sources", on_click=do_extract)
    if "tiers" in st.session_state:
        if st.session_state.get("rule_notes"):
            st.caption(f"Notes: {st.session_state['rule_notes']}")
        free = st.number_input("Free days", min_value=0, key="free_days")
        edited = st.data_editor(st.session_state["tiers"], num_rows="dynamic", key="tier_editor")
        held = st.number_input("Days held", min_value=0, value=10)
        tiers = [{"from_day": int(r.from_day), "to_day": None if pd.isna(r.to_day) else int(r.to_day), "rate": float(r.rate)}
                 for r in edited.itertuples() if not pd.isna(r.from_day)]
        total, rows = charge(int(held), int(free), tiers)
        st.metric("Estimated charge", f"{total:,.2f}")
        if rows:
            st.table(pd.DataFrame(rows))