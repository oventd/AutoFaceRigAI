import cv2
import mediapipe as mp

# Prepare mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh

def get_face_landmarks_from_image(image_path, max_faces=1):
    """
    Read an image from disk and return facial landmarks.

    :param image_path: Path to the input image.
    :param max_faces: Maximum number of faces to detect.
    :return: List of faces, each face is a list of (x, y, z) in pixel space.
             If no face is found, returns [].
    """
    # Load image
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"Failed to read image: {image_path}")

    height, width, _ = image_bgr.shape

    # Convert BGR (OpenCV) -> RGB (mediapipe)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Run FaceMesh
    faces_landmarks = []
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,       # single image mode
        max_num_faces=max_faces,
        refine_landmarks=True,       # include iris / more detailed landmarks
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            return []  # No face detected

        for face_landmarks in results.multi_face_landmarks:
            pts = []
            for lm in face_landmarks.landmark:
                # Mediapipe gives normalized coords [0,1] -> convert to pixel space
                x = lm.x * width
                y = lm.y * height
                z = lm.z * width  # z is relative, scale with width for consistency
                pts.append((x, y, z))
            faces_landmarks.append(pts)

    return faces_landmarks


if __name__ == "__main__":
    img_path = r"D:\code\AutoFaceRigAI\image\playblast\tracker.0001.jpg"
    faces = get_face_landmarks_from_image(img_path, max_faces=1)

    if not faces:
        print("No face found")
    else:
        # First face, first 5 points preview
        first_face = faces[0]
        print(f"Detected {len(first_face)} landmarks.")
        for i, (x, y, z) in enumerate(first_face[:5]):
            print(f"landmark {i}: x={x:.2f}, y={y:.2f}, z={z:.4f}")
