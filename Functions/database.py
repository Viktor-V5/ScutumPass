import os
import sqlcipher3


# Scutum Pass database

def connect_to_scutum_pass_db(db_path : str,key : bytes):
    conn = sqlcipher3.connect(db_path)
    conn.execute(f"PRAGMA key=\"x'{key.hex()}'\"")       
    conn.execute("PRAGMA cipher_page_size=4096") 
    conn.execute("PRAGMA kdf_iter=64000")       
    return conn

def create_password_Managerdb(pass_db_path : str,key : bytes):
    with connect_to_scutum_pass_db(pass_db_path,key) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE passwordcontainer (
            grp TEXT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            createdAt TEXT NOT NULL,
            updatedAt TEXT NOT NULL
        )
        """)

        conn.commit()

def insert_password_row(grp : str,name : str,email: str,password: str,created_at : str,updated_at : str,pass_db_path : str,key : bytes):
    with connect_to_scutum_pass_db(pass_db_path,key) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO passwordcontainer             
        (grp,
        name,
        email,
        password,
        createdAt,
        updatedAt)

        VALUES (?,?,?,?,?,?)
        
        
        """,(grp , name, email, password, created_at, updated_at))

        conn.commit()

def select_db_data(pass_db_path : str,key : bytes):
    with connect_to_scutum_pass_db(pass_db_path,key) as connect:
        cursor = connect.cursor()
        records = cursor.execute(f"SELECT grp,name,email,createdAt,updatedAt FROM passwordcontainer")
        connect.commit()
        selected_records = records.fetchall()
        cursor.close()
    
    return selected_records

def delete_record_db(pass_db_path: str, key: bytes, name: str):
    name = name.strip()

    with connect_to_scutum_pass_db(pass_db_path, key) as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM passwordcontainer WHERE name = ?",(name,))

        conn.commit()

def load_data(pass_db_path : str,key : bytes,name : str):
    with connect_to_scutum_pass_db(pass_db_path,key) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwordcontainer WHERE name = ?",(name,))
        result = cursor.fetchall()

    return result

def password_name_check(pass_db_path: str, key: bytes, name: str):
    with connect_to_scutum_pass_db(pass_db_path, key) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM passwordcontainer WHERE name = ? LIMIT 1",
            (name,)
        )
        result = cursor.fetchone()

    if result is not None:
        return False

    return True

def edit_db_data(grp, name, email, password, created_at, updated_at, pass_db_path, key,old_name):
    name = name.strip()

    delete_record_db(pass_db_path, key, old_name)

    insert_password_row(
        grp,
        name,
        email,
        password,
        created_at,
        updated_at,
        pass_db_path,
        key
    )

def get_db_password(pass_db_path: str, key: bytes, row_name: str):
    with connect_to_scutum_pass_db(pass_db_path, key) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM passwordcontainer WHERE name = ?",
            (row_name,)
        )
        result = cursor.fetchone()

    if result is None:
        return False  

    return result[0]  

def select_all_db_data(pass_db_path : str,key : bytes):
    with connect_to_scutum_pass_db(pass_db_path,key) as connect:
        cursor = connect.cursor()
        records = cursor.execute(f"SELECT * FROM passwordcontainer")
        connect.commit()
        selected_records = records.fetchall()
        cursor.close()

        column_names = [description[0] for description in cursor.description]
    
    return selected_records,column_names

def change_db_key(db_path: str, old_key: bytes, new_key: bytes) -> bool:
    try:
        with connect_to_scutum_pass_db(db_path, old_key) as conn:
            conn.execute(f"PRAGMA rekey=\"x'{new_key.hex()}'\"")
            conn.commit()

        with connect_to_scutum_pass_db(db_path, new_key) as conn:
            conn.execute("SELECT COUNT(*) FROM passwordcontainer").fetchone()

        return True

    except sqlcipher3.DatabaseError:
        return False

