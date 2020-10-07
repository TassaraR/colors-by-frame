# colors_by_frame
Creates images from videos by computing the average colors by its frames

### Usage:
```
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file path
  -s SHAPE, --shape SHAPE
                        Output shape in format (height px, width px)    default = (1080, 1920)
```
When no `INPUT` is provided a dialog window opens up to help choose the desired file.

### Example:
```
$python colors_by_frames.py
```
```
Input Frame Data:
        Height: 808
        Width: 1920
        fps: 23.98

Output Img:
        Height: 1080
        Width: 1920

>Progress: [||||||                   ] 24%
```
### Sample Output:
> Spiderman: Into the Spiderverse

![Sample](/output_images/Into_The_Spiderverse.png)
