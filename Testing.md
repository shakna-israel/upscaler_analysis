% A Basic Analysis of `cart_repair` Upscaling Algorithm

## Technical Information

The dependencies for the test rig, are found in the file `requirements-test.txt`. (The usual dependencies must also be available).

Our upscaling algorithm does not intend to generate a 1:1 copy of an image, but rather an image that is perceptually similar to the original. A loss of detail for an increase in quality is acceptable, however the question is, how much loss of detail occurs? Measuring this objectively is extremely difficult. This paper approximates a way to measure the loss.

---

## Overview

The supplied `test.py` script will attempt to extract the difference between the original and the upscaled version using an implementation [^imagehash] of Wavelet Hashing [^wavelethash].

    def process_frame(image, scale):
        pil_im = Image.fromarray(image)
        before_hash = imagehash.whash(pil_im)

        processed = cart_repair.process_frame(image, scale)
        pil_im = Image.fromarray(processed)
        after_hash = imagehash.whash(pil_im)

        diff = before_hash - after_hash
        return diff

The closer to 0 the value returned, the better our algorithm is preserving the original image.

The script also compares the result to the bicubic equivalent. It is expected that for bicubic upscaling the difference will usually be 0. It isn't altering the image significantly, despite the dramatic quality loss that often results. Pixelisation is ignored by most perceptual hashing algorithms.

Bicubic was chosen as the most important comparison as it is frequently the default interpolation method for many resizing algorithms utilised throughout the industry, despite its somewhat poor performance.

    def compare_frame(image, scale, interp = cv2.INTER_CUBIC):
        height, width, channels = image.shape
        pil_im = Image.fromarray(image)
        before_hash = imagehash.whash(pil_im)
        
        processed = cv2.resize(image,
            (math.floor(width * scale), math.floor(height * scale)),
            interpolation = interp)
        pil_im = Image.fromarray(processed)
        after_hash = imagehash.whash(pil_im)
        
        diff = before_hash - after_hash
        return diff

Other comparisons also include: Nearest Neighbour, Bilinear, Area, and Lanczos v4.

Our algorithm applies more extensive changes to the original image, and measuring that detail loss is possible through this process. When the upscaler receives a worse diff result than the bicubic equivalent, the dataset contains something that the upscaler fails to preserve accurately.

The upscaler does not preserve quality 1:1. This is known, and expected. This testing algorithm simply measures that.

---

## Generating Data

If you run the `test.py` script against a single image, it will return you just the difference between the original and final image.

To get the more extensive data, you need to run it against a video file. At completion (or interruption via the keyboard), the script will attempt to write the comparison plot to a file called `diffs.png`.

The raw data should also be written to a JSON (JavaScript Object Notation) file called `diffs.json`. The "upscaler" key contains the resulting diff using our algorithm, and the "bicubic" key contains the bicubic equivalent diff, and so on. The integers are Hamming distance values.

Example JSON:

    {"upscaler": [2, 0],
     "bicubic": [2, 0],
     "nearest": [2, 0],
     "linear": [2, 0],
     "area": [2, 0],
     "lanczos4": [2, 0]}

These outputs should be reproducible, if the same dataset (image or video file) is being tested.

---

## Results - 200% Scale

On our test dataset, a version of the 1911 Epee Dual [^epeedual] was processed, at a scale of 200%. 601 frames were examined.

The exact command run was:

    python test.py -i demo.mp4 -s 2

