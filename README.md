# ATS-Auto-Drive 美国卡车模拟自动驾驶

Install:

1. Install PyTorch.
Go https://pytorch.org/get-started/locally/ to copy the command. For example, I'm using Windows and Nvidia GPU, so I use this command:
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

2. Intall ultralytics (YOLOv8).
Go https://github.com/ultralytics/ultralytics or use this command
```bash
pip install ultralytics
```
3. Install pywin32.
```bash
pip install pywin32
```

Please open American Truck Simulator first and then start the program

Progress: (🤗 -> done ☝️🤓 -> Work In Progress)

1. Capture game footage 🤗
2. Detect truck's speed 🤗
3. Detect objects using YOLOv8 🤗
4. ???
