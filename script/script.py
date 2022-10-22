import requests
import json
import time

current_cursor = "MA=="
podcasts = []

def create_url(cursor) :
	# return f"https://www.radiofrance.fr/api/v1.9/concepts/d47d3c2b-44e3-11e5-9fe0-005056a87c89/expressions?pageCursor={cursor}%3D&includeFutureExpressionsWithManifestations=true&noLimitDate=true"
	return f"https://www.radiofrance.fr/api/v1.9/concepts/c8b34845-b807-4377-bb44-3f3c712299a0/expressions?pageCursor={cursor}%3D&includeFutureExpressionsWithManifestations=true&noLimitDate=true"

def get_content(cursor):
	url = create_url(cursor)
	r = requests.get(url)
	if r.status_code == 200:
		data = r.json()
		return data["next"], data
	else :
		return "", {}


def content(cursor):
	global current_cursor
	global podcasts
	print("cursor ", cursor)
	current_cursor, content = get_content(cursor)
	url = ""

	for podcast in content["items"]:
		for manifestation in podcast["manifestations"]:
			url = manifestation["url"]
			break

		if url == "":
			continue

		d = {
			"title":  podcast["title"],
			"description": podcast["standFirst"],
			"url": url,
			"timestamp": podcast["startDate"],
		}

		if "path" in podcast and podcast["path"] != None:
			d["link"] = "https://www.radiofrance.fr/" + podcast["path"]

		if "visual" in podcast and podcast["visual"] != None:
			if "src" in podcast["visual"]:
				d["image"] = podcast["visual"]["src"]

		podcasts.append(d)

	time.sleep(0.5)

while current_cursor != "" and current_cursor is not None:
	content(current_cursor)

json_data = json.dumps(podcasts, indent=4)
f = open("data.json", 'w')
f.write(json_data)
