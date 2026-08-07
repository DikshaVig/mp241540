def get_strategy(cluster_id):
    """
    Maps cluster ID (0-4) directly to:
    1. Cluster Label
    2. Description
    3. Business Recommendation
    """
    segment_data = {
        0: {
            "label": "Target Customers",
            "description": "High Income, Low Spending",
            "recommendation": "Send premium product recommendations, luxury item offers, and personalized incentives to encourage spending."
        },
        1: {
            "label": "VIP / Priority Customers",
            "description": "High Income, High Spending",
            "recommendation": "Enroll in VIP loyalty programs, provide early access to new arrivals, and offer dedicated customer support."
        },
        2: {
            "label": "Careful Spenders",
            "description": "Low Income, High Spending",
            "recommendation": "Offer cashback rewards, discount bundle deals, and flexible payment options."
        },
        3: {
            "label": "Budget-Conscious Customers",
            "description": "Low Income, Low Spending",
            "recommendation": "Highlight clearance sales, value pack discounts, and essential budget item promotions."
        },
        4: {
            "label": "Standard Customers",
            "description": "Average Income, Average Spending",
            "recommendation": "Maintain standard marketing updates, newsletter engagement, and seasonal discount notifications."
        }
    }
    
    return segment_data.get(cluster_id, {
        "label": "General Customer",
        "description": "Unclassified Segment",
        "recommendation": "Apply standard customer engagement strategies."
    })
