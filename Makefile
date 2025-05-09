# Makefile for rendering Manim animations using Docker and converting MP4 to WebM or GIF

# Default variables (can be overridden from command line)
DOCKER = docker run --rm -it -v $(shell pwd):/manim manimcommunity/manim manim
FILE ?= two_sum_visual.py
SCENE ?= TwoSumScene
MEDIA_DIR = media
OUTPUT_DIR = output

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
	rm -rf $(MEDIA_DIR)

# Convert MP4 to WebM
.PHONY: webm
webm:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Error: Both INPUT and OUTPUT are required."; \
		echo "Example: make webm INPUT=media/video.mp4 OUTPUT=media/video.webm"; \
		exit 1; \
	fi
	@docker run --rm -v $(shell pwd):/data jrottenberg/ffmpeg \
		-i "/data/$$(echo '$(INPUT)' | sed 's|^/||')" \
		-c:v libvpx-vp9 -c:a libvorbis -y \
		"/data/$$(echo '$(OUTPUT)' | sed 's|^/||')"

# Convert MP4 to GIF
.PHONY: gif
gif:
	@if [ -z "$(INPUT)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Error: Both INPUT and OUTPUT are required."; \
		echo "Example: make gif INPUT=media/video.mp4 OUTPUT=media/video.gif"; \
		exit 1; \
	fi
	@docker run --rm -v $(shell pwd):/data jrottenberg/ffmpeg \
		-i "/data/$$(echo '$(INPUT)' | sed 's|^/||')" \
		-vf "fps=10,scale=480:-1:flags=lanczos" -y \
		"/data/$$(echo '$(OUTPUT)' | sed 's|^/||')"

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
	@echo "  webm     - Convert MP4 to WebM (requires INPUT and OUTPUT)"
	@echo "  gif      - Convert MP4 to GIF (requires INPUT and OUTPUT)"
	@echo "Options for render targets:"
	@echo "  FILE=<file> SCENE=<scene>"
	@echo "Options for convert targets:"
	@echo "  INPUT=<input.mp4> OUTPUT=<output.webm|.gif> (relative to current directory)"
	@echo "Examples:"
	@echo "  make preview FILE=hashing.py SCENE=HashScene"
	@echo "  make webm INPUT=media/video.mp4 OUTPUT=media/video.webm"
	@echo "  make gif INPUT=media/video.mp4 OUTPUT=media/video.gif"
