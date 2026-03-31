import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.title("Hospital Referral Network Model")

# Overview
st.header("Overview")
st.write("""
This project demonstrates a Hospital Referral Network using Graph Theory.
Each doctor is represented as a node, and referrals between doctors are edges.
It helps analyze patient referral patterns between doctors.
Centrality measures identify important doctors and referral hubs.
This model improves decision-making and patient flow in hospitals.
""")

# Store data
if "edges" not in st.session_state:
    st.session_state.edges = []

# Input
doc1 = st.text_input("Enter Doctor 1")
doc2 = st.text_input("Enter Doctor 2")

# Example Data
if st.button("Load Example Data"):
    st.session_state.edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("A", "D"),
        ("D", "E")
    ]
    st.success("Example data loaded!")

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

# Reset
if st.button("Reset"):
    st.session_state.edges = []

# Graph
G = nx.Graph()
G.add_edges_from(st.session_state.edges)

if st.session_state.edges:
    df = pd.DataFrame(st.session_state.edges, columns=["Doctor 1", "Doctor 2"])
    
    st.subheader("Referral Data")
    st.table(df)

    # Graph
    st.subheader("Referral Network Graph")
    st.write("""
    This graph shows referral relationships between doctors.
    Each node represents a doctor and each edge shows a referral.
    Doctors with more connections are more important.
    """)

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, ax=ax)
    st.pyplot(fig)

    # Centrality
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    data = pd.DataFrame({
        "Doctor": list(degree.keys()),
        "Degree": list(degree.values()),
        "Betweenness": list(betweenness.values()),
        "Closeness": list(closeness.values())
    })

    st.subheader("Centrality Analysis")
    st.table(data)

    # 🔹 Degree Centrality Graph
    st.subheader("Degree Centrality Graph")
    fig1, ax1 = plt.subplots()
    ax1.bar(data["Doctor"], data["Degree"])
    ax1.set_title("Degree Centrality")
    st.pyplot(fig1)

    st.write("""
    Degree centrality shows how many direct connections each doctor has.
    Higher value means the doctor is directly connected to more doctors.
    """)

    # 🔹 Betweenness Centrality Graph
    st.subheader("Betweenness Centrality Graph")
    fig2, ax2 = plt.subplots()
    ax2.bar(data["Doctor"], data["Betweenness"])
    ax2.set_title("Betweenness Centrality")
    st.pyplot(fig2)

    st.write("""
    Betweenness centrality shows which doctor acts as a bridge.
    Doctors with higher value connect different parts of the network.
    """)

    # 🔹 Closeness Centrality Graph
    st.subheader("Closeness Centrality Graph")
    fig3, ax3 = plt.subplots()
    ax3.bar(data["Doctor"], data["Closeness"])
    ax