# Source images

Originals that `tools/prepare_images.py` turns into the web-ready files in `assets/img/`.

| File | What it is |
| --- | --- |
| `wheeler-front.png` | Engineering drawing of Wheeler from the front, rendered from the CAD model |
| `wheeler-rear.png` | The same model from the rear |
| `founder-portrait.jpg` | Founder portrait |

## How the Wheeler drawings are made

The drawings are rendered from a copy of the Wheeler CAD assembly, never from the working file. They show what is visible in the saved model, with one addition: the left wheel's rim and tyre, which are hidden in the file, are switched back on so both wheels match. Superseded designs, reference copies and construction geometry stay hidden.

The render is orthographic. Outlines are drawn where one part meets another and where a surface changes direction, and the shading is mapped onto the site's ink colour so the pictures read as drawings.

The export and render scripts are kept with the robot's engineering files, not in this public repository.
