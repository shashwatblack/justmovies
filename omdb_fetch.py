import csv
import requests

omdb_url = "http://www.omdbapi.com/"


class OmdbKey:
    keys = []
    current_key_index = None

    def load_keys(self):
        with open('omdb_keys.txt') as keysfile:
            keys = keysfile.readlines()

        self.keys = [{
            "key": k.strip(),
            "used": 0
        } for k in keys]
        self.current_key_index = 0

    def get_key(self):
        if not self.keys:
            return None
        current_key = self.keys[self.current_key_index]
        return current_key["key"]

    def next(self):
        self.current_key_index += 1
        print("----------------------------------------------------------------")
        print("switched key to ", self.current_key_index)
        print("----------------------------------------------------------------")


omdb_key = OmdbKey()
omdb_key.load_keys()

with open('movies_with_omdb.csv', mode='w', newline='') as export_file:
    writer = csv.writer(export_file)
    with open('movies.csv') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        writer.writerow(["title","year","omdb_data"])

        count = 0
        for row in reader:
            while True:
                print("FETCHING", row[6], row[14])
                r = requests.get(omdb_url, params={
                    "t": row[6],
                    "y": row[14],
                    "apikey": omdb_key.get_key()
                })
                if r.status_code == 200:
                    row.append(r.json())
                    writer.writerow([row[6],row[14],r.json()])
                    count += 1
                    print("DONE ", count, r.status_code, row[6])
                    break
                else:
                    omdb_key.next()
