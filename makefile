.PHONY: all

bin_dir := $(GOPATH)/bin
resource_dir := $(GOPATH)/dumbhome

hat_in := \
	every_minute.py \
	every_thirty.py \

hat_out := $(patsubst %,$(bin_dir)/%,$(hat_in))

resources_in := \
	$(wildcard *.png) \
	$(wildcard style/*.css) \
	$(wildcard pages/*.html) \

resources_out := $(patsubst %,$(resource_dir)/%,$(resources_in))


all: $(bin_dir)/dumbhome $(hat_out) $(resources_out) /lib/systemd/system/dumbhome.service

$(bin_dir)/dumbhome: $(wildcard *.go)
	go install

$(bin_dir)/%.py: %.py
	cp $< $@

$(resource_dir)/%.png: %.png
	cp $< $@

$(resource_dir)/style/%.css: style/%.css $(resource_dir)/style
	cp $< $@
$(resource_dir)/style:
	mkdir $@

$(resource_dir)/pages/%.html: pages/%.html $(resource_dir)/pages
	cp $< $@
$(resource_dir)/pages:
	mkdir $@

/lib/systemd/system/%.service: %.service
	cp $< $@
