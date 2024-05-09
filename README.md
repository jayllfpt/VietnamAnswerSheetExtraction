# Answer-Sheet-Extraction
Vietnamese High School Graduation Examination Answer Extraction using openCV-python

# Installation & Run
1. Clone repository
2. Run ```pip install -r requirements.txt```
3. Change the image path in ```tools/pipeline.py```
4. Run ```python tools/pipeline.py```
![screenshot: pipeline CLI](screenshot/pipelineCLI.png)

# Notes
- Highly recommend using conda/miniconda for avoiding evironments conflicts.
- Test specific features? use the code in ```tools/```

# APIs
1. Running using ```uvicorn app:app --port 1234```
2. Test API via Swagger UI
![screenshot: Swagger UI](screenshot/swaggerUI.jpeg)

# Algorithms
![diagram](screenshot/VNAnswerSheetExtractionDiagram.png)

# References
1. https://learnopencv.com/automatic-document-scanner-using-opencv/
2. https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
3. https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
4. https://www.analyticsvidhya.com/blog/2022/08/image-contrast-enhancement-using-clahe/
5. https://www.mathworks.com/help/visionhdl/ug/contrast-adaptive-histogram-equalization.html
6. https://docs.opencv.org/3.4/d8/d83/tutorial_py_grabcut.html