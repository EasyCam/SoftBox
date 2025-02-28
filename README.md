# SoftBox


SoftBox is a tool for photographer to use screen as a light box. This is also an extreme exercise of PySide6.


## Installation

```Bash
pip install softbox
```

## Usage in Python interpreter

After the installation step above, SoftBox now becomes available in Python. And you can simply use it by type the following commands in your Python interpreter :

```Bash
import sys
import softbox as sb
sys.exit(sb.begin())
```

## Run from Source Code

Clone the repository and run the following command in the root directory of the repository :

```Bash
git clone https://github.com/EasyCam/SoftBox.git
cd SoftBox
```

### Run the PySide6 Version

```Bash
cd softbox_gui
briefcase dev
```

### Run the Toga Version

```Bash
cd softbox_toga
briefcase dev
```
