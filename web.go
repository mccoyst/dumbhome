package main

import (
	"database/sql"
	"html/template"
	"log"
	"net/http"

	_ "rsc.io/sqlite"
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

	db, err := sql.Open("sqlite3", "/home/sm/dumbhome/readings.db")
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

	todayIn, err := pastDayReadings(db, "inside")
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("today inside", err)
		return
	}
	todayOut, err := pastDayReadings(db, "outside")
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("today outside", err)
		return
	}


	err = templates.ExecuteTemplate(w, "index.html", struct{
		PiTemperature float64
		PiHumidity float64
		PiDay []xy
		WeatherTemperature float64
		WeatherHumidity float64
		WeatherDay []xy
		}{ c, h, todayIn, wc, wh, todayOut })
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("index template", err)
	}
}

type xy struct {
	X float64
	Y float64
}

func pastDayReadings(db *sql.DB, table string) ([]xy, error) {
	rows, err := db.Query("select time,temp_c from " + table + " where time > strftime('%s','now') - 24*60*60")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var xys []xy
	for rows.Next() {
		var t int
		var c float64
		err = rows.Scan(&t, &c)
		if err != nil {
			return nil, err
		}
		xy := struct{
			X float64
			Y float64
			}{ float64(t), c }
		xys = append(xys, xy)
	}
	if err = rows.Err(); err != nil {
		return nil, err
	}

	return xys, nil
}
