package main

import (
	"log"
	"net/http"
	"os/exec"
)

func main() {
	http.HandleFunc("/", doIndex)
	log.Fatal(http.ListenAndServe(":8000", nil))
}

func doIndex(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}

	cmd := exec.Command("/home/sm/dumbhome/hat_stats.py")
	cmd.Stdout = w
	err := cmd.Run()
	if err != nil {
		w.Write([]byte(err.Error()))
		log.Println("exec", err)
	}
}
