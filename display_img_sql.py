import cv2
import psycopg2
from io import BytesIO
import numpy as np

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    host="localhost",
    database="HR",
    user="postgres",
    password="Bigv@567"
)

# Replace 'your_table' and 'your_image_id' with your actual table and image ID
table_name = 'classification_data'
image_id = 2

# Query to retrieve image data
query = f"SELECT image FROM {table_name} WHERE id = %s;"

# Retrieve the image data from the database
with connection.cursor() as cursor:
    cursor.execute(query, (image_id,))
    result = cursor.fetchone()

if result:
    image_data = result[0]

    # Convert bytea data to a bytearray
    byte_array = bytearray(image_data)

    # Convert the bytearray to a bytes-like object
    bytes_io = BytesIO(byte_array)

    # Read the image using OpenCV
    image = cv2.imdecode(np.frombuffer(bytes_io.read(), np.uint8), cv2.IMREAD_COLOR)

    # Display the image using OpenCV
    cv2.imshow('Image from PostgreSQL', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(f"No image found for ID {image_id}")

# Close the database connection
connection.close()
