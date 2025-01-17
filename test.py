import subprocess

def get_uuid_by_partition(partition):
    try:
        # Run the blkid command for the specific partition
        result = subprocess.run(
            ["blkid", partition],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            # Handle error (e.g., partition not found)
            raise Exception(result.stderr.strip())
        
        # Parse the output to extract the UUID
        output = result.stdout.strip()
        for part in output.split():
            if part.startswith("UUID="):
                return part.split("=")[1].strip('"')
    except Exception as e:
        print(f"Error: {e}")
    return None

# Example usage
partition = "/dev/sda5"  # Replace with your partition name
uuid = get_uuid_by_partition(partition)
if uuid:
    print(f"UUID of {partition}: {uuid}")
else:
    print(f"UUID for {partition} could not be retrieved.")
