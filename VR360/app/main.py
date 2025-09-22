import streamlit as st
import torch
import subprocess
from video_processor import process_stream
from deep_sort.deep_sort import DeepSort

# create a deepsort tracker instance using the pre-trained feature extraction model
tracker = DeepSort('./deep_sort/deep/checkpoint/ckpt.t7', use_cuda=torch.cuda.is_available())


st.title("360 Video Analytics Dashboard")
source_type = st.radio(
    "Select video source:",
    ["Uploaded file"],
    #["Webcam", "Uploaded file", "Stream URL"],
)




if source_type == "Webcam":
    from streamlit_webrtc import webrtc_streamer

    webrtc_streamer(
        key="video",
        video_frame_callback=process_stream,
        media_stream_constraints={"video": True, "audio": False},
    )




elif source_type == "Uploaded file" :
    camH = st.text_input("Camera height in metre:")
    uploaded_file = st.file_uploader("Upload a video or image", type=["mp4", "avi", "mov", "mkv", "jpg", "jpeg", "png"])
    if uploaded_file is not None:
        import cv2
        import numpy as np
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        # Try image decode first
        image = cv2.imdecode(file_bytes, 1)
        if image is not None:
            # It's an image
            annotated = process_stream(uploaded_file)
            st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB", caption="Processed Image")
        else:
            out_file_result  = './output_file.mp4'
            # Try video decode
            import tempfile
            uploaded_file.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
                tmpfile.write(uploaded_file.read())
                tmpfile_path = tmpfile.name
            
            cap = cv2.VideoCapture(tmpfile_path)
            
            # grab some parameters of video to use them for writing a new, processed video
            video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            video_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            video_fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
            # specify a writer to write a processed video to a disk frame by frame
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            outputfile = cv2.VideoWriter(out_file_result, fourcc, video_fps, (video_width, video_height))
            
            #stframe = st.empty()
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                annotated = process_stream(frame,tracker,float(camH) )
                #stframe.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB")
                outputfile.write(annotated)
            outputfile.release()
            cap.release()

            # re-encodes video to H264 using ffmpeg
            convertedVideo = "./convertedh264.mp4"
            subprocess.call(args=f"ffmpeg -y -i {out_file_result} -c:v libx264 {convertedVideo}".split(" "))
            
            # show results
            st.video(convertedVideo)

            '''
            with open(convertedVideo, 'rb') as file_download :
                # download file
                st.download_button(label="Download",
                                    data=file_download,
                                    file_name = "output_video.mp4",
                                    mime="video/mp4")
            '''

                
            



elif source_type == "Stream URL":
    url = st.text_input("RTSP/HTTP Stream URL:")
    if url:
        import cv2
        cap = cv2.VideoCapture(url)
        stframe = st.empty()
        if not cap.isOpened():
            st.error("Failed to open stream. Please check the URL.")
        else:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                annotated = process_stream(frame)
                stframe.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB")
            cap.release()