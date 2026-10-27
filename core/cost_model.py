def calculate_edge_weight(base_distance, crowd_density):
    """
    Calculates the effective weight of an edge based on crowd density.
    High density increases the cost (weight) to avoid that path.
    """
    multiplier = 1.0
    
    # Crowd density ke hisaab se multiplier set karo
    if crowd_density == 'Low':
        multiplier = 1.0  # Normal speed
    elif crowd_density == 'Medium':
        multiplier = 1.5  # Thoda slow
    elif crowd_density == 'High':
        multiplier = 3.0  # Bahut slow (High cost to avoid)
    else:
        multiplier = 1.0

    # Final weight calculate karo
    effective_weight = base_distance * multiplier
    return effective_weight

# Test karne ke liye
if __name__ == '__main__':
    print(" Testing Cost Model Function...")
    
    distance = 10.0 # 10 meters
    
    w_low = calculate_edge_weight(distance, 'Low')
    print(f"Low Density (10m): Weight = {w_low}")
    
    w_med = calculate_edge_weight(distance, 'Medium')
    print(f"Medium Density (10m): Weight = {w_med}")
    
    w_high = calculate_edge_weight(distance, 'High')
    print(f"High Density (10m): Weight = {w_high}")