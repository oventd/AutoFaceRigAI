# Advenced Skeleton AI Facial Auto Rig

# Process
1. Import the MetaHuman character
2. Set up the camera
	1. using the head joint
	2. **OpenMaya**
3. Capture viewport screenshots from multiple angles
4. Generate 2D landmark data with an AI model
	1. AI model : **Mediapipe Face Mesh**
5. Convert 2D landmarks to 3D 
	1. **Raycasting**
	2. **OpenMaya**
	3. Save as **USD**
6. Refine the 3D data
	1. Algoridm : **RANSAC**
	2. Save as **USD**
7. Create a JSON mapping for Advanced Skeleton
8. Apply the JSON to Advanced Skeleton
9. Build the rig

- Pipeine base = Prism
