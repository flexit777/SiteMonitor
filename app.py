import streamlit as st

st.set_page_config(page_title="Ticket Monitor", page_icon="🎫")
st.title("🎫 Movie Ticket Monitor")

# Display the last time the bot ran
try:
    with open("last_check.txt", "r") as f:
        status_time = f.read()
    st.success(f"Last Bot Check: {status_time} (IST)")
except:
    st.info("Waiting for the first background check to finish...")

st.write("Monitoring: [Miraj Wadala - March 19](https://in.bookmyshow.com/cinemas/mumbai/miraj-cinemas-imax-wadala/buytickets/MCIW/20260319)")
st.caption("Trigger word: 'dhurandhar'")
