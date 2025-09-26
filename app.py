import streamlit as st
import hashlib
import datetime
import random
import pandas as pd

# -------------------------------
# Blockchain Ticketing Components
# -------------------------------

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # ticket info
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, str(datetime.datetime.now()), {"info": "Genesis Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        new_block = Block(len(self.chain), str(datetime.datetime.now()), data, self.get_latest_block().hash)
        self.chain.append(new_block)


# -------------------------------
# Streamlit UI
# -------------------------------

st.title("🎟 Blockchain-based Event Ticketing System")

# Initialize blockchain in session state
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

# Dropdown for event type
event_type = st.selectbox("Select Event", ["Sports", "Art", "Cultural", "Literature", "MUN"])

# Buyer name
buyer_name = st.text_input("Enter Buyer Name")

# Number of tickets
num_tickets = st.number_input("Number of Tickets", min_value=1, step=1)

# Issue tickets
if st.button("Issue New Ticket(s)"):
    if buyer_name.strip() == "":
        st.error("Please enter buyer name.")
    else:
        tickets = []
        timestamp = str(datetime.datetime.now())
        for _ in range(num_tickets):
            ticket_id = f"T{random.randint(100000, 999999)}"
            ticket_data = {
                "event": event_type,
                "buyer": buyer_name,
                "ticket_id": ticket_id,
                "time": timestamp
            }
            st.session_state.blockchain.add_block(ticket_data)
            tickets.append(ticket_data)

        st.success(f"{num_tickets} Ticket(s) successfully issued to {buyer_name} for {event_type} event.")
        st.json(tickets)

# -------------------------------
# Verify Ticket
# -------------------------------
st.subheader("🔍 Verify Ticket")
ticket_to_verify = st.text_input("Enter Ticket ID to Verify")

if st.button("Verify"):
    found = False
    for block in st.session_state.blockchain.chain:
        data = block.data
        if isinstance(data, dict) and data.get("ticket_id") == ticket_to_verify:
            st.success(f"✅ Ticket {ticket_to_verify} is VALID.")
            st.json(data)
            found = True
            break
    if not found:
        st.error("❌ Ticket not found or invalid.")

# -------------------------------
# Event Summary Table
# -------------------------------
st.subheader("📊 Event Summary")

records = []
for block in st.session_state.blockchain.chain[1:]:  # skip genesis
    data = block.data
    if isinstance(data, dict):
        records.append([data["event"], data["buyer"], data["ticket_id"], data["time"]])

if records:
    df = pd.DataFrame(records, columns=["Event Name", "Buyer Name", "Ticket ID", "Time of Purchase"])
    st.dataframe(df)
else:
    st.info("No tickets issued yet.")

# -------------------------------
# Full Blockchain Summary
# -------------------------------
st.subheader("⛓ Full Blockchain Ledger (All Blocks)")

block_records = []
for block in st.session_state.blockchain.chain:
    block_records.append([
        block.index,
        block.timestamp,
        block.data,
        block.previous_hash,
        block.hash
    ])

df_blocks = pd.DataFrame(block_records, columns=["Index", "Timestamp", "Data", "Previous Hash", "Hash"])
st.dataframe(df_blocks)
