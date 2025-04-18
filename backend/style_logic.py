from product_data import product_catalog

def suggest_outfits(request):
    matched = []

    # Budget filter
    budget = request.budget
    temp = request.temperature
    occasion = request.occasion
    color_vibe = request.color_vibe

    # Define temperature thresholds
    cold_temp = 16  # °C and below = chilly
    warm_temp = 24  # °C and above = warm

    for item in product_catalog:
        # Match occasion and color vibe
        if occasion not in item["occasion"]:
            continue
        if color_vibe != item["color_vibe"]:
            continue
        if budget != item["budget"]:
            continue

        # Match temperature to clothing weight/type
        if temp <= cold_temp and item["weight"] != "heavy":
            continue  # Only heavy allowed when chilly
        if temp >= warm_temp and item["weight"] == "heavy":
            continue  # Avoid heavy when warm

        # Check if temperature is within item's range
        if not (item["temp_range"][0] <= temp <= item["temp_range"][1]):
            continue

        matched.append({
            "name": item["name"],
            "description": item["description"],
            "price": item["price"],
            "why": (
                f"Perfect for {occasion} occasions with your {color_vibe} vibe. "
                f"{'Keeps you warm' if item['weight']=='heavy' else 'Light and comfy'} for {temp}°C."
            )
        })

    # If less than 3, relax color_vibe, then weight, then budget
    if len(matched) < 3:
        for relax in ["color_vibe", "weight", "budget"]:
            for item in product_catalog:
                if occasion not in item["occasion"]:
                    continue
                if relax != "color_vibe" and color_vibe != item["color_vibe"]:
                    continue
                if relax != "budget" and budget != item["budget"]:
                    continue
                if temp <= cold_temp and relax != "weight" and item["weight"] != "heavy":
                    continue
                if temp >= warm_temp and relax != "weight" and item["weight"] == "heavy":
                    continue
                if not (item["temp_range"][0] <= temp <= item["temp_range"][1]):
                    continue
                if item not in matched:
                    matched.append({
                        "name": item["name"],
                        "description": item["description"],
                        "price": item["price"],
                        "why": f"Good alternative for {occasion} and {temp}°C."
                    })
                if len(matched) >= 3:
                    break
            if len(matched) >= 3:
                break

    return matched[:3]
