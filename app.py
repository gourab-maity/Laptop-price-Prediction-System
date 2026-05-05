import streamlit as st
import pickle
import pandas as pd

# ---------- LOAD FILES ----------
model = pickle.load(open('model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))
df = pd.read_csv("data.csv", encoding="latin1")

# ---------- TITLE ----------
st.title("Laptop Price Prediction System")

# ---------- USER INPUTS ----------

# RAM
ram_option = st.selectbox(
    "RAM",
    ["4 GB", "8 GB", "16 GB", "32 GB", "64 GB"]
)
ram = int(ram_option.split()[0])

# Storage
storage_options = {
    "128 GB": 128,
    "256 GB": 256,
    "512 GB": 512,
    "1 TB": 1024,
    "2 TB": 2048
}
storage_option = st.selectbox("Storage", list(storage_options.keys()))
storage = storage_options[storage_option]

# Display size
display_option = st.selectbox(
    "Display Size",
    ["13.3 inch", "14 inch", "15.6 inch", "16 inch", "17.3 inch"]
)
display_size = float(display_option.split()[0])

# ---------- PERFORMANCE ----------
spec_rating = st.slider(
    "Performance Score (Spec Rating)",
    min_value=30,
    max_value=100,
    value=60,
    step=1
)

if spec_rating < 50:
    spec_level = "Low"
elif spec_rating < 70:
    spec_level = "Medium"
else:
    spec_level = "High"

st.write(f"Performance Level: **{spec_level}**")

# Gaming
gaming_option = st.selectbox("Gaming Laptop?", ["No", "Yes"])
gaming = 1 if gaming_option == "Yes" else 0

# Resolution
resolution_option = st.selectbox(
    "Screen Resolution",
    ["1366x768 (720p)", "1920x1080 (1080p)", "2560x1440 (1440p/2K)", "3840x2160 (4K)"]
)

if resolution_option == "1366x768 (720p)":
    res_w, res_h = 1366, 768
elif resolution_option == "1920x1080 (1080p)":
    res_w, res_h = 1920, 1080
elif resolution_option == "2560x1440 (1440p/2K)":
    res_w, res_h = 2560, 1440
else:
    res_w, res_h = 3840, 2160

# Brand
brand = st.selectbox("Brand", ["HP", "Dell", "Lenovo", "Asus", "Acer"])

# OS
os = st.selectbox("Operating System", ["Windows 10", "Windows 11", "Linux"])

# ---------- SHOW SELECTED CONFIG ----------
st.subheader("📋 Selected Configuration")

st.write(f"RAM: {ram} GB")
st.write(f"Storage: {storage} GB")
st.write(f"Display: {display_size} inch")
st.write(f"Resolution: {resolution_option}")
st.write(f"Performance: {spec_level} ({spec_rating})")
st.write(f"Gaming: {gaming_option}")
st.write(f"Brand: {brand}")
st.write(f"OS: {os}")

# ---------- CREATE INPUT ----------
input_dict = {
    'RAM': ram,
    'storage': storage,
    'display_size': display_size,
    'spec_rating': spec_rating,
    'Gaming': gaming,
    'resolution_width': res_w,
    'resolution_height': res_h,
    'brand': brand,
    'OS': os
}

input_df = pd.DataFrame([input_dict])

# ---------- ENCODING ----------
input_df = pd.get_dummies(input_df)
input_df = input_df.reindex(columns=columns, fill_value=0)

# ---------- PREDICTION ----------
if st.button("Predict Price"):

    # Loading animation
    with st.spinner("Predicting price..."):
        prediction = model.predict(input_df)

    predicted_price = int(prediction[0])

    # Main result
    st.success(f"Estimated Price: ₹{predicted_price:,}")

    # Price range
    low = int(predicted_price * 0.9)
    high = int(predicted_price * 1.1)
    st.info(f"Expected Price Range: ₹{low:,} - ₹{high:,}")

    # ---------- SIMILAR LAPTOPS ----------

    filtered = df[
        (df['RAM'] == ram) &
        (df['storage'] == storage)
    ]

    if filtered.empty:
        filtered = df[df['RAM'] == ram]

    if filtered.empty:
        df['price_diff'] = abs(df['price_rs'] - predicted_price)
        filtered = df.sort_values(by='price_diff')

    st.subheader("🔍 Similar Laptops:")

    for _, row in filtered.head(5).iterrows():
        st.write(f"💻 **{row['brand']} - {row['Name']}**")
        st.write(f"💰 Price: ₹{row['price_rs']:,}")
        st.write("---")
