# Makefile for rendering Manim animations using Docker and converting MP4 to WebM

# Default variables (can be overridden from command line)
DOCKER = docker run --rm -it -v $(shell pwd):/manim manimcommunity/manim manim
FILE ?= two_sum_visual.py
SCENE ?= TwoSumScene
OUTPUT_DIR = media

# Default target
.PHONY: all
all: high

# Render in low quality (480p, 15fps)
.PHONY: low
low:
	$(DOCKER) $(FILE) $(SCENE) -pql

# Render in medium quality (720p, 30fps)
.PHONY: medium
medium:
	$(DOCKER) $(FILE) $(SCENE) -pqm

# Render in high quality (1080p, 60fps)
.PHONY: high
high:
	$(DOCKER) $(FILE) $(SCENE) -pqh

# Preview without saving (low quality)
.PHONY: preview
preview:
	$(DOCKER) $(FILE) $(SCENE) -p -ql

# Clean up generated media files
.PHONY: clean
clean:
	rm -rf $(OUTPUT_DIR)

# Convert MP4 to WebM
.PHONY: convert
convert:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Error: Both INPUT and OUTPUT are required."; \
		echo "Example: make convert INPUT=media/two_sum/videos/input.mp4 OUTPUT=media/two_sum/videos/output.webm"; \
		exit 1; \
	fi
	@docker run --rm -v $(shell pwd):/data jrottenberg/ffmpeg -i "/data/$$(echo '$(INPUT)' | sed 's|^/||')" -c:v libvpx-vp9 -c:a libvorbis -y "/data/$$(echo '$(OUTPUT)' | sed 's|^/||')"

# Help message
.PHONY: help
help:
	@echo "Usage: make [target] [options]"
	@echo "Targets:"
	@echo "  low      - Render in low quality (480p, 15fps)"
	@echo "  medium   - Render in medium quality (720p, 30fps)"
	@echo "  high     - Render in high quality (1080p, 60fps) [default]"
	@echo "  preview  - Preview animation without saving (low quality)"
	@echo "  clean    - Remove generated media files"
	@echo "  convert  - Convert MP4 to WebM (requires INPUT and OUTPUT)"
	@echo "Options for render targets:"
	@echo "  FILE=<file> SCENE=<scene>"
	@echo "Options for convert target:"
	@echo "  INPUT=<input.mp4> OUTPUT=<output.webm> (relative to current directory)"
	@echo "Examples:"
	@echo "  make preview FILE=consistent_hashing_visual.py SCENE=ConsistentHashingScene"
	@echo "  make convert INPUT=media/two_sum/videos/input.mp4 OUTPUT=media/two_sum/videos/output.webm"
	@echo "  make convert INPUT=/media/two_sum/videos/input.mp4 OUTPUT=/media/two_sum/videos/output.webm (leading / is ignored)"