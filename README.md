# MiniGimp
## Small python code to edit RGB and greyscale pictures with different filters/methods.
![1](https://github.com/LegendNeo/MiniGimp/blob/main/screenshot.png)

## Requirements and Installation

You need a recent version of python installed, at least python 3.9
You also need to have  a recent version of pip installed 
```
python3 pip install --upgrade pip
```

## Description

To run the programm simpy type python3 (or py depending on your version) followed by the filename, followed by the filters followed by the name of the picture
```
Example Input: "python3 minigimp.py --br 0.4 --th 200 --er picture.jpg"
```
```
--brightness (--br) followed by a float which multiplies the brightness -->                     --br 0.2
--threshold (--th) followed by a int [0;255] with 255 turning the picture complete dark -->     --th 200      
--contrast (--co) followed by a int [-255;255] with 255 making the most contrast -->            --co -100
--blur (--bl) followed by a int either 1 or 2 which changes the kernel -->                      --bl 2
--sharpen (--sh) -->                                                                            --sh
--changeColorChannel (--ch) followed by 12, 13 or 23 which represents the changing channels --> --ch 13
--erode (--er) -->                                                                              --er
--dilate (--di) -->                                                                             --di
```
