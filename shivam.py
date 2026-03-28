import random
import streamlit as st
import matplotlib.pyplot as plt

st.title("🏦 Bank Queue Simulation")

# User Inputs
customers = st.number_input("Enter number of customers:", min_value=1, value=10)
tellers = st.number_input("Enter number of tellers:", min_value=1, value=2)

if st.button("Run Simulation"):

    arrival = []
    service = []
    waiting = []
    start = []
    end = []

    time = 0

    # Generate arrival times
    for i in range(customers):
        gap = random.randint(0, 2)
        time += gap
        arrival.append(time)

    # Generate service times
    for i in range(customers):
        service.append(random.randint(2, 6))

    # Teller free time tracker
    teller_time = [0] * tellers

    # Simulation
    for i in range(customers):

        free_teller = teller_time.index(min(teller_time))

        start_time = max(arrival[i], teller_time[free_teller])
        finish_time = start_time + service[i]

        start.append(start_time)
        end.append(finish_time)

        waiting.append(start_time - arrival[i])

        teller_time[free_teller] = finish_time

    # Average waiting time
    avg_wait = sum(waiting) / customers

    st.subheader(f"Average Waiting Time: {round(avg_wait, 2)}")

    # Plot graph
    fig, ax = plt.subplots()
    ax.plot(range(1, customers + 1), waiting, marker='o')
    ax.set_xlabel("Customer Number")
    ax.set_ylabel("Waiting Time")
    ax.set_title("Customer Waiting Time Graph")
    ax.grid(True)

    st.pyplot(fig)