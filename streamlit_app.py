import streamlit as st

def get_sample_size(lot_size, inspection_level):
    """Determine sample size based on lot size and inspection level"""
    # Sample size tables for general and special inspection levels
    general_level = {
        'I': [2, 8, 20, 50, 125, 315, 800, 2000, 5000, 12500, 31500],
        'II': [2, 8, 20, 50, 125, 315, 800, 2000, 5000, 12500, 31500],
        'III': [2, 8, 20, 50, 125, 315, 800, 2000, 5000, 12500, 31500]}
    
    special_level = {
        'S-1': [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200],
        'S-2': [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200],
        'S-3': [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200],
        'S-4': [2, 3, 5, 8, 13, 20, 32, 50, 80, 125, 200]}
    
    # Lot size ranges
    lot_ranges = [
        (2, 8), (9, 15), (16, 25), (26, 50), (51, 90),
        (91, 150), (151, 280), (281, 500), (501, 1200),
        (1201, 3200), (3201, 10000), (10001, 35000),
        (35001, 150000), (150001, 500000), (500001, float('inf'))
    ]
    
    # Find the appropriate index based on lot size
    index = 0
    for i, (low, high) in enumerate(lot_ranges):
        if low <= lot_size <= high:
            index = i
            break
    
    # Get sample size based on inspection level
    if inspection_level in ['I', 'II', 'III']:
        return general_level[inspection_level][min(index, len(general_level[inspection_level])-1)]
    elif inspection_level in ['S-1', 'S-2', 'S-3', 'S-4']:
        return special_level[inspection_level][min(index, len(special_level[inspection_level])-1)]
    else:
        return 0  # Invalid inspection level

def aql_calculator(lot_size, inspection_level, aql_level):
    """Calculate AQL values with GIL support"""
    # Standard AQL limits (accept, reject)
    aql_limits = {
        0.010: (0, 1),
        0.015: (0, 1),
        0.025: (0, 1),
        0.040: (0, 1),
        0.065: (0, 1),
        0.10: (0, 1),
        0.15: (0, 1),
        0.25: (0, 2),
        0.40: (0, 3),
        0.65: (0, 4),
        1.0: (0, 7),
        1.5: (0, 10),
        2.5: (0, 14),
        4.0: (0, 20),
        6.5: (0, 30)
    }
    
    # Get sample size based on inspection level
    sample_size = get_sample_size(lot_size, inspection_level)
    
    if sample_size == 0:
        return {"Error": "Invalid inspection level"}
    
    # Calculate accept and reject points
    if aql_level in aql_limits:
        accept_point, reject_point = aql_limits[aql_level]
        
        # For very small AQL levels, we need special handling
        if aql_level <= 0.065:
            if sample_size <= 8:
                accept_point = 0
                reject_point = 1
            elif sample_size <= 32:
                accept_point = 1 if aql_level >= 0.065 else 0
                reject_point = 2 if aql_level >= 0.065 else 1
            else:
                accept_point = int(sample_size * (aql_level / 100)) if (sample_size * (aql_level / 100)) >= 1 else 0
                reject_point = accept_point + 1
        else:
            accept_point = int(sample_size * (aql_level / 100))
            reject_point = accept_point + 1
    else:
        return {"Error": "Invalid AQL level"}
    
    return {
        "Sample Size": sample_size,
        "Accept Point": accept_point,
        "Reject Point": reject_point,
        "Inspection Level": inspection_level
    }

# Streamlit UI
def main():
    st.title("AQL Calculator with GIL (General/Special Inspection Level)")
    
    st.markdown("""
    This calculator helps determine sample size and acceptance criteria based on:
    - Lot size
    - Inspection level (General I, II, III or Special S-1 to S-4)
    - AQL (Acceptable Quality Level)
    """)
    
    # Input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        lot_size = st.number_input("Lot Size", min_value=2, value=2000)
    
    with col2:
        inspection_level = st.selectbox(
            "Inspection Level",
            options=['I', 'II', 'III', 'S-1', 'S-2', 'S-3', 'S-4'],
            index=1
        )
    
    with col3:
        aql_level = st.selectbox(
            "AQL Level (%)",
            options=[0.010, 0.015, 0.025, 0.040, 0.065, 0.10, 0.15, 0.25, 
                     0.40, 0.65, 1.0, 1.5, 2.5, 4.0, 6.5],
            index=11
        )
    
    # Calculate button
    if st.button("Calculate AQL"):
        result = aql_calculator(lot_size, inspection_level, aql_level)
        
        if "Error" in result:
            st.error(result["Error"])
        else:
            st.success("AQL Calculation Results")
            st.markdown(f"""
            - *Sample Size*: {result['Sample Size']}
            - *Accept Point*: {result['Accept Point']}
            - *Reject Point*: {result['Reject Point']}
            - *Inspection Level*: {result['Inspection Level']}
            """)
            
            # Additional explanation
            st.info(f"""
            For a lot size of {lot_size} with {inspection_level} inspection level and AQL {aql_level}%:
            - You should inspect *{result['Sample Size']}* items
            - Accept the lot if defects are *≤ {result['Accept Point']}*
            - Reject the lot if defects are *≥ {result['Reject Point']}*
            """)

if _name_ == "_main_":
    main()
