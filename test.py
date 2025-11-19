import cv2
import mediapipe as mp
import json
from pathlib import Path

mp_face_mesh = mp.solutions.face_mesh


def get_face_landmarks_from_image(image_path, save_path=None, max_faces=1, face_mesh=None):
    image_bgr = cv2.imread(str(image_path))
    if image_bgr is None:
        raise FileNotFoundError(f"Failed to read image: {image_path}")

    height, width, _ = image_bgr.shape
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    close_after = False
    if face_mesh is None:
        face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=max_faces,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        close_after = True

    results = face_mesh.process(image_rgb)

    faces_landmarks = []
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            pts = []
            for lm in face_landmarks.landmark:
                x = lm.x * width
                y = lm.y * height
                z = lm.z * width
                pts.append((x, y, z))
            faces_landmarks.append(pts)

    if close_after:
        face_mesh.close()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(faces_landmarks, f, indent=4)

    return faces_landmarks


if __name__ == "__main__":
    image_dir = Path(__file__).parent / "image"
    playblast_dir = image_dir / "playblast"
    landmark_dir = image_dir / "landmarks"

    landmark_dir.mkdir(parents=True, exist_ok=True)

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        for f in playblast_dir.glob("*.jpg"):
            parts = f.stem.split(".")
            name = parts[0]
            number = parts[1] if len(parts) > 1 else "0000"

            output_path = landmark_dir / f"landmarks.{number}.json"
            get_face_landmarks_from_image(
                f,
                save_path=output_path,
                max_faces=1,
                face_mesh=face_mesh,
            )
