# A Basic Analysis of `cart_repair` Upscaling Algorithm

---

## Summary

The `cart_repair` upscaling algorithm attempts to preserve the human perception of quality, whilst having some acceptable level of detail loss. As the algorithm is originally intended for video processing work, it was created with the idea that the human brain will fill in details that may come and go between individual frames so that the viewer is not particularly aware that the video they are watching is not a 1:1 preservation of the original.

In the subjective testing throughout development, it was found to work well on images up to 200% scaling, and depending on the subject media, have passable results at 300% scaling. It falls short above that scale.

However, the subjective analysis of an image doesn't supply us with a source of truth. This document reflects an attempt to create an objective measure to compare the algorithm against existing industry standard algorithms, and to provide a source of truth that could be used for further improvements to the algorithm.

---

## Reading

You can find the main body of text in the file `Testing.md`.

We recommend generating a PDF with:

	pandoc --toc Testing.md -o Testing.pdf

---

## Supplementary Materials

The repository has a number of other files that can be useful when analysing the work.

This includes the results from the hash comparisons in JSON files, and the code used to generate the comparisons.