[//]: # (Our generated plot of data:)

![Plot of outputs](diffs_x2.png)

A simple plot shows that, for the most part, all the tested algorithms are relatively close to each other, which is what you would expect when scaling to 200%. However, you can already see that there are some differences that may become clearer when looking at the individual numbers.

---

### Hamming Distance Counts - 200% Scale

| Algorithm         | Distance: 0 | Distance: 2 | Distance: 4 |
| :---------------- | ----------: | ----------: | ----------: |
| Bicubic           | 114         | 485         | 2           |
| Nearest Neighbour | 111         | 486         | 4           |
| Bilinear          | 113         | 483         | 5           |
| Area              | 111         | 486         | 4           |
| Lanczos v4        | 116         | 483         | 2           |
| Ours              | 170         | 431         | 6           |

A Hamming distance of 0 means there is no difference found.

A Hamming distance of 2 means there is some difference found, but that the images are still likely the same. Usually there has been some quality loss between the images.

A Hamming distance of 4 means that there has been significant quality loss.

A Hamming distance of greater than 5 is a general rule for images that are not considered to be the same, used by the industry. Any upscale algorithm scoring a 5 can be considered to be a failure. Thankfully none of the tested algorithms failed at 200% scaling.

### Predictions of Quality Loss - 200% Scale

Translating this, we can make a few predictions.

These predictions are only true when looking at 200% scaling.

The table below shows the rough chance of experiencing quality loss when upscaling at 200%.

| Algorithm         | Expected Quality Loss | Expected Significant Quality Loss |
| :---------------- | --------------------: | --------------------------------: |
| Bicubic           | 81.03%                | 0.3%                              |
| Nearest Neighbour | 81.53%                | 0.6%                              |
| Bilinear          | 81.19%                | 0.8%                              |
| Area              | 81.53%                | 0.6%                              |
| Lanczos v4        | 80.69%                | 0.3%                              |
| Ours              | 72.71%                | 0.9%                              |

Our algorithm seems to suffer here somewhat. It has a higher chance of significant quality loss than any of the other algorithms. Worse even than bilinear upscaling.

However, the overall chance of quality loss is much less than any of the others.

---

## Results - 300% Scale

[//]: # (TODO: Framecount)

On our test dataset, a version of the 1911 Epee Dual [^epeedual] was processed, at a scale of 300%. N frames were examined.

The exact command run was:

    python test.py -i demo.mp4 -s 3

[//]: # (Our generated plot of data:)

![Plot of outputs](diffs_x3.png)

A simple plot shows that, for the most part, all the tested algorithms are relatively close to each other, which is what you would expect when scaling to 300%. However, you can already see that there are some differences that may become clearer when looking at the individual numbers.

---

### Hamming Distance Counts - 300% Scale

[//]: # (TODO: Data counts)

| Algorithm         | Distance: 0 | Distance: 2 | Distance: 4 |
| :---------------- | ----------: | ----------: | ----------: |
| Bicubic           |             |             |             |
| Nearest Neighbour |             |             |             |
| Bilinear          |             |             |             |
| Area              |             |             |             |
| Lanczos v4        |             |             |             |
| Ours              |             |             |             |

A Hamming distance of 0 means there is no difference found.

A Hamming distance of 2 means there is some difference found, but that the images are still likely the same. Usually there has been some quality loss between the images.

A Hamming distance of 4 means that there has been significant quality loss.

[//]: # (TODO: Did any of the algos fail?)

A Hamming distance of greater than 5 is a general rule for images that are not considered to be the same, used by the industry. Any upscale algorithm scoring a 5 can be considered to be a failure.

---

### Predictions of Quality Loss - 300% Scale

Translating this, we can make a few predictions.

These predictions are only true when looking at 300% scaling.

The table below shows the rough chance of experiencing quality loss when upscaling at 300%.

[//]: # (TODO: Fill in our data)

| Algorithm         | Expected Quality Loss | Expected Significant Quality Loss |
| :---------------- | --------------------: | --------------------------------: |
| Bicubic           |                       |                                   |
| Nearest Neighbour |                       |                                   |
| Bilinear          |                       |                                   |
| Area              |                       |                                   |
| Lanczos v4        |                       |                                   |
| Ours              |                       |                                   |

[//]: # (TODO: Analysis of how well our algorithm faired compared to the competition)

---

## The Process

This is a high-level description of the process, which is slightly convoluted. You should not expect to be able to duplicate the results from this, however it may put you on the right track. The actual algorithm will be released to the public at some point, but for now it is only used in production by SIXTEENmm [^sixteenmm].

A copy of the original image is resized using a bilinear algorithm, and then denoised using a complicated algorithm. [^denoise]. This frame is blended at 50% with a black empty frame of the appropriate size.

Next, a X & Y Sobel gradient is generated from the smoothed but unblended layer, denoised using the same algorithm [^denoise], and then the colour inverted. This layer is blended onto the existing stack at 70%.

A K-means clustering algorithm is used to create a quantized layer. K-selection for the algorithm is slightly complicated, but is roughly:

    c10 = colour_count / 1000
    if c10 > 0:
        if c10 > 48:
            colour_count = c10
        else:
            colour_count = 48
    else:
        colour_count = 48

    if colour_count < 100:
        colour_count = colour_count * 2

This results in a minimum of 96 for K, without an upper bound but with a generally reasonable range of less than a thousand.

The quantized layer is then blended onto the stack at 70%.

The X & Y Sobel gradient layer from earlier is then re-blended onto the stack at 30%.

Finally we do some contrast correction, and then apply the denoising algorithm [^denoise] to the result.

---

[^imagehash]: Buchner, Johannes (2020). imagehash. https://github.com/JohannesBuchner/imagehash/

[^epeedual]: Pierre Mortier vs. Gustave Tery (1911). https://archive.org/details/1911pierremortiervsgustavetery

[^wavelethash]: Petrov, Dmitry (2016). Wavelet image hash in Python. https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5

[^denoise]: Buades, Antoni. Coll, Bartomeu. Morel, Jean-Michel (2011).  Non-Local Means Denoising. https://www.ipol.im/pub/art/2011/bcm_nlm/

[^sixteenmm]: SIXTEENmm. https://sixteenmm.org
