import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.title("Hospital Referral Network Model")

# 1️⃣ Overview Section
st.header("Overview")
st.write("""
This project demonstrates a Hospital Referral Network using Graph Theory.
Each doctor is represented as a node, and referrals between doctors are shown as edges.
The model helps in analyzing how patients are referred within the network.
Using centrality measures, we can identify important doctors and referral hubs.
It also helps in improving patient flow and decision-making in hospitals.
""")

# Store referrals
if "edges" not in st.session_state:
    st.session_state.edges = []

# Input
doc1 = st.text_input("Enter Doctor 1")
doc2 = st.text_input("Enter Doctor 2")

# 2️⃣ Example Button
if st.button("Load Example Data"):
    st.session_state.edges = [
        ("Dr A", "Dr B"),
        ("Dr B", "Dr C"),
        ("Dr C", "Dr D"),
        ("Dr A", "Dr D"),
        ("Dr B", "Dr D")
    ]
    st.success("Example data loaded! Now scroll down to see results.")

# Add referral
if st.button("Add Referral"):
    if doc1 and doc2 and doc1 != doc2:
        edge = tuple(sorted((doc1, doc2)))
        if edge not in st.session_state.edges:
            st.session_state.edges.append(edge)
            st.success("Referral Added")
        else:
            st.warning("Already Exists")
    else:
        st.error("Invalid Input")

# Reset button
if st.button("Reset"):
    st.session_state.edges = []

# Create graph
G = nx.Graph()
G.add_edges_from(st.session_state.edges)

# Display table
if st.session_state.edges:
    df = pd.DataFrame(st.session_state.edges, columns=["Doctor 1", "Doctor 2"])
    st.subheader("Referral Data")
    st.table(df)

    # 3️⃣ Graph Section + Explanation
    st.subheader("Referral Network Graph")
    st.write("""
    This graph represents the referral relationships between doctors.
    Each node represents a doctor, and each connection (edge) shows a referral between them.
    Doctors with more connections are more important in the network.
    The structure helps identify key doctors and referral patterns.
    """)

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", ax=ax)
    st.pyplot(fig)

    # Centrality
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    data = pd.DataFrame({
        "Doctor": list(degree.keys()),
        "Degree Centrality": list(degree.values()),
        "Betweenness Centrality": list(betweenness.values()),
        "Closeness Centrality": list(closeness.values())
    })

    st.subheader("Centrality Analysis")
    st.table(data)