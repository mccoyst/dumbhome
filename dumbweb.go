package main

import (
	"database/sql"
	"flag"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"time"

	_ "rsc.io/sqlite"
)

var resourceDir = flag.String("d", ".", "path to images, tempates, etc.")
var zipcode = flag.String("zip", "03801", "your favorite zipcode")

var templates *template.Template
var wunderkey string

func main() {
	flag.Parse()
	templates = template.Must(template.ParseGlob(*resourceDir+"/pages/*.html"))

	wk, err := ioutil.ReadFile(*resourceDir+"/wunder.key")
	if err != nil {
		log.Fatal(err)
	}
	wunderkey = string(wk)

	go weatherReport()

	http.Handle("/style/", http.FileServer(http.Dir(*resourceDir)))
	http.HandleFunc("/record", recordTemp)
	http.HandleFunc("/", doIndex)
	log.Fatal(http.ListenAndServe(":8000", nil))
}

func doIndex(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}

	if r.Method != "GET" {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}

	log.Println("GET", r.URL)

	db, err := sql.Open("sqlite3", *resourceDir+"/readings.db")
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("db open", err)
		return
	}
	defer db.Close()
	var t int
	var c, h, wc, wh float64
	row := db.QueryRow("select max(time),temp_c,humidity from inside")
	err = row.Scan(&t, &c, &h)
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("db inside query", err)
		return
	}
	row = db.QueryRow("select max(time),temp_c,humidity from outside")
	err = row.Scan(&t, &wc, &wh)
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("db outside query", err)
		return
	}

	err = templates.ExecuteTemplate(w, "index.html", struct{
		PiTemperature float64
		PiHumidity string
		WeatherTemperature float64
		WeatherHumidity string
		}{ c, estimateDewpoint(c, h), wc, estimateDewpoint(wc, wh) })
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("index template", err)
	}
}

func recordTemp(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}

	log.Printf("Got %sC, %s%%\n", r.FormValue("t"), r.FormValue("h"));

	t, err := strconv.ParseFloat(r.FormValue("t"), 64)
	if err != nil {
		http.Error(w, "bad temperature " +r.FormValue("t"), http.StatusBadRequest)
		return
	}

	h, err := strconv.ParseFloat(r.FormValue("h"), 64)
	if err != nil {
		http.Error(w, "bad temperature " +r.FormValue("h"), http.StatusBadRequest)
		return
	}

	db, err := sql.Open("sqlite3", *resourceDir+"/readings.db")
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("db open", err)
		return
	}
	defer db.Close()

	_, err = db.Exec("insert into inside (time, temp_c, humidity) values (?, ?, ?)",
		time.Now().Unix(), t, h)
	if err != nil {
		w.Write([]byte("BAD"))
		log.Println("db insert 'inside'", err)
		return
	}

	w.Write([]byte("OK"))
}

func estimateDewpoint(t, h float64) string {
	// https://www.sciencedaily.com/releases/2005/03/050329133131.htm
	d := t - (100-h)/5
	log.Printf("Dewpoint estimate for %.1f at %.0f%%: %.1f", t, h, d)
	// https://youtu.be/GtmOlpbkQDw
	if t < 0 || d < 15.6 {
		return "seems cold"
	} else if d > 18.3 {
		return "might be moist"
	}
	return "probably fine"
}

func weatherReport() {
/*
	api := "http://api.wunderground.com/api/"+wunderkey+"/conditions/q/"+*zipcode+".json"
	tt := time.Tick(30 * time.Minute)
	for now := range tt {
		r, err := http.Get(api)
		if err != nil {
			log.Println("OOPS:", err)
			continue
		}
		if r.StatusCode != 200 {
			log.Println("OOPS:", r.Status)
			r.Body.Close()
			continue
		}

		blob, err := ioutile.ReadAll(r.Body)
		r.Body.Close()
		if err != nil {
			log.Println("OOPS:", err)
			continue
		}

		var data map[string]interface{}
		err = json.Unmarshall(blob, &data)
		if err != nil {
			log.Println("OOPS:", err)
			continue
		}

		current, ok := data.(map[string]string)
		if !ok {
			log.Println("OOPS:", "Not the JSON I expected", string(blob))
			continue
		}

		
	}
*/
}
