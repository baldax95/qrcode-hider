
# Steganography: Hiding an image inside another

## Usage

Create a `virtualenv` and install the requirements:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, merge and unmerge your files with:

```
python steganography.py merge --img1=res/img1.jpg --img2=res/img2.jpg --output=res/mixed.png

python steganography.py unmerge --img=res/mixed.png --output=res/unmerged.png
```

## Concept

I hided ``3 pixels of the qrCode`` inside ``1 pixel of the container image`` using the 3 color channels:
+ I put ``1 pixel of the qr`` (which is black or white, so I need only 1 channel of it) inside the ``R channel`` of 1 pixel of the container image,
+ then I put ``1 pixel of the qr`` inside the ``G channel`` of the same pixel of the container image,
+ and then I put another ``1 pixel of the qr`` inside the ``B channel`` of that pixel.

I place the pixels of the qrCode ``not adjacent`` inside the container image but I use a ``particular spacing`` so that I can also recover them.

I save the ``sizes of the qrCode`` inside a particular pixel of the container image so that I can recover them and use them to know when I'm done with unmerging.