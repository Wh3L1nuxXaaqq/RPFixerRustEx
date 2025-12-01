import os
import json
import zipfile
import shutil

def fix(content):
    try:
        json.loads(content)
        return content
    except json.JSONDecodeError as e:
        end_pos = e.pos
        if end_pos:
            return content[:end_pos].strip()
        else:
            raise e

def fixer(zip_path, output_zip_path):
    temp_dir = "temp"

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        blockstates_path = os.path.join(temp_dir, "assets", "minecraft", "blockstates")

        if not os.path.exists(blockstates_path):
            print("???")
            return

        for root, _, files in os.walk(blockstates_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        cleaned_content = fix(content)

                        json.loads(cleaned_content)

                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(cleaned_content)
                        print(f"[+] {file_path}")
                    except Exception as e:
                        print(f"[-] {file_path}: {e}")

        shutil.make_archive(output_zip_path.replace(".zip", ""), 'zip', temp_dir)
        print(f"fixed: {output_zip_path}")

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


input_zip = "rp.zip"
import random
output_zip = f"output\\fixed_resourcepack-{str(random.randint(0,999999))}.zip"
fixer(input_zip, output_zip)
input()
