import streamlit as st
import pickle
import pandas as pd
# LOAD MODEL + DATASET
model = pickle.load(open('model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))
df = pd.read_csv("data.csv", encoding="latin1")

# PAGE SETTINGS
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="",
    layout="wide"
)
# TITLE
st.title("💻 Laptop Price Predictor")
st.write("Predict laptop prices using Machine Learning")
# FIRST ROW
col1, col2, col3 = st.columns(3)
# BRAND
with col1:
    brand = st.selectbox(
        "Brand",
        [
            "HP",
            "Dell",
            "Lenovo",
            "Asus",
            "Acer",
            "Apple",
            "MSI",
            "Samsung"
        ]
    )
# CPU BRAND
with col2:
    cpu_brand = st.selectbox(
        "CPU Brand",
        [
            "Intel",
            "AMD",
            "Apple (M Series)"
        ]
    )
# RAM
with col3:

    ram_option = st.selectbox(
        "RAM",
        [
            "4 GB",
            "8 GB",
            "16 GB",
            "32 GB",
            "64 GB"
        ]
    )
ram = int(ram_option.split()[0])
# SECOND ROW
col4, col5, col6 = st.columns(3)
# GPU BRAND
with col4:
    gpu_brand = st.selectbox(
        "GPU Brand",
        [
            "Integrated",
            "NVIDIA",
            "AMD Radeon"
        ]
    )
# OPERATING SYSTEM
with col5:

    os = st.selectbox(
        "Operating System",
        [
            "Windows 10",
            "Windows 11",
            "Linux",
            "macOS"
        ]
    )
# STORAGE
with col6:
    storage_option = st.selectbox(
        "Storage",
        [
            "128 GB",
            "256 GB",
            "512 GB",
            "1 TB",
            "2 TB"
        ]
    )
# STORAGE CONVERSION
storage_map = {
    "128 GB": 128,
    "256 GB": 256,
    "512 GB": 512,
    "1 TB": 1024,
    "2 TB": 2048

}
storage = storage_map[storage_option]
# THIRD ROW
col7, col8, col9 = st.columns(3)
# DISPLAY SIZE
with col7:
    display_option = st.selectbox(
        "Display Size",
        [
            "13.3 inch",
            "14 inch",
            "15.6 inch",
            "16 inch",
            "17.3 inch"
        ]
    )

display_size = float(display_option.split()[0])
# SCREEN RESOLUTION
with col8:
    resolution = st.selectbox(
        "Screen Resolution",
        [
            "1366x768 (720p)",
            "1920x1080 (1080p)",
            "2560x1440 (2K)",
            "3840x2160 (4K)"
        ]
    )
# GAMING
with col9:
    gaming_option = st.selectbox(
        "Gaming Laptop?",
        [
            "No",
            "Yes"
        ]
    )
gaming = 1 if gaming_option == "Yes" else 0
# RESOLUTION CONVERSION
if resolution == "1366x768 (720p)":
    res_w = 1366
    res_h = 768
elif resolution == "1920x1080 (1080p)":
    res_w = 1920
    res_h = 1080
elif resolution == "2560x1440 (2K)":
    res_w = 2560
    res_h = 1440
else:
    res_w = 3840
    res_h = 2160
# PERFORMANCE SCORE
spec_rating = st.slider(
    "Performance Score",
    min_value=30,
    max_value=100,
    value=60,
    step=1
)
# PERFORMANCE LEVEL
if spec_rating < 50:
    spec_level = "Low"
elif spec_rating < 70:
    spec_level = "Medium"
else:
    spec_level = "High"
st.write(f"Performance Level: **{spec_level}**")
# CONFIGURATION PREVIEW
st.subheader("📋 Selected Configuration")
st.write(f"Brand: {brand}")
st.write(f"CPU Brand: {cpu_brand}")
st.write(f"GPU Brand: {gpu_brand}")
st.write(f"RAM: {ram} GB")
st.write(f"Storage: {storage} GB")
st.write(f"Display Size: {display_size} inch")
st.write(f"Resolution: {resolution}")
st.write(f"Gaming Laptop: {gaming_option}")
st.write(f"Operating System: {os}")
st.write(f"Performance Level: {spec_level}")
# CREATE INPUT DICTIONARY
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
# CREATE DATAFRAME
input_df = pd.DataFrame([input_dict])
# ONE HOT ENCODING
input_df = pd.get_dummies(input_df)
# MATCH TRAINING COLUMNS
input_df = input_df.reindex(
    columns=columns,
    fill_value=0
)
# PREDICT BUTTON
if st.button("Predict Price"):
    # PREDICTION
    prediction = model.predict(input_df)
    predicted_price = int(prediction[0])
    # SHOW PREDICTED PRICE
    st.success(
        f"Estimated Price: ₹{predicted_price:,}"
    )
    # PRICE RANGE
    lower_price = predicted_price - 10000
    upper_price = predicted_price + 10000
    st.info(
        f"Expected Price Range: ₹{lower_price:,} - ₹{upper_price:,}"
    )
    # FIND SIMILAR LAPTOPS
    filtered = df[
        (df['RAM'] == ram) &
        (df['storage'] == storage)
    ]
    # RELAX FILTER
    if filtered.empty:
        filtered = df[
            (df['RAM'] == ram)
        ]
    # FINAL FALLBACK
    if filtered.empty:

        df['price_diff'] = abs(
            df['price_rs'] - predicted_price
        )
        filtered = df.sort_values(
            by='price_diff'
        )
    # SHOW RECOMMENDATIONS
    st.subheader("🔍 Recommended Laptops")
    for _, row in filtered.head(5).iterrows():
        gaming_value = row.get(
            'Gaming',
            row.get('gaming', 0)
        )
        st.markdown(f"""
        ###  {row['brand']} - {row['Name']}
        -  RAM: {row['RAM']} GB
        -  Storage: {row['storage']} GB
        -  Display Size: {row['display_size']} inch
        -  Gaming Laptop:
        {"Yes" if gaming_value == 1 else "No"}
        -  Price: ₹{row['price_rs']:,}
        ---
        """)
