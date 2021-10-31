import psycopg2
from credentials import DB_USER_NAME,DB_PASSWORD,DB
import csv
import gdown
import glob
import random

def get_file_name(file_name):
    file_name_jpg = file_name+".jpg"
    all_files =[f.split('\\')[-1] for f in glob.glob("./media/place/*.jpg")]
    while True:
        if file_name_jpg in all_files:
            file_name = file_name+str(random.randrange(10))
            file_name_jpg = file_name+".jpg"
        else:
            return file_name

def upload_place_data(conn):
    with open("admin/place_db.csv","r") as f:
        reader = csv.reader(f)
        next(reader)
        for data in reader:
            image_url = data[3]
            file_id = image_url.split("=")[-1]
            file_name = get_file_name(data[1])
        
            try:
                url = image_url.replace("open", "uc")
                output = f'./media/place/{file_name}.jpg'
                gdown.download(url, output, quiet=False)    
            except:
                print("[*]Error uploading:\n",data)

def connect():

    try:
        conn = psycopg2.connect(
                database=DB,
                user=DB_USER_NAME,
                password=DB_PASSWORD,
                host='localhost'
                )

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return None

if __name__ == "__main__":
    conn = connect()

    print("[*]1.Upload Place Data from place_db.csv to DB/n")
    option = input("Your Choice:")
    if option=="1":
        upload_place_data(conn=conn)
    else:
        print("[*]Connection Closed!!!")
        conn.close()