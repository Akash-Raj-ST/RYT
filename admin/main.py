import psycopg2
from credentials import DB_USER_NAME,DB_PASSWORD,DB
import csv
import gdown
import glob
import random
TEST = True

def get_file_name(file_name):
    file_name_jpg = file_name+".jpg"
    all_files =[f.split('\\')[-1] for f in glob.glob("./media/place/*.jpg")]
    while True:
        if file_name_jpg in all_files:
            file_name = file_name+str(random.randrange(10))
            file_name_jpg = file_name+".jpg"
        else:
            return file_name

def upload_place_data(conn,csv_name):

    cur = conn.cursor()

    def duplicate_place_name(place_name):
        sql = "SELECT pLace_name FROM api_places"
        cur.execute(sql)
        data = cur.fetchall()
        data = [x[0] for x in data]
        data =[''.join(x.split()).lower() for x in data]

        place_name = ''.join(place_name.split()).lower()

        if TEST:
            print(data,"\n",place_name)

        if place_name in data:
            return True
        return False

    #get image from g_drive and save iti in media
    with open(f"admin/{csv_name}.csv","r",encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)
        for data in reader:
            place_name = data[1]
            print(f"[*]Processing {place_name}....")

            if duplicate_place_name(place_name):
                print(f"[*]Place: {place_name} already available :|")
                choice = input("[*]Press 123 to force feed...")
                if choice!="123":
                    print("[*]Place neglected!!!")
                    continue

            image_url = data[3]

            file_id = image_url.split("=")[-1]
            file_name = get_file_name(data[1])

            subject = data[4]
            if len(subject)>100:
                if TEST:
                    subject = subject[:99]
                else:
                    print("[*]Subject length is greater than 100")
                    continue

            try:
                url = image_url.replace("open", "uc")
                output = f'./media/place/{file_name}.jpg'
                gdown.download(url, output, quiet=False)    
            except:
                print("[*]Error uploading:\n",data)
                continue
 
            #upload data to db
            data[3] = f"place/{file_name}.jpg"
            sql = "INSERT INTO api_places(place_name,link,image,subject,place_type,description) VALUES(%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql,tuple(data[1:]))
                print(f"[*] {place_name} added successfully :)")
            except:
                if TEST:
                    print(tuple(data[1:]))  
                print(f"[*]Error uploading data({place_name}) to db :(")
            conn.commit()
    
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

    print("[*]1.Upload Place Data from place_db.csv to DB")
    option = input("Your Choice:")
    if option=="1":
        csv_name = input("Enter CSV file name:");
        upload_place_data(conn=conn,csv_name=csv_name)
    else:
        print("[*]Connection Closed!!!")
        conn.close()