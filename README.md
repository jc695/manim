# 🎬 Manim Visualizations

This project uses [Manim](https://www.manim.community/) (Mathematical Animation Engine) via Docker to generate mathematical or algorithmic animations from Python code.

Manim code → Docker container → MP4/WebM video 🎞️

---

## 📦 Prerequisites

- [Docker](https://www.docker.com/)
- `make` (comes with most UNIX systems like macOS or Linux)

---

## 🚀 Usage

### 🔁 Common Commands

Render animations using the provided `Makefile`:

#### ▶️ Preview in low quality (480p, 15fps):
```bash
make preview FILE=your_file.py SCENE=YourScene
```

#### 🎥 Render in high quality (1080p, 60fps):
```bash
make high FILE=your_file.py SCENE=YourScene
```

Other quality targets:
```bash
make low    # 480p, 15fps
make medium # 720p, 30fps
```

You can also use raw Docker commands:

```bash
docker run --rm -it -v $(pwd):/manim manimcommunity/manim manim your_file.py YourScene -pqh
```

---

## 🧹 Cleanup

Delete all generated media:
```bash
make clean
```

---

## 🔄 Convert MP4 to WebM

Use this to compress or convert output videos:
```bash
make convert INPUT=media/your_scene/videos/input.mp4 OUTPUT=media/your_scene/videos/output.webm
```

---

## 🛠️ Makefile Options

| Variable | Description                      |
|----------|----------------------------------|
| `FILE`   | Python script (e.g. `my_vis.py`) |
| `SCENE`  | Scene class name (e.g. `MyScene`)|
| `INPUT`  | (for `convert`) Input MP4 path   |
| `OUTPUT` | (for `convert`) Output WebM path |

---

## 📂 Project Structure

```bash
manim/
├── your_scene.py         # Python scene definitions
├── Makefile              # Docker-based build system
├── README.md             # This file
└── media/                # Output videos (auto-generated)
```

---

## 💡 Example

Render a consistent hashing animation:

```bash
make high FILE=consistent_hashing_visual.py SCENE=ConsistentHashingScene
```

Or preview it:

```bash
make preview FILE=consistent_hashing_visual.py SCENE=ConsistentHashingScene
```

---

## 🐳 Docker Notes

Manim's Docker image (`manimcommunity/manim`) is used to ensure consistent rendering across platforms. If you see errors about `xdg-open`, remove the `-p` flag or manually open the generated video from:

```
./media/videos/<scene_folder>/<quality>/YourScene.mp4
```

---

## 📎 Resources

- [Official Manim Docs](https://docs.manim.community/)
- [Manim Examples Repo](https://github.com/ManimCommunity/manim-examples)
