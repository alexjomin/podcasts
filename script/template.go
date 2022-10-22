package main

import (
	"bytes"
	_ "embed"
	"encoding/json"
	"log"
	"os"
	"text/template"
	"time"
)

type podcast struct {
	Title       string `json:"title"`
	Description string `json:"description"`
	URL         string `json:"url"`
	Timestamp   int    `json:"timestamp"`
	Date        time.Time
	Link        *string `json:"link,omitempy"`
	Image       *string `json:"image,omitempy"`
}

//go:embed template.html
var podcastTpl string

//go:embed data/methode-scientifique.json
var podcastMethodeScientifique []byte

//go:embed data/conversation-scientifique.json
var podcastConversationScientifique []byte

var tmpl *template.Template

func init() {
	var err error
	tmpl, err = template.New("podcase").Parse(podcastTpl)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	createHTML(podcastConversationScientifique, "conversation-scientifique.html")
	createHTML(podcastMethodeScientifique, "methode-scientifique.html")

}

func createHTML(jsonData []byte, filename string) {
	data := []podcast{}
	err := json.Unmarshal(jsonData, &data)
	if err != nil {
		log.Fatal(err)
	}

	content := []podcast{}

	for _, p := range data {
		p.Date = time.Unix(int64(p.Timestamp), 0)
		content = append(content, p)
	}

	var tpl bytes.Buffer
	err = tmpl.Execute(&tpl, content)
	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile("../public/"+filename, tpl.Bytes(), 0644)
	if err != nil {
		log.Fatal(err)
	}
}
