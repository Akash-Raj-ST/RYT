import psycopg2
from credentials import DB_USER_NAME,DB_PASSWORD,DB
import csv
import gdown
import glob
import random
TEST = True
DEBUG = True

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

        if DEBUG:
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

            if len(data[4])>100:
                if TEST:
                    data[4] = data[4][:99]
                    print("[*]Subject Trimmed")
                else:
                    print("[*]Subject length is greater than 100")
                    continue
            
            if len(data[6])>400:
                if TEST:
                    data[6] =data[6][:400]
                    print("[*]Description Trimmed")
                else:
                    print("[*]Description length is greater than 100")
            try:
                url = image_url.replace("open", "uc")
                output = f'./media/place/{file_name}.jpg'
                gdown.download(url, output, quiet=False)    
            except:
                print("[*]Error uploading pic :\n",data)
                continue
 
            #upload data to db
            data[3] = f"place/{file_name}.jpg"
            sql = "INSERT INTO api_places(place_name,link,image,subject,place_type,description) VALUES(%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql,tuple(data[1:]))
                print(f"[*] {place_name} added successfully :)")
            except:
                if DEBUG:
                    print(tuple(data[1:]))  
                print(f"[*]Error uploading data({place_name}) to db :(")
            conn.commit()
    
def upload_review_data(conn,csv_name):
    cur = conn.cursor()

    with open(f"admin/{csv_name}.csv","r",encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)
        for data in reader:
            user = data[1]
            place = data[2]
            content = data[3]
            tags = data[4].strip().split(" ")
            likes = data[5]
            date = data[6]
            images = data[7].split(";")

            if DEBUG:
                print("User: ",user)
                print("Place: ",place)            
                print("Content: ",content)
                print("Likes: ",likes)
                print("Date: ",date)

                count = 0
                for tag in tags:
                    count += 1 
                    print(f"tag{count} :",tag)

                count = 0
                for image in images:
                    count += 1 
                    print(f"Image{count} :",image)

            
            sql = "INSERT INTO api_review(content,likes,p_id_id,u_id_id,date_uploaded) VALUES(%s,%s,%s,%s,%s) RETURNING r_id"

            cur.execute(sql,(content,likes,place,user,date))
            review_id = cur.fetchone()[0]
            conn.commit()

            if TEST:
                print("Review id: ",review_id)

            sql = "INSERT INTO api_review_tag(tags,r_id_id) VALUES(%s,%s)"
            for tag in tags:
                if tag[0] == "#":
                    tag = tag[1:]
                cur.execute(sql,(tag,review_id))

            sql = "INSERT INTO api_review_pic(r_pic,r_id_id) VALUES(%s,%s)"
            count = 0
            for image_url in images:
                count += 1
                try:
                    file_name = str(review_id)+"_"+str(count)
                    file_url = f"review/{file_name}.jpg"
                    url = image_url.replace("open", "uc")
                    output = f'./media/review/{file_name}.jpg'
                    gdown.download(url, output, quiet=False)    
                except:
                    print(f"[*]Error downloading image{count}\n")
                    continue
                cur.execute(sql,(file_url,review_id))

            conn.commit()

def map_data(conn):
    cur = conn.cursor()

    main_place_id = int(input("Enter main place id:"))
    sub_place_st = int(input("Subplace start id:"))
    sub_place_en = int(input("Subplace end id:"))

    if main_place_id==sub_place_en or main_place_id==sub_place_st:
        print("[*]Main place cannot be subplace")
        return
    sql = "INSERT INTO api_place_map(pm_id_id,spm_id_id) VALUES(%s,%s)"
    for i in range(sub_place_st,sub_place_en+1):
        cur.execute(sql,(main_place_id,i))
        if DEBUG:
            print(f"Map: {main_place_id}:{i}")
    conn.commit()

def connect():
    db_env = os.environ.get('DATABASE_URL')
    try:
        DATABASE_URL = db_env
        conn = psycopg2.connect(DATABASE_URL)

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return None

if __name__ == "__main__":
    conn = connect()
    print("[*]1.Upload Place Data from csv to DB")
    print("[*]2.Upload Review Data from csv to DB")
    print("[*]3.Map Place Data")

    print('--Check if permissions are provided--')

    option = input("Your Choice:")
    if option=="1":
        csv_name = input("Enter CSV file name: ")
        upload_place_data(conn=conn,csv_name=csv_name)
    elif option=="2":
        csv_name = input("Enter CSV file name: ")
        upload_review_data(conn=conn,csv_name=csv_name)
    elif option=="3":
        map_data(conn)
    else:
        print("[*]Connection Closed!!!")
        conn.close()