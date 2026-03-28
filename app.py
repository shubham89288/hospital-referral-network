import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.title("Hospital Referral Network Model")

# Store referrals
if "edges" not in st.session_state:
    st.session_state.edges = []

# Input
doc1 = st.text_input("Enter Doctor 1")
doc2 = st.text_input("Enter Doctor 2")

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
# Display table
# If data exists
if st.session_state.edges:

    # ✅ TABLE
    df = pd.DataFrame(st.session_state.edges, columns=["Doctor 1", "Doctor 2"])
    st.subheader("Referral Data")
    st.table(df)

    # ✅ GRAPH (IMPORTANT - DON'T REMOVE)
    G = nx.Graph()
    G.add_edges_from(st.session_state.edges)

    st.subheader("Referral Network Graph")
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", ax=ax)
    st.pyplot(fig)

    # ✅ CENTRALITY
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    data = pd.DataFrame({
        "Doctor": list(degree.keys()),
        "Degree Centrality": list(degree.values()),
        "Betweenness Centrality": list(betweenness.values()),
        "Closeness Centrality": list(closeness.values())
    })

    # ✅ TABLE
    st.subheader("Centrality Analysis")
    st.table(data)

    # ✅ BAR GRAPHS
    st.subheader("Centrality Bar Graph")

    st.write("Degree Centrality")
    st.bar_chart(data.set_index("Doctor")["Degree Centrality"])

    st.write("Betweenness Centrality")
    st.bar_chart(data.set_index("Doctor")["Betweenness Centrality"])

    st.write("Closeness Centrality")
    st.bar_chart(data.set_index("Doctor")["Closeness Centrality"])