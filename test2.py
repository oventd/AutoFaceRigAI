import json
import cv2
import os


def load_landmarks_from_json(json_path, frame_index=0):
    """
    Load landmark coordinates from a JSON file.

    Accepts two structures:
        1) [ [x, y, z], [x, y, z], ... ]
        2) [ [ [x, y, z], ... ],  [ [x, y, z], ... ], ... ]  # multiple frames

    Args:
        json_path (str): Path to the JSON file.
        frame_index (int): Index of the frame to use if multiple frames exist.

    Returns:
        list[tuple]: List of (x, y, z) tuples.
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    # Case 1: data is directly a list of [x, y, z]
    if data and isinstance(data[0], (list, tuple)) and isinstance(data[0][0], (int, float)):
        points = data

    # Case 2: data is a list of frames: [ [ [x,y,z], ... ], [ [x,y,z], ... ] ]
    elif data and isinstance(data[0], (list, tuple)) and isinstance(data[0][0], (list, tuple)):
        try:
            points = data[frame_index]
        except IndexError:
            raise IndexError(f"Frame index {frame_index} is out of range for this JSON.")
    else:
        raise ValueError("Unsupported JSON structure for landmarks.")

    # Convert to list of tuples
    landmarks = [tuple(p[:3]) for p in points]  # (x, y, z)
    return landmarks


def draw_landmarks_on_image(image_path, landmarks, output_path=None, draw_index=False):
    """
    Draw landmark points on an image.

    Args:
        image_path (str): Path to the input image.
        landmarks (list[tuple]): List of (x, y, z) landmark coordinates.
        output_path (str or None): Output image path. If None, saves next to original.
        draw_index (bool): If True, also draw point index text.

    Returns:
        str: Output image path.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise IOError(f"Failed to read image: {image_path}")

    height, width = image.shape[:2]

    # If your coordinates are normalized (0~1), uncomment this:
    # scaled = []
    # for x, y, z in landmarks:
    #     scaled.append((x * width, y * height, z))
    # landmarks = scaled

    for idx, (x, y, z) in enumerate(landmarks):


        # Convert to int pixel coords
        px = int(round(x))
        py = int(round(y))

        # Skip points outside the image
        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        # Draw a small circle at the point
        cv2.circle(image, (px, py), 3, (0, 255, 0), thickness=-1)  # filled circle

        # Optionally draw index label
        if draw_index:
            cv2.putText(
                image,
                str(idx),
                (px + 5, py - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )

    # Determine output path
    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_landmarks{ext}"

    cv2.imwrite(output_path, image)
    return output_path


def visualize_mediapipe_landmarks(json_path, image_path, output_path=None, frame_index=0, draw_index=False):
    """
    High-level helper:
    - Load landmarks from JSON
    - Draw them on the image
    - Save the result

    Args:
        json_path (str): Path to the landmark JSON.
        image_path (str): Path to the input image.
        output_path (str or None): Output image path.
        frame_index (int): Which frame to use if JSON contains multiple frames.
        draw_index (bool): If True, draw point indices as text.

    Returns:
        str: Output image path.
    """
    landmarks = load_landmarks_from_json(json_path, frame_index=frame_index)
    out = draw_landmarks_on_image(image_path, landmarks, output_path, draw_index=draw_index)
    print(f"Saved visualization to: {out}")
    return out


if __name__ == "__main__":
    # Example usage:
    # python visualize_landmarks.py path/to/landmarks.json path/to/image.png
    
    index = 72
    json_path_arg = fr"D:\code\AutoFaceRigAI\image\landmarks\landmarks.{str(index).zfill(4)}.json"
    image_path_arg = rf"D:\code\AutoFaceRigAI\image\playblast\tracker.{str(index).zfill(4)}.jpg"
    frame_idx_arg = 0

    visualize_mediapipe_landmarks(
        json_path_arg,
        image_path_arg,
        output_path=r"D:\code\AutoFaceRigAI\test.png",
        frame_index=frame_idx_arg,
        draw_index=True,
    )
