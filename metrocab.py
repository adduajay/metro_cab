import qrcode
from gtts import gTTS
import streamlit as st
from io import BytesIO
import uuid
from PIL import Image
import base64

#QR GENERATION FUNCTION

def generate_qr(data):
    qr = qrcode.QRCode(version = 1,box_size = 10,border = 4)
    qr.add_data(data)
    qr.make(fit = True)
    img = qr.make_image(fill_color= "black",back_color = "white")
    return img

#STREAMLIT UI

st.set_page_config(page_title="Metro Ticket Booking", page_icon="")
st.title (" Metro Ticket Booking System with QR Code + Auto Voice")
stations = ["Ameerpet", "Miyapur", "LB Nagar", "KPHB", "JNTU"]
name = st.text_input ("Passenger Name")
source = st. selectbox("Source Station", stations)
destination = st. selectbox("Destination Station", stations)
no_tickets = st.number_input("Number of Tickets", min_value=1, value=1)
ch=st.radio("Cab:",["Yes","No"])
price_per_ticket = 30
total_amount = no_tickets * price_per_ticket

if(ch=="Yes"):
            des=st.text_input("Enter Drop location:")
            price=60
            total_amount+=price
st.info(f" Total Amount: {total_amount}")
# BOOKING BUTTON
if st.button ("Book Ticket"):
    if name.strip() == "":
        st.error("Please enter passenger name.")
    elif source == destination :
        st.error("Source and Destinatiion cannot be same.")
    else :
        booking_id = str(uuid.uuid4())[:8]
        #CAB
        if(ch=="Yes"):
            qr_data = (
                f"BookingID : {booking_id}\n"
                f"Name : {name}\n From : {source}\n To : {destination}\nTickets : {no_tickets}\n"
                f"Drop Location : {des}\n Total Price : {total_amount}"
                )
        else:
            qr_data = (
                f"BookingID : {booking_id}\n"
                f"Name : {name}\n From : {source}\n To : {destination}\nTickets : {no_tickets}"
                )

        qr_img = generate_qr(qr_data)

        buf = BytesIO()
        qr_img.save(buf,format = "PNG")
        qr_bytes = buf.getvalue()
        voice_text = f"Ticket booked successfully. {name}, your journey from {source} to {destination},Total amount {total_amount} rupees."
        tts = gTTS(voice_text)
        audio_buf = BytesIO()
        tts.write_to_fp(audio_buf)
        audio_buf.seek(0)

        st.success("Ticket Booked Successfully!")
        st.write(f"Ticket Details")
        st.write(f"Booking ID : {booking_id}")
        st.write(f"Passenger : {name}")
        st.write(f"From : {source}")
        st.write(f"To : {destination}")
        st.write(f"Tickets : {no_tickets}")
        try:
            st.write(f"Drop Location : {des}")
        except:
            pass
        st.write(f"Amount : {total_amount}")
        st.image(qr_bytes,width = 250)
        st.audio(audio_buf, format="audio/mp3")
