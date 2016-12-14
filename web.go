package main

import (
	"bytes"
	"html/template"
	"log"
	"net/http"
	"os/exec"
)

var templates = template.Must(template.ParseGlob("/home/sm/dumbhome/pages/*.html"))

func main() {
	http.Handle("/style/", http.FileServer(http.Dir("/home/sm/dumbhome")))
	http.HandleFunc("/", doIndex)
	log.Fatal(http.ListenAndServe(":8000", nil))
}

func doIndex(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}

	cmd := exec.Command("/home/sm/dumbhome/hat_stats.py")
	o, err := cmd.Output()
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("exec", err)
	}
	lines := bytes.Split(o, []byte{'\n'})
	err = templates.ExecuteTemplate(w, "index.html", struct{
		PiTemperature string
		PiHumidity string
		}{ string(lines[0]), string(lines[1]) })
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("index template", err)
	}
}
