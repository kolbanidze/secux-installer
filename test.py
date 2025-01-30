def convert_bytes_to_human_readable(size_in_bytes):
    # Define the size units
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    
    # Initialize the unit index
    unit_index = 0
    
    # Convert bytes to the appropriate unit
    while size_in_bytes >= 1024 and unit_index < len(units) - 1:
        size_in_bytes /= 1024
        unit_index += 1
    
    # Return the formatted string with 2 decimal places
    return f"{size_in_bytes:.2f} {units[unit_index]}"

# Example usage
print(convert_bytes_to_human_readable(1024))          # Output: 1.00 KiB
print(convert_bytes_to_human_readable(1048576))       # Output: 1.00 MiB
print(convert_bytes_to_human_readable(1073741824))    # Output: 1.00 GiB
print(convert_bytes_to_human_readable(1099511627776)) # Output: 1.00 TiB