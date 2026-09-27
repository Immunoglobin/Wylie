# Wylie

Wylie is a robotics project for creating a mechanical scarecrow to ward off home garden pests.

The project builds on [PyThermalCamera](https://github.com/leswright1977/PyThermalCamera) as the basis for working with the TOPDON TC100.

## How it works

- Reads frames from a V4L2 video device (default `/dev/video0`).
- Each frame carries both image and thermal data; Wylie splits them and works with the image portion.
- The image is converted from YUYV to BGR, contrast-adjusted, and upscaled with bicubic interpolation.
- Optional processing can be toggled live: Gaussian blur, a JET colormap (grayscale mode), binary thresholding, and a Laplacian edge filter.
- OpenCV's `SimpleBlobDetector` looks for blobs in the frame.
- **When blobs are present, recording starts** and frames are written to an AVI file (XVID codec) in `videos/`. **When the blobs disappear, recording stops.**
- The live view is shown in a window titled `Critter-Cam`, with detected keypoints drawn on screen.

## Requirements

- Linux with V4L2 support
- Python 3
- [OpenCV](https://opencv.org/) (`cv2`) and `numpy`
- A TOPDON TC100 thermal camera (or another compatible V4L2 camera)

Install the Python dependencies:

```bash
sudo apt install v4l-utils qv4l2 vlc python3-opencv
```

## Setup

Confirm the camera is visible to the system:

```bash
v4l2-ctl --list-devices
```

Note the device number (e.g. `0` for `/dev/video0`).

## Usage

Run the app with the provided script:

```bash
./wylie.sh
```

or directly:

```bash
python3 src/main.py
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--device N` | Video device number (e.g. `0`). Find it with `v4l2-ctl --list-devices`. | `0` |

Example:

```bash
python3 src/main.py --device 1
```

### Keyboard controls

| Key | Action |
|-----|--------|
| `q` | Quit |
| `b` | Toggle Gaussian blur |
| `g` | Toggle grayscale (JET colormap) |
| `l` | Toggle Laplacian edge filter |
| `t` | Toggle binary threshold |
| `f` | Increase contrast |
| `v` | Decrease contrast |

## Project structure

```
Wylie/
├── src/
│   └── main.py        # Main application
├── videos/            # Recorded video output (git-ignored)
├── wylie.sh           # Launcher script
├── LICENSE            # Apache License 2.0
└── README.md
```

## License

Distributed under the [Apache License, Version 2.0](LICENSE).
