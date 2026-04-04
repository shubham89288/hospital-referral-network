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
It helps analyze how patients move between doctors in a hospital system.
Using graph analysis, we can identify key doctors and referral patterns.
Centrality measures help in understanding doctor importance.
This improves hospital efficiency and patient flow.
""")

# Store data
if "edges" not in st.session_state:
    st.session_state.edges = []

# Input
doc1 = st.text_input("Enter Doctor 1")
doc2 = st.text_input("Enter Doctor 2")

# Example
if st.button("Load Example Data"):
    st.session_state.edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("A", "D"),
        ("D", "E")
    ]
    st.success("Example data loaded!")

# Add
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

    # Network Graph
    st.subheader("Referral Network Graph")
    st.write("""
    This graph shows referral relationships between doctors.
    Each node represents a doctor and each edge shows a referral.
    Highly connected doctors play important roles in the network.
    This helps identify referral hubs and important connections.
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

    # 🔥 TOP DOCTORS
    st.subheader("Top Doctors")
    top_degree = max(degree, key=degree.get)
    top_between = max(betweenness, key=betweenness.get)
    top_close = max(closeness, key=closeness.get)

    st.write(f"Top Doctor (Degree Centrality): {top_degree}")
    st.write(f"Top Doctor (Betweenness Centrality): {top_between}")
    st.write(f"Top Doctor (Closeness Centrality): {top_close}")

    # 🔹 Degree Graph
    st.subheader("Degree Centrality Graph")
    fig1, ax1 = plt.subplots()
    ax1.bar(data["Doctor"], data["Degree"])
    ax1.set_title("Degree Centrality")
    st.pyplot(fig1)

    st.write("""
    Degree centrality measures the number of direct connections a doctor has.
    A higher value means the doctor is connected to many other doctors.
    These doctors are important for direct referrals in the network.
    They act as active participants in patient transfer.
    High degree centrality indicates popularity in the network.
    It helps in identifying major referral hubs.
    These doctors can influence patient flow significantly.
    """)

    # 🔹 Betweenness Graph
    st.subheader("Betweenness Centrality Graph")
    fig2, ax2 = plt.subplots()
    ax2.bar(data["Doctor"], data["Betweenness"])
    ax2.set_title("Betweenness Centrality")
    st.pyplot(fig2)

    st.write("""
    Betweenness centrality shows how often a doctor lies on shortest paths.
    Doctors with high values act as bridges between different groups.
    They help connect separate parts of the network.
    These doctors control the flow of information or patients.
    Removing them can break the network structure.
    They are critical for maintaining connectivity.
    They play a strategic role in referrals.
    """)

    # 🔹 Closeness Graph (FIXED)
    st.subheader("Closeness Centrality Graph")
    fig3, ax3 = plt.subplots()
    ax3.bar(data["Doctor"], data["Closeness"])
    ax3.set_title("Closeness Centrality")
    st.pyplot(fig3)   # ✅ FIX HERE

    st.write("""
    Closeness centrality measures how close a doctor is to all others.
    Doctors with high values can quickly reach other doctors.
    It indicates efficiency in communication and referrals.
    These doctors reduce the number of steps in patient transfer.
    They are important for fast decision-making.
    High closeness means better network accessibility.
    It helps identify well-positioned doctors in the network.
    """)
