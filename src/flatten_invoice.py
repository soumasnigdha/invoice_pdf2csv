import re

def normalize_whitespace(text):
    """
    Replaces any sequence of whitespace characters (including newlines) 
    with a single space.
    """    
    if text is None:
        return None
    return re.sub(r'\s+', ' ', str(text)).strip()

def flatten_invoice_data(invoice_data):
    """
    Flattens a single invoice's nested JSON data into a list of dictionaries
    suitable for CSV, with one row per item.
    Skips "Shipping And Handling Charges" and "Shipping And Packaging Charges" from being treated as a product item.
    """
    flattened_rows = []

    # Extract top-level details
    base_data = {
        "seller_name": invoice_data.get("seller_name"),
        "seller_gstin": invoice_data.get("seller_gstin"),
        "invoice_number": invoice_data.get("invoice_number"),
        "order_id": invoice_data.get("order_id"),
        "order_date": invoice_data.get("order_date"),
        "invoice_date": invoice_data.get("invoice_date"),
        "pan": invoice_data.get("pan"),
        "grand_total": invoice_data.get("grand_total"),
        "selling_website": invoice_data.get("selling_website")
    }

    # Flatten bill_to_address
    bill_to = invoice_data.get("bill_to_address", {})
    base_data["bill_to_name"] = normalize_whitespace(bill_to.get("name"))
    base_data["bill_to_full_address"] = normalize_whitespace(bill_to.get("full_address"))
    base_data["bill_to_phone"] = bill_to.get("phone")

    # Flatten ship_to_address
    ship_to = invoice_data.get("ship_to_address", {})
    base_data["ship_to_name"] = normalize_whitespace(ship_to.get("name"))
    base_data["ship_to_full_address"] = normalize_whitespace(ship_to.get("full_address"))
    base_data["ship_to_phone"] = ship_to.get("phone")

    # Flatten shipping_handling_charges 
    shipping_charges = invoice_data.get("shipping_handling_charges", {})
    base_data["shipping_qty"] = shipping_charges.get("qty")
    base_data["shipping_gross_amount"] = shipping_charges.get("gross_amount")
    base_data["shipping_discounts_coupons"] = shipping_charges.get("discounts_coupons")
    base_data["shipping_taxable_value"] = shipping_charges.get("taxable_value")
    base_data["shipping_sgst_utgst_amount"] = shipping_charges.get("sgst_utgst_amount")
    base_data["shipping_cgst_amount"] = shipping_charges.get("cgst_amount")
    base_data["shipping_igst_amount"] = shipping_charges.get("igst_amount")
    base_data["shipping_total_amount"] = shipping_charges.get("total_amount")

    items = invoice_data.get("items", [])
    
    # Filter out "Shipping And Handling Charges" and "Shipping And Packaging Charges" from items if it's there
    product_items = [item for item in items if item.get("product_name") != "Shipping And Handling Charges" and item.get("product_name") != "Shipping And Packaging Charges"]

    if not product_items:
        # If no actual product items, still creating one row with just invoice data
        flattened_rows.append(base_data)
    else:
        for item in product_items: # Iterate over filtered product items
            row = base_data.copy() # Start with a copy of base invoice data
            # Adding item-specific details
            row["item_product_name"] = normalize_whitespace(item.get("product_name"))
            row["item_fsn"] = item.get("fsn")
            row["item_hsn_sac"] = item.get("hsn_sac")
            row["item_qty"] = item.get("qty")
            row["item_gross_amount"] = item.get("gross_amount")
            row["item_discounts_coupons"] = item.get("discounts_coupons")
            row["item_taxable_value"] = item.get("taxable_value")
            row["item_sgst_utgst_amount"] = item.get("sgst_utgst_amount")
            row["item_cgst_amount"] = item.get("cgst_amount")
            row["item_igst_amount"] = item.get("igst_amount")
            row["item_total_amount"] = item.get("total_item_amount")
            flattened_rows.append(row)

    return flattened_rows