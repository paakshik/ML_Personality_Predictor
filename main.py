import streamlit as st
import pickle
import pandas as pd

# --- STEP 1: LOAD ASSETS ---
# We load the model AND the scaler.
def load_assets():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    return model, scaler


model, scaler = load_assets()

# --- STEP 2: UI HEADER  FOR THE APP---
st.set_page_config(page_title="Student Grade Predictor", page_icon="🎓")
st.title("🎓 AI Student Success Predictor")
st.markdown("""
This app uses a **Linear Regression** model to predict a student's final performance.
It analyzes engagement levels, test scores, and historical data to provide early warnings.
""")

# --- STEP 3: USER INPUTS ---
# We use sliders and number inputs.
st.sidebar.header("Student Parameters")

# Feature 1: Engagement
engagement = st.sidebar.slider("Engagement Level (1-10)", 1, 10, 0)


# Feature 3: Error Rate
error_rate = st.sidebar.slider("Error Rate (%)", 0, 100,0)

# Feature 4: Previous Grade (G1)
test_avg_score = st.sidebar.number_input("Test Average Score", 0, 100, 15)

# --- STEP 4: PREDICTION LOGIC ---
if st.button("Generate Prediction"):

    input_data = pd.DataFrame({
        'Engagement_Level': [engagement],
        'Test_Avg_Score': [test_avg_score],
        'Error_Rate': [error_rate/100]

    })

    st.write("📊 Input Features:")
    st.dataframe(input_data,hide_index=True)

    # 2. Scale the input using the saved scaler
    # This is ESSENTIAL because model was trained on scaled data
    scaled_input = scaler.transform(input_data)

    st.write("🔧 Scaled Features:")
    st.write(scaled_input)

    # 3. Make prediction
    prediction = model.predict(scaled_input)[0]

    # 4. Ensure prediction is within valid range (0-100)
    final_grade = max(0, min(100, prediction))

    # --- STEP 5: DISPLAY RESULTS ---
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Predicted Final Grade", value=f"{final_grade:.2f}%")

    with col2:
        if final_grade >= 85:
            st.success("Status: Excellent")
        elif final_grade >= 50:
            st.info("Status: On Track")
        else:
            st.error("Status: High Risk")

    # Visual feedback
    st.progress(int(final_grade))