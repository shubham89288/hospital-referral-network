import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.title("Hospital Referral Network Model")

# 1️⃣ Overview
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

# 2️⃣ Example Data Button
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

# Display
if st.session_state.edges:
    df = pd.DataFrame(st.session_state.edges, columns=["Doctor 1", "Doctor 2"])
    
    st.subheader("Referral Data")
    st.table(df)

    # 3️⃣ Graph + Explanation
    st.subheader("Referral Network Graph")
    st.write("""
    This graph shows referral relationships between doctors.
    Each node represents a doctor and each edge shows a referral.
    Doctors with more connections are more important.
    It helps identify key doctors and referral patterns.
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

    # 4️⃣ Bar Graph
    st.subheader("Centrality Bar Graph")

    fig2, ax2 = plt.subplots()
    data.set_index("Doctor")[[
        "Degree Centrality",
        "Betweenness Centrality",
        "Closeness Centrality"
    ]].plot(kind="bar", ax=ax2)

    ax2.set_ylabel("Centrality Value")
    ax2.set_title("Doctor Importance Comparison")

    st.pyplot(fig2)

    # 5️⃣ Bar Graph Explanation
    st.write("""
    This bar graph compares centrality values of doctors.
    Degree centrality shows number of direct connections.
    Betweenness centrality shows bridge doctors.
    Closeness centrality shows how quickly a doctor connects to others.
    Higher values indicate more important doctors.
    """)
